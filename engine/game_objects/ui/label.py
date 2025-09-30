import pygame

from engine.components.ui.ui_renderable import UIRenderable
from engine.components.ui.ui_text import UIText
from engine.components.ui.ui_transform import UITransform
from engine.game_object import GameObject
from pygame_wrappers.event_manager import EventManager
from pygame_wrappers.window import Window


class Label(GameObject):
    """
    A simple UI label GameObject for rendering text, with optional background.
    Auto-updates size on window resize.
    """

    def __init__(self, text,
                 x=0.5, y=0.5,
                 anchor="center",
                 text_size=24,
                 bg_color=None,
                 border_radius=15,
                 relative=True,
                 padding=10,
                 halign="center",
                 valign="center"):
        """
        Initialize a Label object.

        Args:
            text (str): The text to display in the label.
            x (float): Horizontal position of the label (0.0 to 1.0 if relative=True).
            y (float): Vertical position of the label (0.0 to 1.0 if relative=True).
            anchor (str): Anchor point for positioning, e.g., 'center', 'top-left'.
            text_size (int): Font size of the text.
            bg_color (tuple or None): Background colour as (R, G, B), or None for transparent.
            border_radius (int): Corner radius of the background rectangle.
            relative (bool): Whether position and size are relative to window size.
            padding (int): Padding around text inside the label, in pixels.
            halign (str): Horizontal alignment of text ('left', 'center', 'right').
            valign (str): Vertical alignment of text ('top', 'center', 'bottom').
        """
        super().__init__()
        self.text = text
        self.text_size = text_size
        self.bg_color = bg_color
        self.border_radius = border_radius
        self.anchor = anchor
        self.relative = relative
        self.padding = padding
        self.halign = halign
        self.valign = valign

        # Transform (positioning & sizing)
        width, height = self.calculate_size()
        self.transform = UITransform(
            x=x, y=y,
            width=width, height=height,
            anchor=anchor,
            relative=relative
        )
        self.add_component(self.transform)

        # Background rendering
        if bg_color:
            self.renderable = UIRenderable(
                bg_color=bg_color,
                border_radius=border_radius
            )
            self.add_component(self.renderable)

        # Text rendering with alignment
        self.text_component = UIText(text, size=text_size, halign=halign, valign=valign)
        self.add_component(self.text_component)

        # Subscribe to window resize events
        EventManager.get_instance().subscribe(self.on_event)

    def calculate_size(self):
        """Calculate width and height relative to current window size."""
        screen_w, screen_h = Window.get_instance().get_size()
        width = (len(self.text) * self.text_size + self.padding * 2) / screen_w
        height = (self.text_size * 1.2 + self.padding * 2) / screen_h
        return width, height

    def update_size(self):
        """Update the transform size to fit text + padding."""
        self.transform.width, self.transform.height = self.calculate_size()
        self.transform.update_rect()  # make sure the UITransform updates its rect

    def on_event(self, event):
        """Handle events from EventManager."""
        if event.type == pygame.VIDEORESIZE:
            self.update_size()
