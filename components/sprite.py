import pygame
from component import Component
from components.transform import Transform
from components.rigidbody2d import Rigidbody2D

class Sprite(Component):
    def __init__(self, image_path: str):
        """
        Sprite component to render an image associated with a GameObject.

        Args:
            image_path (str): Path to the image file.
        """
        super().__init__()
        self.image_path = image_path
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Original unscaled image
        self.image = self.original_image  # Current transformed image
        self.rect = self.image.get_rect()  # Rect for positioning and collision
        self.transform: Transform = None

    def start(self):
        """
        Initialise the component. Ensure the GameObject has a Transform,
        and if it has a Rigidbody2D, set its width/height to the sprite size
        if not already defined.
        """
        self.transform = self.game_object.get_component(Transform)
        if not self.transform:
            self.transform = Transform()
            self.game_object.add_component(self.transform)

        rb: Rigidbody2D = self.game_object.get_component(Rigidbody2D)
        if rb and (rb.width == 0 or rb.height == 0):
            rb.width = self.original_image.get_width()
            rb.height = self.original_image.get_height()

    def update(self, dt: float):
        """
        Update the sprite image every frame based on Transform scaling and rotation.

        Args:
            dt (float): Delta time (not used here but included for consistency).
        """
        if not self.transform:
            return

        # Apply Transform scale
        sx, sy = self.transform.get_scale()
        scaled_image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * sx), int(self.original_image.get_height() * sy))
        )

        # Apply Transform rotation (pygame rotates counter-clockwise)
        self.image = pygame.transform.rotate(scaled_image, -self.transform.rotation)

        # Update rect to match transformed image and center at Transform position
        self.rect = self.image.get_rect(center=(self.transform.x, self.transform.y))

    def render(self, surface):
        """
        Draw the sprite onto the given surface, considering camera zoom/position if available.

        Args:
            surface (pygame.Surface): The surface to render onto.
        """
        if not self.transform:
            return

        camera = getattr(self.game_object.scene, "camera_component", None)
        x, y = self.transform.get_world_position()
        img = self.image

        if camera:
            # Convert world position to screen coordinates
            x, y = camera.world_to_screen(x, y)
            # Apply camera zoom
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * camera.zoom), int(h * camera.zoom)))

        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect.topleft)

    def change_image(self, new_image_path: str):
        """
        Change the sprite image at runtime.

        Args:
            new_image_path (str): Path to the new image file.
        """
        self.image_path = new_image_path
        self.original_image = pygame.image.load(new_image_path).convert_alpha()
        self.update(0)  # Immediately update image to match current transform
