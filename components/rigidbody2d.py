# rigidbody2d.py
import math
import pymunk
from component import Component
from components.transform import Transform


class Rigidbody2D(Component):
    def __init__(
        self,
        shape_type="box",  # "box" or "circle"
        width=0,
        height=0,
        radius=0,
        mass=1.0,
        static=False,
        debug=False,
        freeze_rotation=False,
    ):
        """
        2D Rigidbody component supporting box and circle colliders.

        Args:
            shape_type (str): "box" or "circle"
            width (float): Box width
            height (float): Box height
            radius (float): Circle radius
            mass (float): Mass of the body
            static (bool): If True, body is immovable
            debug (bool): If True, render debug visuals
            freeze_rotation (bool): If True, prevents rotation
        """
        super().__init__()
        self.shape_type = shape_type
        self.width = width
        self.height = height
        self.radius = radius
        self.mass = mass
        self.static = static
        self.debug = debug
        self.freeze_rotation = freeze_rotation

        self.transform: Transform = None
        self.body: pymunk.Body = None
        self.shape: pymunk.Shape = None

    def start(self):
        self.transform = self.game_object.get_component(Transform)
        self._create_body()

    def reset_to_start(self):
        if not self.transform:
            self.transform = self.game_object.get_component(Transform)
        self._create_body()

    def _create_body(self):
        """Internal method to create the pymunk body and shape."""
        # Determine scaled dimensions
        scale_x, scale_y = self.transform.local_scale_x, self.transform.local_scale_y

        if self.shape_type == "box":
            width = max(self.width * scale_x, 1)
            height = max(self.height * scale_y, 1)
        elif self.shape_type == "circle":
            width = height = radius = max(self.radius * max(scale_x, scale_y), 1)
        else:
            raise ValueError(f"Unknown shape_type: {self.shape_type}")

        # Create body
        if self.static:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            safe_mass = max(self.mass, 0.0001)
            if self.shape_type == "box":
                moment = float("inf") if self.freeze_rotation else pymunk.moment_for_box(safe_mass, (width, height))
            else:  # circle
                moment = float("inf") if self.freeze_rotation else pymunk.moment_for_circle(safe_mass, 0, radius)
            self.body = pymunk.Body(safe_mass, moment)

        self.body.position = self.transform.get_local_position()
        self.body.angle = math.radians(self.transform.get_local_rotation())
        self.transform._rb_body = self.body

        # Create shape
        if self.shape_type == "box":
            self.shape = pymunk.Poly.create_box(self.body, (width, height))
        else:  # circle
            self.shape = pymunk.Circle(self.body, radius)

        self.shape.friction = 0.7
        self.shape.elasticity = 0.0

        self.game_object.scene.physics_space.add(self.body, self.shape)

    def apply_force(self, fx, fy):
        """Apply a force to the body at its center."""
        self.body.apply_force_at_world_point((fx, fy), self.body.position)

    def fixed_update(self, dt):
        """Sync transform with physics body."""
        if self.body:
            self.transform.set_world_position(*self.body.position)
            self.transform.set_local_rotation(math.degrees(self.body.angle))

    def render(self, surface):
        if not self.debug:
            return
        import pygame

        camera = getattr(self.game_object.scene, "camera_component", None)
        pos = camera.world_to_screen(*self.body.position) if camera else self.body.position
        pos = (int(pos[0]), int(pos[1]))

        # Draw shape
        if self.shape_type == "box":
            vertices = [v.rotated(self.body.angle) + self.body.position for v in self.shape.get_vertices()]
            points = [camera.world_to_screen(*v) if camera else v for v in vertices]
            for i in range(len(points)):
                pygame.draw.line(surface, (255, 0, 0), points[i], points[(i + 1) % len(points)], 2)
        else:  # circle
            pygame.draw.circle(surface, (255, 0, 0), pos, int(self.shape.radius//2), 2)

        # Draw center of mass
        pygame.draw.circle(surface, (0, 255, 0), pos, 3)

        # Draw local axes
        axis_length = 20
        angle = self.body.angle
        x_axis_end = (pos[0] + axis_length * math.cos(angle), pos[1] + axis_length * math.sin(angle))
        y_axis_end = (pos[0] - axis_length * math.sin(angle), pos[1] + axis_length * math.cos(angle))
        pygame.draw.line(surface, (0, 0, 255), pos, x_axis_end, 2)
        pygame.draw.line(surface, (255, 255, 0), pos, y_axis_end, 2)
