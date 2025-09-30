import math
from component import Component


class Transform(Component):
    """
    Transform component to track position, rotation, and scale of a GameObject.

    Supports both local (relative to parent) and world (absolute) transforms.

    Attributes:
        local_x (float): Local X position relative to parent.
        local_y (float): Local Y position relative to parent.
        local_rotation (float): Local rotation in degrees relative to parent.
        local_scale_x (float): Local scale along X axis.
        local_scale_y (float): Local scale along Y axis.
    """

    def __init__(self, x=0, y=0, rotation=0, scale_x=1, scale_y=1):
        super().__init__()
        # Local transform (relative to parent)
        self.local_x = x
        self.local_y = y
        self.local_rotation = rotation
        self.local_scale_x = scale_x
        self.local_scale_y = scale_y

    def reset_to_start(self):
        if self.game_object.uuid in self.game_object.scene.start_states:
            state = self.game_object.scene.start_states[self.game_object.uuid]
            self.set_local_position(state["local_x"], state["local_y"])
            self.set_local_rotation(state["local_rotation"])
            self.set_local_scale(state["local_scale_x"], state["local_scale_y"])

    # --- Local setters ---
    def set_local_position(self, x, y):
        """
        Set the local position of the Transform relative to parent.

        Args:
            x (float): Local X position.
            y (float): Local Y position.
        """
        self.local_x = x
        self.local_y = y

    def get_local_position(self):
        """
        Get the local position of the Transform relative to parent.

        Returns:
            tuple: (x, y) local position.
        """
        return self.local_x, self.local_y

    def set_local_rotation(self, degrees):
        """
        Set the local rotation of the Transform relative to parent.

        Args:
            degrees (float): Rotation angle in degrees.
        """
        self.local_rotation = degrees % 360

    def get_local_rotation(self, radians=True):
        """
        Get the local rotation of the Transform.

        Args:
            radians (bool): If True, returns rotation in radians; else in degrees.

        Returns:
            float: Rotation angle.
        """
        return math.radians(self.local_rotation) if radians else self.local_rotation

    def set_local_scale(self, sx, sy=None):
        """
        Set the local scale of the Transform relative to parent.

        Args:
            sx (float): Scale along X axis.
            sy (float, optional): Scale along Y axis. If None, Y scale = X scale.
        """
        self.local_scale_x = sx
        self.local_scale_y = sy if sy is not None else sx

    def get_local_scale(self):
        """
        Get the local scale of the Transform.

        Returns:
            tuple: (scale_x, scale_y)
        """
        return self.local_scale_x, self.local_scale_y

    # --- World setters ---
    def set_world_position(self, x, y):
        """
        Set the world position of the Transform.

        Converts world coordinates to local if the GameObject has a parent.

        Args:
            x (float): World X position.
            y (float): World Y position.
        """
        if self.game_object and self.game_object.parent:
            px, py = self.game_object.parent.transform.get_world_position()
            self.local_x = x - px
            self.local_y = y - py
        else:
            self.local_x = x
            self.local_y = y

    def set_world_rotation(self, degrees):
        """
        Set the world rotation of the Transform.

        Converts world rotation to local rotation if the GameObject has a parent.

        Args:
            degrees (float): Rotation angle in degrees.
        """
        if self.game_object and self.game_object.parent:
            parent_rotation = self.game_object.parent.transform.get_world_rotation(radians=False)
            self.local_rotation = (degrees - parent_rotation) % 360
        else:
            self.local_rotation = degrees % 360

    def set_world_scale(self, sx, sy=None):
        """
        Set the world scale of the Transform.

        Converts world scale to local scale if the GameObject has a parent.

        Args:
            sx (float): Scale along X axis.
            sy (float, optional): Scale along Y axis. If None, Y scale = X scale.
        """
        if self.game_object and self.game_object.parent:
            psx, psy = self.game_object.parent.transform.get_world_scale()
            self.local_scale_x = sx / psx
            self.local_scale_y = (sy / psy) if sy is not None else (sx / psx)
        else:
            self.local_scale_x = sx
            self.local_scale_y = sy if sy is not None else sx

    # --- World getters ---
    def get_world_position(self):
        """
        Get the world position of the Transform.

        Returns:
            tuple: (x, y) position in world space.
        """
        if self.game_object and self.game_object.parent:
            px, py = self.game_object.parent.transform.get_world_position()
            return px + self.local_x, py + self.local_y
        return self.local_x, self.local_y

    def get_world_rotation(self, radians=True):
        """
        Get the world rotation of the Transform.

        Returns:
            float: Rotation angle in radians or degrees.
        """
        angle = self.local_rotation
        if self.game_object and self.game_object.parent:
            angle += self.game_object.parent.transform.get_world_rotation(radians=False)
        return math.radians(angle) if radians else angle

    def get_world_scale(self):
        """
        Get the world scale of the Transform.

        Returns:
            tuple: (scale_x, scale_y)
        """
        sx, sy = self.local_scale_x, self.local_scale_y
        if self.game_object and self.game_object.parent:
            psx, psy = self.game_object.parent.transform.get_world_scale()
            return sx * psx, sy * psy
        return sx, sy