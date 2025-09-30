import pygame
from engine.components.ui.ui_input_handler import UIInputHandler
from engine.components.ui.ui_renderable import UIRenderable
from engine.components.ui.ui_text import UIText
from engine.components.ui.ui_transform import UITransform
from engine.game_object import GameObject
from pygame_wrappers.window import Window
from pygame_wrappers.event_manager import EventManager


class Button(GameObject):
    """
        A reusable UI button GameObject that supports text, background,
        hover effects, and click handling.
    """
    def __init__(self, text, on_click,
                 width=0.25, height=0.1,
                 x=0.5, y=0.5,
                 anchor="center",
                 bg_color=(0, 0, 255),
                 hover_color=(50, 50, 255),
                 border_radius=16,
                 text_size=24,
                 min_text_size=10, max_text_size=48,
                 min_width=80, min_height=40,
                 max_width=600, max_height=200,
                 relative=True,
                 padding=10,
                 auto_resize_text=True,
                 text_halign="center",
                 text_valign="center"):
        """
        Initialise a Button object.

        Args:
            text (str): The text to display on the button.
            on_click (Callable): Function to call when the button is clicked.
            width (float): Button width (relative to screen if relative=True).
            height (float): Button height (relative to screen if relative=True).
            x (float): X position (relative or absolute depending on `relative`).
            y (float): Y position (relative or absolute depending on `relative`).
            anchor (str): The anchor for the button.
            bg_color (tuple[int, int, int]): Default background colour in RGB.
            hover_color (tuple[int, int, int]): Background colour when hovered.
            border_radius (int): Corner radius for the button background.
            text_size (int): Font size of the button label.
            relative (bool): Whether size/position are relative to screen.
            padding (int): Padding for the button.
            auto_resize_text (bool): Whether text should be automatically resized.
            text_halign (str): Horizontal alignment of text ('left', 'center', 'right').
            text_valign (str): Vertical alignment of text ('top', 'center', 'bottom').
        """
        super().__init__()

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text
        self.relative = relative
        self.relative_width = width
        self.relative_height = height

        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height

        self.min_text_size = min_text_size
        self.max_text_size = max_text_size

        self.padding = padding
        self.auto_resize_text = auto_resize_text
        self.text_halign = text_halign
        self.text_valign = text_valign

        # Transform
        self.transform = UITransform(
            x=x, y=y, width=width, height=height,
            anchor=anchor, relative=relative
        )
        self.add_component(self.transform)

        # Background
        self.renderable = UIRenderable(bg_color=self.bg_color, border_radius=border_radius)
        self.add_component(self.renderable)

        # Text
        initial_size = self.calculate_text_size() if auto_resize_text else text_size
        self.text_component = UIText(text, size=initial_size, halign=text_halign, valign=text_valign)
        self.add_component(self.text_component)

        # Input
        self.add_component(UIInputHandler(
            on_click=on_click,
            on_hover=self._on_hover,
            on_hover_exit=self._on_hover_exit
        ))

        # Apply initial clamping
        self._clamp_size_and_text()

        # Subscribe to window resize
        EventManager.get_instance().subscribe(self.on_event)

    def _clamp_size_and_text(self):
        """Clamp button and text size to min/max constraints."""
        screen_w, screen_h = Window.get_instance().get_size()
        transform = self.transform

        w = transform.width * screen_w if self.relative else transform.width
        h = transform.height * screen_h if self.relative else transform.height

        w = max(self.min_width, min(self.max_width, w))
        h = max(self.min_height, min(self.max_height, h))

        transform.width = w / screen_w if self.relative else w
        transform.height = h / screen_h if self.relative else h
        transform.update_rect()

        if self.auto_resize_text:
            self.update_text_size()

    def calculate_text_size(self):
        """Compute font size that fits inside the button."""
        screen_w, screen_h = Window.get_instance().get_size()
        button_w = self.transform.width * screen_w if self.relative else self.transform.width
        button_h = self.transform.height * screen_h if self.relative else self.transform.height

        size = self.max_text_size
        while size > self.min_text_size:
            text_width = len(self.text) * size * 0.6
            text_height = size * 1.2
            if text_width + self.padding * 2 <= button_w and text_height + self.padding * 2 <= button_h:
                break
            size -= 1
        return max(self.min_text_size, min(self.max_text_size, size))

    def update_text_size(self):
        self.text_component.update_size(self.calculate_text_size())

    def on_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self._clamp_size_and_text()

    def _on_hover(self, *_):
        self.renderable.bg_color = self.hover_color

    def _on_hover_exit(self, *_):
        self.renderable.bg_color = self.bg_color
