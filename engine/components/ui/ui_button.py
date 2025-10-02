import pygame
from engine.components.ui.ui_transform import UITransform
from engine.components.ui.ui_renderer import UIRenderer
from pygame_wrappers.event_manager import EventManager

class UIButton(UIRenderer):
    """
    UIButton is a simple interactive UI element that can be rendered on screen,
    respond to mouse hover, and trigger an action when clicked.

    Features:
        - Renders a rectangular button with text centered inside.
        - Highlights (brightens background) when hovered.
        - Supports a callback function to be executed on click.
    """

    def __init__(self, text, on_click=None, font_size=24, text_color=(255,255,255), bg_color=(0,0,255)):
        """
        Initialise a UIButton component.

        Args:
            text (str): The text displayed on the button.
            on_click (callable, optional): A function to call when the button is clicked.
                                           It will receive the button's game_object as an argument.
            font_size (int, optional): Size of the text font (default: 24).
            text_color (tuple[int,int,int], optional): RGB colour of the text (default: white).
            bg_color (tuple[int,int,int], optional): RGB background colour of the button (default: blue).
        """
        super().__init__()
        self.text = text
        self.on_click = on_click
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.hovered = False

        # Subscribe to global event manager to handle mouse events
        EventManager.get_instance().subscribe(self.handle_event)

    def handle_event(self, event):
        rect = self.game_object.get_component(UITransform).rect
        if event.type == pygame.MOUSEMOTION:
            self.hovered = rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered and self.on_click:
            self.on_click(self.game_object)

    def render(self, surface):
        rect = self.game_object.get_component(UITransform).rect
        color = tuple(min(c+50,255) if self.hovered else c for c in self.bg_color)
        pygame.draw.rect(surface, color, rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surf, text_surf.get_rect(center=rect.center))

    def on_destroy(self):
        EventManager.get_instance().unsubscribe(self.handle_event)