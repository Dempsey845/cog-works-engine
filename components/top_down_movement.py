from component import Component
from components.transform import Transform
import pygame
from input_manager import InputManager

class TopDownMovement(Component):
    """
    Moves a GameObject in a top-down 2D plane using keyboard input.
    """

    def __init__(self, speed=200):
        super().__init__()
        self.speed = speed  # pixels per second
        self.input = InputManager.get_instance()
        self.transform = None

    def start(self):
        print(f"{self.game_object.name}: TopDownMovement initialized with speed {self.speed}")
        self.transform = self.game_object.get_component(Transform)

    def update(self, dt):
        dx, dy = 0, 0

        # WASD controls
        if self.input.is_key_down(pygame.K_w) or self.input.is_key_down(pygame.K_UP):
            dy -= 1
        if self.input.is_key_down(pygame.K_s) or self.input.is_key_down(pygame.K_DOWN):
            dy += 1
        if self.input.is_key_down(pygame.K_a) or self.input.is_key_down(pygame.K_LEFT):
            dx -= 1
        if self.input.is_key_down(pygame.K_d) or self.input.is_key_down(pygame.K_RIGHT):
            dx += 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            import math
            dx /= math.sqrt(2)
            dy /= math.sqrt(2)

        # Apply movement
        self.transform.x += dx * self.speed * dt
        self.transform.y += dy * self.speed * dt