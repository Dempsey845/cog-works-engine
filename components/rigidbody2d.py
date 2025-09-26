import math
import pymunk
from component import Component
from components.transform import Transform

class Rigidbody2D(Component):
    def __init__(self, width=0, height=0, mass=1.0, static=False, debug=False, freeze_rotation=False):
        """
        Initialize a 2D rigidbody component.

        Args:
            width (float): Width of the collider box.
            height (float): Height of the collider box.
            mass (float): Mass of the body (ignored if static).
            static (bool): Whether the body is static (immovable).
            debug (bool): Whether to render debug collider.
            freeze_rotation (bool): If True, prevents rotation of the body.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.mass = mass
        self.static = static
        self.debug = debug
        self.freeze_rotation = freeze_rotation
        self.transform: Transform = None
        self.body: pymunk.Body = None
        self.shape: pymunk.Poly = None

    def start(self):
        self.transform = self.game_object.get_component(Transform)

        # Compute scaled width and height based on Transform scale
        scaled_width = max(self.width * self.transform.local_scale_x, 1)
        scaled_height = max(self.height * self.transform.local_scale_y, 1)

        # Create static or dynamic body
        if self.static:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            # Extra protection for freeze_rotation
            if self.freeze_rotation:
                # Prevent invalid moments by ensuring mass is positive
                safe_mass = max(self.mass, 0.0001)
                moment = float('inf') if safe_mass > 0 else 0
            else:
                # Ensure width/height are valid for moment calculation
                scaled_width = max(scaled_width, 0.1)
                scaled_height = max(scaled_height, 0.1)
                safe_mass = max(self.mass, 0.0001)
                moment = pymunk.moment_for_box(safe_mass, (scaled_width, scaled_height))

            self.body = pymunk.Body(safe_mass, moment)

        # Set initial position and rotation from Transform
        self.body.position = self.transform.get_world_position()
        self.body.angle = math.radians(self.transform.local_rotation)
        self.transform._rb_body = self.body

        # Create box collider shape
        self.shape = pymunk.Poly.create_box(self.body, (scaled_width, scaled_height))
        self.shape.friction = 0.7
        self.shape.elasticity = 0.0

        # Add body and shape to the scene's physics space
        self.game_object.scene.physics_space.add(self.body, self.shape)


    def apply_force(self, fx, fy):
        """
        Apply a force to the body at its centre of mass.

        Args:
            fx (float): Force along the X axis.
            fy (float): Force along the Y axis.
        """
        self.body.apply_force_at_world_point((fx, fy), self.body.position)

    def fixed_update(self, dt):
        """
        Called every physics step.
        Updates the Transform position and rotation based on the Rigidbody's
        current physics state.
        """
        if self.body:
            self.transform.set_world_position(*self.body.position)
            self.transform.set_local_rotation(math.degrees(self.body.angle))

    def render(self, surface):
        if not self.debug:
            return
        import pygame
        camera = getattr(self.game_object.scene, "camera_component", None)

        # Draw collider box
        vertices = [v.rotated(self.body.angle) + self.body.position for v in self.shape.get_vertices()]
        points = [camera.world_to_screen(*v) if camera else v for v in vertices]
        for i in range(len(points)):
            pygame.draw.line(surface, (255, 0, 0), points[i], points[(i + 1) % len(points)], 2)

        # Draw center of mass
        com = camera.world_to_screen(*self.body.position) if camera else self.body.position
        com = (int(com[0]), int(com[1]))
        pygame.draw.circle(surface, (0, 255, 0), com, 3)

        # Draw local axes
        axis_length = 20  # pixels
        angle = self.body.angle
        x_axis_end = (com[0] + axis_length * math.cos(angle),
                      com[1] + axis_length * math.sin(angle))
        y_axis_end = (com[0] - axis_length * math.sin(angle),
                      com[1] + axis_length * math.cos(angle))

        pygame.draw.line(surface, (0, 0, 255), com, x_axis_end, 2)  # X axis in blue
        pygame.draw.line(surface, (255, 255, 0), com, y_axis_end, 2)  # Y axis in yellow


