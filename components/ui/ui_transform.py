import pygame
from component import Component


class UITransform(Component):
    """
    Defines the screen-space position and size of a UI element.
    """

    def __init__(self, x=0, y=0, width=100, height=50, anchor="topleft", debug=False):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anchor = anchor  # e.g. "topleft", "center", "bottomright"
        self.debug = debug
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.update_rect()

    def update_rect(self):
        """Recalculate the rect using position, size, and anchor."""
        self.rect.size = (self.width, self.height)

        # Apply the anchor
        if hasattr(self.rect, self.anchor):
            setattr(self.rect, self.anchor, (self.x, self.y))
        else:
            # default fallback
            self.rect.topleft = (self.x, self.y)

    def render(self, surface):
        # Debug: show rect bounds
        if not self.debug:
            return
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)

