import pygame
from cogworks.components.ui.ui_transform import UITransform
from cogworks.components.ui.ui_renderer import UIRenderer
from cogworks.utils.asset_loader import load_engine_image, load_user_image


class UIImage(UIRenderer):
    """
    UIImage is a UI component for rendering images within a defined rectangle.

    Features:
        - Loads images either from cogworks assets or user-provided files.
        - Automatically scales the image to fit inside the UITransform's rect
          while preserving aspect ratio (no stretching).
        - Centers the image inside its assigned rect.
        - Supports swapping the image dynamically at runtime.
    """

    def __init__(self, image_path, load_engine=False):
        """
        Initialise a UIImage component.

        Args:
            image_path (str): Path to the image file.
            load_engine (bool, optional): If True, loads from cogworks assets.
                                          If False, loads from user assets. (default: False)
        """
        super().__init__()
        self.image = load_engine_image(image_path) if load_engine else load_user_image(image_path)

    def set_image(self, image_path, load_engine=False):
        """
        Change the image displayed by this UIImage at runtime.

        Args:
            image_path (str): Path to the new image file.
            load_engine (bool, optional): If True, loads from cogworks assets.
                                          If False, loads from user assets. (default: False)

        Example:
            ui_image.set_image("icons/new_icon.png")
        """
        self.image = load_engine_image(image_path) if load_engine else load_user_image(image_path)

    def render(self, surface):
        rect = self.game_object.get_component(UITransform).rect
        # Original image size
        iw, ih = self.image.get_size()
        # Compute scale factors
        scale_w = rect.width / iw
        scale_h = rect.height / ih
        # Use the smaller scale to fit inside rect without stretching
        scale = min(scale_w, scale_h)
        new_size = (int(iw * scale), int(ih * scale))
        img = pygame.transform.scale(self.image, new_size)

        # Center the image inside rect
        img_rect = img.get_rect(center=rect.center)
        surface.blit(img, img_rect)
