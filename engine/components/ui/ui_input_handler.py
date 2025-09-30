import pygame
from engine.component import Component
from engine.components.ui.ui_transform import UITransform
from pygame_wrappers.event_manager import EventManager


class UIInputHandler(Component):
    """
    Handles mouse input events for a UI element (hover, click, release).
    """

    def __init__(self, on_click=None, on_hover=None, on_hover_exit=None, on_release=None):
        super().__init__()
        self.on_click = on_click
        self.on_hover = on_hover
        self.on_hover_exit = on_hover_exit
        self.on_release = on_release

        self.is_hovered = False
        self.is_pressed = False

    def start(self):
        # Subscribe to EventManager
        EventManager.get_instance().subscribe(self.handle_event)

    def on_remove(self):
        # Unsubscribe when component is removed
        EventManager.get_instance().unsubscribe(self.handle_event)

    def handle_event(self, event):
        if not self.active or not self.game_object:
            return

        transform = self.game_object.get_component(UITransform)
        if not transform:
            return

        rect = transform.rect
        mouse_pos = pygame.mouse.get_pos()

        # Hover detection
        if rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                self.is_hovered = True
                if self.on_hover:
                    self.on_hover(self.game_object)
        else:
            if self.is_hovered:
                if self.on_hover_exit:
                    self.on_hover_exit(self.game_object)
            self.is_hovered = False

        # Click handling
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(mouse_pos):
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and rect.collidepoint(mouse_pos):
                if self.on_click:
                    self.on_click(self.game_object)

            if self.is_pressed and self.on_release:
                self.on_release(self.game_object)

            self.is_pressed = False
