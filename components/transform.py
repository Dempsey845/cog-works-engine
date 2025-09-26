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
        """Set local position relative to parent."""
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Move relative to current local position."""
        self.x += dx
        self.y += dy

    def get_position(self, world=False):
        """
        Return current position as a tuple (x, y).
        If world=True, returns global position including parent transforms.
        """
        if world and self.game_object and self.game_object.parent:
            px, py = self.game_object.parent.transform.get_position(world=True)
            return self.x + px, self.y + py
        return self.x, self.y

    def set_world_position(self, world_x, world_y):
        """Set position in world space; converts to local coordinates."""
        if self.game_object.parent:
            px, py = self.game_object.parent.get_world_position()
            self.x = world_x - px
            self.y = world_y - py
        else:
            self.x = world_x
            self.y = world_y

    def get_world_position(self):
        """
        Calculate absolute position from transform and parents.
        """
        x, y = self.x, self.y
        parent = getattr(self.game_object, "parent", None)
        while parent:
            parent_transform = parent.get_component(Transform)
            if parent_transform:
                x += parent_transform.x
                y += parent_transform.y
            parent = getattr(parent, "parent", None)
        return x, y

    # --- Rotation Methods ---
    def set_rotation(self, angle):
        """Set absolute local rotation in degrees."""
        self.rotation = angle % 360

    def rotate(self, delta_angle):
        """Rotate relative to current local rotation."""
        self.rotation = (self.rotation + delta_angle) % 360

    def get_rotation(self, world=False):
        """
        Return rotation in degrees.
        If world=True, includes parent rotations.
        """
        if world and self.game_object and self.game_object.parent:
            parent_rot = self.game_object.parent.transform.get_rotation(world=True)
            return (self.rotation + parent_rot) % 360
        return self.rotation

    # --- Scale Methods ---
    def set_scale(self, scale_x, scale_y=None):
        """Set local scale; if scale_y is None, uniform scaling is applied."""
        self.scale_x = scale_x
        self.scale_y = scale_y if scale_y is not None else scale_x

    def scale_by(self, factor_x, factor_y=None):
        """Scale relative to current local scale."""
        self.scale_x *= factor_x
        self.scale_y *= factor_y if factor_y is not None else factor_x

    def get_scale(self, world=False):
        """
        Return scale as a tuple (scale_x, scale_y).
        If world=True, includes parent scales.
        """
        if world and self.game_object and self.game_object.parent:
            parent_sx, parent_sy = self.game_object.parent.transform.get_scale(world=True)
            return self.scale_x * parent_sx, self.scale_y * parent_sy
        return self.scale_x, self.scale_y

    # --- Debug Methods ---
    def debug_draw(self, surface, color=(255, 0, 0), size=10):
        """
        Draw a small cross at the object's position for debugging.

        Args:
            surface (pygame.Surface): The surface to draw on.
            color (tuple): RGB color of the debug marker.
            size (int): Half-length of the cross lines.
        """
        if not self.game_object.scene or not self.game_object.scene.camera_component:
            return  # nothing to draw

        camera = self.game_object.scene.camera_component

        # Convert world → screen and apply zoom
        px, py = camera.world_to_screen(*self.get_position(world=True))
        size = camera.scale_length(size)  # scale the cross size

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
        if not self.game_object.scene or not self.game_object.scene.camera_component:
            return  # nothing to draw
        camera = self.game_object.scene.camera_component
        rect_width = camera.scale_length(width)
        rect_height = camera.scale_length(height)
        rect = pygame.Rect(0, 0, rect_width, rect_height)
        rect.center = camera.world_to_screen(*self.get_position(world=True))
        pygame.draw.rect(surface, color, rect, 2)

    def render(self, surface):
        self.debug_draw(surface)
        self.debug_draw_rect(surface)

    def __repr__(self):
        return (f"<Transform x={self.x}, y={self.y}, rotation={self.rotation}, "
                f"scale=({self.scale_x},{self.scale_y})>")
