import pygame
from engine.components.ui.ui_transform import UITransform
from engine.components.ui.ui_renderer import UIRenderer

class UILabel(UIRenderer):
    """
    UILabel is a simple UI element for displaying text on the screen.

    Features:
        - Renders text at the position defined by the UITransform.
        - Supports custom font size, text colour, and optional background colour.
        - Text is automatically centered within the label's rectangle.
        - Can update text dynamically at runtime via `set_text`.
    """

    def __init__(self, text, font_size=24, color=(255,255,255), bg_color=None):
        """
        Initialise a UILabel component.

        Args:
            text (str): The text displayed by the label.
            font_size (int, optional): Size of the font (default: 24).
            color (tuple[int,int,int], optional): RGB colour of the text (default: white).
            bg_color (tuple[int,int,int] | None, optional): RGB background colour of the label.
                                                           If None, no background is drawn.
        """
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.bg_color = bg_color

    def set_text(self, new_text):
        """
        Update the label's text.

        Args:
            new_text (str): The new text to display.
        """
        self.text = new_text

    def render(self, surface):
        rect = self.game_object.get_component(UITransform).rect
        text_surf = self.font.render(self.text, True, self.color)
        if self.bg_color:
            pygame.draw.rect(surface, self.bg_color, rect)
        surface.blit(text_surf, text_surf.get_rect(center=rect.center))
