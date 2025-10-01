import pygame
from engine.component import Component
from engine.components.linebody2d import LineBody2D
from engine.components.transform import Transform
from engine.components.rigidbody2d import Rigidbody2D
from engine.utils.asset_loader import load_user_image


class Sprite(Component):
    def __init__(self, image_path: str):
        """
        Sprite component to render an image associated with a GameObject.

        Args:
            image_path (str): Path to the image file (inside 'assets' folder).
        """
        super().__init__()
        self.image_path = image_path
        self.original_image = load_user_image(image_path)
        self.image = self.original_image  # Current transformed image
        self.rect = self.image.get_rect()  # Rect for positioning and collision
        self.transform: Transform = None
        self._last_transform_state = None  # Cache to detect Transform changes

    def start(self):
        self.transform = self.game_object.get_component(Transform)
        if not self.transform:
            self.transform = Transform()
            self.game_object.add_component(self.transform)

        # Box rigidbody config
        rb: Rigidbody2D = self.game_object.get_component(Rigidbody2D)
        if rb and (rb.width == 0 or rb.height == 0):
            # Use unscaled image size for collider
            rb.width = self.original_image.get_width()
            rb.height = self.original_image.get_height()


        # Line rigidbody config
        lb: LineBody2D = self.game_object.get_component(LineBody2D)
        if lb and lb.point_a == (0, 0) and lb.point_b == (0, 0):
            # Initialise the line points scaled to the current transform
            half_width = (self.original_image.get_width() / 2) * self.transform.local_scale_x
            lb.point_a = (-half_width, 0)
            lb.point_b = (half_width, 0)

        # Apply the transform once on start
        self._apply_transform()

    def _apply_transform(self):
        """
        Internal: rebuild the sprite image if scale/rotation changed
        """
        sx, sy = self.transform.get_local_scale()
        angle = -self.transform.local_rotation  # rotate counter-clockwise

        # Apply rotozoom (rotation + scale combined)
        avg_scale = (sx + sy) / 2 if (sx != sy) else sx
        self.image = pygame.transform.rotozoom(self.original_image, angle, avg_scale)

        # Update rect to match transformed image and center at Transform position
        self.rect = self.image.get_rect(center=(self.transform.local_x, self.transform.local_y))

        # Store the state so we don't re-transform unnecessarily
        self._last_transform_state = (sx, sy, self.transform.local_rotation)

    def update(self, dt: float):
        if not self.transform:
            return

        # Current state
        sx, sy = self.transform.get_local_scale()
        state = (sx, sy, self.transform.local_rotation)

        # Only update if something actually changed
        if state != self._last_transform_state:
            self._apply_transform()

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
        self.original_image = load_user_image(new_image_path)
        self._apply_transform()  # Immediately apply to match current transform

    def get_width(self, transform: 'Transform' = None) -> float:
        """
        Returns the width of the sprite, scaled by the provided transform or the sprite's own transform.

        Args:
            transform (Transform, optional): An optional transform to use for scaling.
                If not provided, the sprite's own transform is used.

        Raises:
            ReferenceError: If no transform is provided and the sprite does not have its own transform.

        Returns:
            float: The scaled width of the sprite image.
        """
        scale_x = self._get_scale(transform, 'x')
        return self.image.get_width() * scale_x

    def get_image_width(self) -> int:
        """
        Returns the unscaled width of the sprite image.

        Returns:
            int: The width of the image in pixels.
        """
        return self.image.get_width()

    def get_height(self, transform: 'Transform' = None) -> float:
        """
        Returns the height of the sprite, scaled by the provided transform or the sprite's own transform.

        Args:
            transform (Transform, optional): An optional transform to use for scaling.
                If not provided, the sprite's own transform is used.

        Raises:
            ReferenceError: If no transform is provided and the sprite does not have its own transform.

        Returns:
            float: The scaled height of the sprite image.
        """
        scale_y = self._get_scale(transform, 'y')
        return self.image.get_height() * scale_y

    def get_image_height(self) -> int:
        """
        Returns the unscaled height of the sprite image.

        Returns:
            int: The height of the image in pixels.
        """
        return self.image.get_height()

    def _get_scale(self, transform: 'Transform', axis: str) -> float:
        """
        Internal helper to get the scaling factor for a given axis ('x' or 'y').

        Args:
            transform (Transform): Optional transform provided by the caller.
            axis (str): Either 'x' or 'y' to indicate which scale to return.

        Raises:
            ReferenceError: If no transform is provided and the sprite has no own transform.

        Returns:
            float: The scale factor along the specified axis.
        """
        if transform is None:
            if self.transform is None:
                raise ReferenceError(
                    "Sprite doesn't have reference to Transform yet. Provide one or call this method in start()/update()."
                )
            transform = self.transform

        if axis == 'x':
            return transform.local_scale_x
        elif axis == 'y':
            return transform.local_scale_y
        else:
            raise ValueError("Axis must be 'x' or 'y'.")