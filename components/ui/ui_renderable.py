import pygame
from component import Component
from components.ui.ui_transform import UITransform


class UIRenderable(Component):
    """
    Renders a background (solid colour or image) for a UI element.
    """

    def __init__(self, bg_color=(50, 50, 50), border_radius=0, image=None, z_index=0):
        super().__init__()
        self.bg_color = bg_color
        self.border_radius = border_radius
        self.image = image
        self.z_index = z_index

        if isinstance(image, str):
            self.image = pygame.image.load(image).convert_alpha()

    def render(self, surface):
        if not self.active:
            return

        if self.game_object:
            transform = self.game_object.get_component(UITransform)
            if not transform:
                return

            rect = transform.rect

            if self.image:
                # scale image to fit rect
                scaled_img = pygame.transform.smoothscale(self.image, (rect.width, rect.height))
                surface.blit(scaled_img, rect.topleft)
            else:
                # draw a filled rectangle
                pygame.draw.rect(surface, self.bg_color, rect, border_radius=self.border_radius)