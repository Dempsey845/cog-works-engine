from component import Component


class Camera(Component):
    def __init__(self):
        super().__init__()
        self.offset_x = 0
        self.offset_y = 200
        self.zoom = 1.0  # 1.0 = normal, <1.0 = zoom out, >1.0 = zoom in

    def move(self, dx, dy):
        """Move the camera by a given delta."""
        self.offset_x += dx
        self.offset_y += dy

    def set_zoom(self, zoom: float):
        """Set the camera zoom level."""
        if zoom <= 0:
            raise ValueError("Zoom must be greater than 0")
        self.zoom = zoom

    def world_to_screen(self, x, y):
        """Convert world coordinates to screen coordinates based on offset and zoom."""
        screen_x = (x - self.offset_x) * self.zoom
        screen_y = (y - self.offset_y) * self.zoom
        return screen_x, screen_y

    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates back to world coordinates considering zoom and offset."""
        world_x = screen_x / self.zoom + self.offset_x
        world_y = screen_y / self.zoom + self.offset_y
        return world_x, world_y

    def scale_length(self, length: float) -> float:
        """Scale a size/length according to the zoom level."""
        return length * self.zoom

    def center_on(self, x, y, screen_width, screen_height):
        """
        Center the camera on a world position, taking zoom into account.
        """
        self.offset_x = x - (screen_width / 2) / self.zoom
        self.offset_y = y - (screen_height / 2) / self.zoom
