import math
import pymunk
from components.transform import Transform
from components.rigidbody2d import Rigidbody2D

class CircleBody2D(Rigidbody2D):
    def __init__(self, radius=10, mass=0.2, static=False, debug=False, freeze_rotation=False):
        """
        Initialize a 2D circular rigidbody.

        Args:
            radius (float): Radius of the circle collider.
            mass (float): Mass of the body (ignored if static).
            static (bool): Whether the body is static (immovable).
            debug (bool): Whether to render debug collider.
            freeze_rotation (bool): If True, prevents rotation of the body.
        """
        super().__init__(width=radius*2, height=radius*2, mass=mass, static=static, debug=debug, freeze_rotation=freeze_rotation)
        self.radius = radius
        self.shape: pymunk.Circle = None

    def start(self):
        self.transform = self.game_object.get_component(Transform)

        # Compute scaled radius based on Transform scale (taking max scale for simplicity)
        scaled_radius = max(self.radius * max(self.transform.local_scale_x, self.transform.local_scale_y), 1)

        # Create static or dynamic body
        if self.static:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            moment = math.inf if self.freeze_rotation else pymunk.moment_for_circle(self.mass, 0, scaled_radius)
            self.body = pymunk.Body(self.mass, moment)

        # Set initial position and rotation from Transform
        self.body.position = self.transform.get_world_position()
        self.body.angle = math.radians(self.transform.local_rotation)
        self.transform._rb_body = self.body

        # Create circle collider shape
        self.shape = pymunk.Circle(self.body, scaled_radius)
        self.shape.friction = 0.7
        self.shape.elasticity = 0.0

        # Add body and shape to the scene's physics space
        self.game_object.scene.physics_space.add(self.body, self.shape)

    def render(self, surface):
        if not self.debug:
            return
        import pygame
        camera = getattr(self.game_object.scene, "camera_component", None)

        # Draw circle
        pos = camera.world_to_screen(*self.body.position) if camera else self.body.position
        pos = (int(pos[0]), int(pos[1]))
        radius = int(self.shape.radius) //2
        pygame.draw.circle(surface, (255, 0, 0), pos, radius, 2)

        # Draw center of mass
        pygame.draw.circle(surface, (0, 255, 0), pos, 3)

        # Draw local axes
        axis_length = 20  # pixels
        angle = self.body.angle
        x_axis_end = (pos[0] + axis_length * math.cos(angle),
                      pos[1] + axis_length * math.sin(angle))
        y_axis_end = (pos[0] - axis_length * math.sin(angle),
                      pos[1] + axis_length * math.cos(angle))

        pygame.draw.line(surface, (0, 0, 255), pos, x_axis_end, 2)  # X axis in blue
        pygame.draw.line(surface, (255, 255, 0), pos, y_axis_end, 2)  # Y axis in yellow
