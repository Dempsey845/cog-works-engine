import math
from component import Component


class Transform(Component):
    def __init__(self, x=0, y=0, rotation=0, scale_x=1, scale_y=1):
        """
        Transform component to track position, rotation, and scale of a GameObject.

        Args:
            x (float): X position in world space.
            y (float): Y position in world space.
            rotation (float): Rotation in degrees.
            scale_x (float): Scale along the X axis.
            scale_y (float): Scale along the Y axis.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale_x = scale_x
        self.scale_y = scale_y

    def set_world_position(self, x, y):
        """
        Set the world position of the Transform.

        Args:
            x (float): New X position.
            y (float): New Y position.
        """
        self.x = x
        self.y = y

    def get_world_position(self):
        """
        Get the world position of the Transform.

        Returns:
            tuple: (x, y) position in world space.
        """
        return self.x, self.y

    def set_rotation(self, degrees):
        """
        Set the rotation of the Transform in degrees.

        Args:
            degrees (float): Rotation angle in degrees.
        """
        self.rotation = degrees % 360  # Keep rotation within 0-359 degrees

    def get_world_rotation(self, radians=True):
        """
        Get the rotation of the Transform.

        Args:
            radians (bool): If True, returns rotation in radians; else in degrees.

        Returns:
            float: Rotation angle.
        """
        angle = self.rotation
        return math.radians(angle) if radians else angle

    def get_scale(self):
        """
        Get the scale of the Transform.

        Returns:
            tuple: (scale_x, scale_y)
        """
        return self.scale_x, self.scale_y

    def set_scale(self, sx, sy=None):
        """
        Set the scale of the Transform.

        Args:
            sx (float): Scale along X axis.
            sy (float, optional): Scale along Y axis. If None, Y scale = X scale.
        """
        self.scale_x = sx
        self.scale_y = sy if sy is not None else sx




