import pygame
from engine.component import Component
from engine.components.ui.ui_transform import UITransform
from engine.utils.asset_loader import load_user_image, load_engine_image


class UIRenderable(Component):
    """
    Renders a background (solid colour or image) for a UI element.
    """

    def __init__(self, bg_color=(50, 50, 50), border_radius=0, image_path=None, z_index=1, from_engine=False):
        """
        Args:
            bg_color (tuple): Background colour if no image is given.
            border_radius (int): Optional rounded corners.
            image_path (str): Relative path to image (either user asset or engine asset).
            z_index (int): Render order.
            from_engine (bool): If True, loads from engine assets. Otherwise, loads from user assets.
        """
        super().__init__()
        self.bg_color = bg_color
        self.border_radius = border_radius
        self.z_index = z_index

        self.transform = None
        self.original_image = None
        self.scaled_image = None

        if image_path is not None:
            if from_engine:
                self.original_image = load_engine_image(image_path)
            else:
                self.original_image = load_user_image(image_path)
            self.scaled_image = self.original_image

    def render(self, surface):
        if not self.active or not self.game_object:
            return

        self.transform = self.game_object.get_component(UITransform)
        if not self.transform:
            return

        rect = self.transform.rect

        if self.scaled_image:
            # Center the image in the rect
            pos_x = rect.x + (rect.width - self.scaled_image.get_width()) // 2
            pos_y = rect.y + (rect.height - self.scaled_image.get_height()) // 2
            surface.blit(self.scaled_image, (pos_x, pos_y))
        else:
            pygame.draw.rect(surface, self.bg_color, rect, border_radius=self.border_radius)
