import pygame
from component import Component
from components.transform import Transform


class Sprite(Component):
    """
    Component for rendering an image on the screen.
    Requires a Transform component on the same GameObject.
    """

    def __init__(self, image_path: str):
        """
        Args:
            image_path (str): Path to the image file to render.
        """
        super().__init__()
        self.transform = None
        self.image_path = image_path
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def start(self):
        """
        Ensure the GameObject has a Transform component.
        """
        self.transform = self.game_object.get_component(Transform)
        if self.transform is None:
            # If no Transform exists, create one
            self.transform = Transform()
            self.game_object.add_component(self.transform)

    def update(self, dt: float):
        """
        Update the sprite's rect and apply rotation/scale.
        """
        # Apply scaling
        scaled_width = int(self.original_image.get_width() * self.transform.scale_x)
        scaled_height = int(self.original_image.get_height() * self.transform.scale_y)
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

        # Apply rotation
        self.image = pygame.transform.rotate(self.image, self.transform.rotation)
        self.rect = self.image.get_rect(center=(self.transform.x, self.transform.y))

    def render(self, surface):
        """
        Draw the sprite on the given surface.
        """
        surface.blit(self.image, self.rect.topleft)

    def change_image(self, new_image_path: str):
        """
        Change the sprite's image at runtime.

        Args:
            new_image_path (str): Path to the new image file.
        """
        self.image_path = new_image_path
        self.original_image = pygame.image.load(new_image_path).convert_alpha()
        # Update immediately for the next render
        self.update(0)
