import math
import pymunk
from engine.component import Component
from engine.components.transform import Transform

class LineBody2D(Component):
    def __init__(self, point_a=(0, 0), point_b=(0, 0), thickness=1.0, mass=1.0, static=False, debug=False, offset=(0, 0)):
        """
        A 2D rigidbody represented as a line (segment).

        Args:
            point_a (tuple): Local start point of the line (x, y).
            point_b (tuple): Local end point of the line (x, y).
            thickness (float): Thickness (radius) of the line collider.
            mass (float): Mass of the body (ignored if static).
            static (bool): Whether the body is static (immovable).
            debug (bool): Whether to render debug collider.
            offset (tuple): Local offset from the Transform's position.
        """
        super().__init__()
        self.point_a = point_a
        self.point_b = point_b
        self.thickness = thickness
        self.mass = mass
        self.static = static
        self.debug = debug
        self.offset = offset
        self.transform: Transform = None
        self.body: pymunk.Body = None
        self.shape: pymunk.Segment = None

        # Cache
        self._last_transform_state = None
        self._world_a = None
        self._world_b = None

    def start(self):
        self.transform = self.game_object.get_component(Transform)

        # Create body
        if self.static:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            safe_mass = max(self.mass, 0.0001)
            moment = pymunk.moment_for_segment(safe_mass, self.point_a, self.point_b, self.thickness)
            self.body = pymunk.Body(safe_mass, moment)

        # Set initial position/rotation from Transform + offset
        pos_x, pos_y = self.transform.get_world_position()
        self.body.position = (pos_x + self.offset[0], pos_y + self.offset[1])
        self.body.angle = math.radians(self.transform.local_rotation)
        self.transform._rb_body = self.body

        # Create segment shape
        self.shape = pymunk.Segment(self.body, self.point_a, self.point_b, self.thickness)
        self.shape.friction = 0.7
        self.shape.elasticity = 0.0

        # Add to physics space
        self.game_object.scene.physics_space.add(self.body, self.shape)

        # Precompute endpoints
        self._apply_transform()

    def _apply_transform(self):
        """
        Internal: recompute world endpoints based on Transform position, rotation, and offset.
        """
        angle_rad = math.radians(self.transform.local_rotation)

        # Rotate local points by angle
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        def rotate_point(p):
            return (p[0] * cos_a - p[1] * sin_a,
                    p[0] * sin_a + p[1] * cos_a)

        rotated_a = rotate_point(self.point_a)
        rotated_b = rotate_point(self.point_b)

        pos_x, pos_y = self.transform.get_world_position()
        offset_x, offset_y = self.offset
        self._world_a = (rotated_a[0] + pos_x + offset_x, rotated_a[1] + pos_y + offset_y)
        self._world_b = (rotated_b[0] + pos_x + offset_x, rotated_b[1] + pos_y + offset_y)

        # Store cached state
        self._last_transform_state = (self.transform.local_rotation,
                                      self.transform.local_x,
                                      self.transform.local_y)

    def render(self, surface):
        if not self.debug or not self._world_a or not self._world_b:
            return
        import pygame
        camera = getattr(self.game_object.scene, "camera_component", None)

        a = self._world_a
        b = self._world_b

        a_screen = camera.world_to_screen(*a) if camera else a
        b_screen = camera.world_to_screen(*b) if camera else b

        pygame.draw.line(surface, (255, 0, 0), a_screen, b_screen, int(self.thickness * 2))

        # Draw centre of mass
        com = camera.world_to_screen(*self.body.position) if camera else self.body.position
        pygame.draw.circle(surface, (0, 255, 0), (int(com[0]), int(com[1])), 3)

    def reset_to_start(self):
        # Recreate body
        if self.static:
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else:
            safe_mass = max(self.mass, 0.0001)
            moment = pymunk.moment_for_segment(safe_mass, self.point_a, self.point_b, self.thickness)
            self.body = pymunk.Body(safe_mass, moment)

        # Reset position & rotation from transform
        pos_x, pos_y = self.transform.get_world_position()
        self.body.position = (pos_x + self.offset[0], pos_y + self.offset[1])
        self.body.angle = math.radians(self.transform.local_rotation)

        # Recreate segment shape
        self.shape = pymunk.Segment(self.body, self.point_a, self.point_b, self.thickness)
        self.shape.friction = 0.7
        self.shape.elasticity = 0.0

        # Add back to physics space
        self.game_object.scene.physics_space.add(self.body, self.shape)

        # Update cached endpoints
        self._apply_transform()
