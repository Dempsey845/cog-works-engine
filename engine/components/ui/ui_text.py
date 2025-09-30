import pygame
from engine.component import Component
from engine.components.ui.ui_transform import UITransform


class UIText(Component):
    """
    Displays text inside a UI element.
    """

    def __init__(self, text="", font_name="Arial", size=20, color=(255, 255, 255), halign="center", valign="center"):
        super().__init__()
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont(self.font_name, self.size)
        self.surface = None
        self.rect = None
        self.halign=halign
        self.valign=valign

    def set_text(self, text: str):
        """Update the displayed text and re-render the surface."""
        self.text = text
        self.surface = None  # force re-render on next render

    def update_size(self, new_size: int):
        """Update the font size and re-render the text surface."""
        self.size = new_size
        self.font = pygame.font.SysFont(self.font_name, self.size)
        self.surface = None  # force re-render

    def render(self, surface):
        if not self.active:
            return

        if self.surface is None:
            self.surface = self.font.render(self.text, True, self.color)

        if self.game_object:
            transform = self.game_object.get_component(UITransform)
            if transform:
                # Apply padding (if present)
                padding = getattr(self.game_object, "padding", 0)
                padded_rect = transform.rect.inflate(-padding * 2, -padding * 2)

                self.rect = self.surface.get_rect()

                # Horizontal alignment
                if self.halign == "left":
                    self.rect.midleft = padded_rect.midleft
                elif self.halign == "right":
                    self.rect.midright = padded_rect.midright
                else:  # default center
                    self.rect.centerx = padded_rect.centerx

                # Vertical alignment
                if self.valign == "top":
                    self.rect.midtop = padded_rect.midtop
                elif self.valign == "bottom":
                    self.rect.midbottom = padded_rect.midbottom
                else:  # default center
                    self.rect.centery = padded_rect.centery

                surface.blit(self.surface, self.rect)

