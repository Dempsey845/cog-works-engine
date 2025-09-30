from engine.components.ui.ui_input_handler import UIInputHandler
from engine.components.ui.ui_renderable import UIRenderable
from engine.components.ui.ui_text import UIText
from engine.components.ui.ui_transform import UITransform
from engine.game_object import GameObject


class Button(GameObject):
    """
    A reusable UI button GameObject that supports text, background,
    hover effects, and click handling.

    Attributes:
        bg_color (tuple): Default background colour (R, G, B).
        hover_color (tuple): Background colour when hovered.
        renderable (UIRenderable): The renderable component for the button background.
    """

    def __init__(self, text, on_click,
                 width=0.25, height=0.1,
                 x=0.5, y=0.5,
                 anchor="center",
                 bg_color=(0, 0, 255),
                 hover_color=(50, 50, 255),
                 border_radius=16,
                 text_size=24,
                 relative=True):
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
        """
        super().__init__()

        self.bg_color = bg_color
        self.hover_color = hover_color

        # Transform (positioning & sizing)
        self.add_component(UITransform(
            x=x, y=y,
            width=width, height=height,
            anchor=anchor, relative=relative
        ))

        # Background rendering
        self.renderable = UIRenderable(
            bg_color=self.bg_color,
            border_radius=border_radius
        )
        self.add_component(self.renderable)

        # Text rendering
        self.add_component(UIText(
            text,
            size=text_size
        ))

        # Input handling (click + hover)
        self.add_component(UIInputHandler(
            on_click=on_click,
            on_hover=self._on_hover,
            on_hover_exit=self._on_hover_exit
        ))

    def _on_hover(self, *_):
        """
        Change button background to hover colour when the mouse enters.
        """
        self.renderable.bg_color = self.hover_color

    def _on_hover_exit(self, *_):
        """
        Reset button background to default colour when the mouse exits.
        """
        self.renderable.bg_color = self.bg_color
