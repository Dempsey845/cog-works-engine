import pygame
from component import Component
from components.ui.ui_transform import UITransform


class UIText(Component):
    """
    Displays text inside a UI element.
    """

    def __init__(self, text="", font_name="Arial", size=20, color=(255, 255, 255)):
        super().__init__()
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont(self.font_name, self.size)
        self.surface = None
        self.rect = None

    def set_text(self, text: str):
        """Update the displayed text and re-render the surface."""
        self.text = text
        self.surface = None  # force re-render on next render

    def render(self, surface):
        if not self.active:
            return

        if self.surface is None:
            self.surface = self.font.render(self.text, True, self.color)

        if self.game_object:
            transform = self.game_object.get_component(UITransform)
            if transform:
                # Center text within transform rect
                self.rect = self.surface.get_rect(center=transform.rect.center)
                surface.blit(self.surface, self.rect)
