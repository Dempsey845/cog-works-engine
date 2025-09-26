import pygame
from component import Component


class Transform(Component):
    """
    Core component for position, rotation, and scale.
    All GameObjects have a Transform to determine their placement in the world.
    """

    def __init__(self, x=0, y=0, rotation=0, scale_x=1, scale_y=1):
        super().__init__()
        self.x = x
        self.y = y
        self.rotation = rotation  # in degrees
        self.scale_x = scale_x
        self.scale_y = scale_y

    # --- Position Methods ---
    def set_position(self, x, y):
        """Set absolute position."""
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Move relative to current position."""
        self.x += dx
        self.y += dy

    def get_position(self):
        """Return current position as a tuple (x, y)."""
        return self.x, self.y

    # --- Rotation Methods ---
    def set_rotation(self, angle):
        """Set absolute rotation in degrees."""
        self.rotation = angle % 360

    def rotate(self, delta_angle):
        """Rotate relative to current rotation."""
        self.rotation = (self.rotation + delta_angle) % 360

    # --- Scale Methods ---
    def set_scale(self, scale_x, scale_y=None):
        """Set scale; if scale_y is None, uniform scaling is applied."""
        self.scale_x = scale_x
        self.scale_y = scale_y if scale_y is not None else scale_x

    def scale_by(self, factor_x, factor_y=None):
        """Scale relative to current scale."""
        self.scale_x *= factor_x
        self.scale_y *= factor_y if factor_y is not None else factor_x

    def get_scale(self):
        """Return current scale as a tuple (scale_x, scale_y)."""
        return self.scale_x, self.scale_y

    def debug_draw(self, surface, color=(255, 0, 0), size=10):
        """
        Draw a small cross at the object's position for debugging.

        Args:
            surface (pygame.Surface): The surface to draw on.
            color (tuple): RGB color of the debug marker.
            size (int): Half-length of the cross lines.
        """
        camera = self.game_object.scene.camera_component
        zoom = camera.zoom if camera else 1.0

        # Convert world → screen and apply zoom
        px, py = camera.world_to_screen(self.x, self.y)
        size = camera.scale_length(10) # scale the cross size

        # Draw horizontal line
        pygame.draw.line(surface, color, (px - size, py), (px + size, py), 2)
        # Draw vertical line
        pygame.draw.line(surface, color, (px, py - size), (px, py + size), 2)

    def debug_draw_rect(self, surface, width=50, height=50, color=(0, 255, 0)):
        """
        Draw a rectangle centred on the transform position.

        Args:
            surface (pygame.Surface): The surface to draw on.
            width (int): Width of rectangle.
            height (int): Height of rectangle.
            color (tuple): RGB colour.
        """
        camera = self.game_object.scene.camera_component
        rect_width = camera.scale_length(width)
        rect_height = camera.scale_length(height)
        rect = pygame.Rect(0, 0, rect_width, rect_height)
        rect.center = camera.world_to_screen(self.x, self.y)
        pygame.draw.rect(surface, color, rect, 2)

    def render(self, surface):
        self.debug_draw(surface)
        self.debug_draw_rect(surface)

    def __repr__(self):
        return f"<Transform x={self.x}, y={self.y}, rotation={self.rotation}, scale=({self.scale_x},{self.scale_y})>"
