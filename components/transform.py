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

    def __repr__(self):
        return f"<Transform x={self.x}, y={self.y}, rotation={self.rotation}, scale=({self.scale_x},{self.scale_y})>"
