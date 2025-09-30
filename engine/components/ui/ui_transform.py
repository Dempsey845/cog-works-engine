import pygame
from engine.component import Component
from pygame_wrappers.window import Window


class UITransform(Component):
    """
    Defines the screen-space position and size of a UI element.
    Supports normalised (relative) or absolute coordinates.
    """

    def __init__(self, x=0.5, y=0.5, width=0.25, height=0.1,
                 anchor="center", relative=True, debug=False):
        """
        Args:
            x, y (float or int): Position of the element.
                - If relative=True, values are in [0.0–1.0] (fraction of screen).
                - If relative=False, values are absolute pixels.
            width, height (float or int): Size of the element.
                - If relative=True, values are fractions of screen size.
                - If relative=False, values are absolute pixels.
            anchor (str): Anchor point ('topleft', 'center', etc.).
            relative (bool): Whether to use relative (normalised) coordinates.
            debug (bool): If True, draw bounding box.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anchor = anchor
        self.relative = relative
        self.debug = debug
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update_rect()
        Window.get_instance().event_manager.subscribe(self.on_window_event)

    def on_window_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.update_rect()

    def update_rect(self):
        """Recalculate rect using position, size, and anchor, adapting to window size."""
        window = Window.get_instance()
        screen_w, screen_h = window.get_size()

        if self.relative:
            abs_x = int(self.x * screen_w)
            abs_y = int(self.y * screen_h)
            abs_w = int(self.width * screen_w)
            abs_h = int(self.height * screen_h)
        else:
            abs_x, abs_y, abs_w, abs_h = self.x, self.y, self.width, self.height

        self.rect.size = (abs_w, abs_h)

        # Apply the anchor
        if hasattr(self.rect, self.anchor):
            setattr(self.rect, self.anchor, (abs_x, abs_y))
        else:
            # default fallback
            self.rect.topleft = (abs_x, abs_y)

    def render(self, surface):
        if self.debug:
            pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)
