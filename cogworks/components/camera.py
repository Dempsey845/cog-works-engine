from cogworks.component import Component
from cogworks.pygame_wrappers.event_manager import EventManager
from cogworks.pygame_wrappers.window import Window


class Camera(Component):
    def __init__(self):
        super().__init__()
        self.offset_x = 0
        self.offset_y = 200
        self.zoom = 1.0  # 1.0 = normal, <1.0 = zoom out, >1.0 = zoom in
        self.surface_width, self.surface_height = Window.get_instance().get_size()

        # Subscribe to window resize events
        EventManager.get_instance().subscribe(self.handle_window_event)

    def handle_window_event(self, event):
        """Update surface size on window resize."""
        import pygame
        if event.type == pygame.VIDEORESIZE:
            self.surface_width = event.w
            self.surface_height = event.h

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

    def is_visible(self, x: float, y: float, width: float, height: float,
                   tolerance: float = None) -> bool:
        """
        Determine if a rectangle (sprite) is visible on the camera surface.

        Args:
            x (float): World X position of the sprite center.
            y (float): World Y position of the sprite center.
            width (float): Width of the sprite after scaling/zoom.
            height (float): Height of the sprite after scaling/zoom.
            tolerance (float, optional): Extra buffer in pixels to consider visible. If None, calculated dynamically.

        Returns:
            bool: True if the sprite is (partially) visible on camera, False if completely outside.
        """
        # Automatically set tolerance based on size if not provided
        if tolerance is None:
            max_dim = max(width, height)
            if max_dim > 200:  # threshold for "large" objects
                tolerance = max_dim * 0.5
            else:
                tolerance = 10

        # Calculate axis-aligned bounding box
        left = (x - width / 2 - self.offset_x) * self.zoom
        right = (x + width / 2 - self.offset_x) * self.zoom
        top = (y - height / 2 - self.offset_y) * self.zoom
        bottom = (y + height / 2 - self.offset_y) * self.zoom

        # Return True if any part is on screen, accounting for tolerance
        return not (right < -tolerance or left > self.surface_width + tolerance or
                    bottom < -tolerance or top > self.surface_height + tolerance)
