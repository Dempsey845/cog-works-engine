import pygame

from engine.components.ui.ui_renderable import UIRenderable
from engine.components.ui.ui_transform import UITransform
from engine.game_object import GameObject
from pygame_wrappers.event_manager import EventManager
from pygame_wrappers.window import Window


class UIImage(GameObject):
    """
    A UI GameObject for rendering an image with optional background colour.
    Auto-updates size on window resize.
    """

    def __init__(self, image_path,
                 x=0.5, y=0.5,
                 width=0.2, height=0.2,
                 anchor="center",
                 relative=True, z_index=1):
        """
        Initialize a UIImage object.

        Args:
            image_path (str): Path to the image file.
            x (float): Horizontal position (0.0 to 1.0 if relative=True).
            y (float): Vertical position (0.0 to 1.0 if relative=True).
            width (float): Width (relative if relative=True, else pixels).
            height (float): Height (relative if relative=True, else pixels).
            anchor (str): Anchor point for positioning, e.g., 'center', 'topleft'.
            relative (bool): Whether position and size are relative to window size.
        """
        super().__init__(z_index=z_index)
        self.image_path = image_path
        self.anchor = anchor
        self.relative = relative
        self.width = width
        self.height = height

        # Transform (positioning & sizing)
        self.transform = UITransform(
            x=x, y=y,
            width=width, height=height,
            anchor=anchor,
            relative=relative,
            debug=True
        )
        self.add_component(self.transform)

        # Background or image rendering
        self.renderable = UIRenderable(
            image_path=image_path
        )
        self.add_component(self.renderable)

        # Subscribe to window resize events to maintain relative size
        EventManager.get_instance().subscribe(self.on_event)

        self.update_size()

    def update_size(self):
        if not self.renderable.original_image:
            return

        orig_w, orig_h = self.renderable.original_image.get_size()
        rect_w, rect_h = self.transform.rect.size

        # Fit image inside rect while keeping aspect ratio
        scale = min(rect_w / orig_w, rect_h / orig_h)
        new_w = max(1, int(orig_w * scale))
        new_h = max(1, int(orig_h * scale))

        # Always scale from original image
        self.renderable.scaled_image = pygame.transform.smoothscale(self.renderable.original_image, (new_w, new_h))

    def on_event(self, event):
        """Handle window resize events."""
        if event.type == pygame.VIDEORESIZE:
            self.update_size()
