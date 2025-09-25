from component import Component
from components.rigidbody2d import Rigidbody2D
import pygame
from input_manager import InputManager


class TopDownMovement(Component):
    """
    Moves a GameObject in a top-down 2D plane using keyboard input.
    Works with Rigidbody2D for proper physics and collisions.
    """

    def __init__(self, speed=200):
        super().__init__()
        self.speed = speed  # pixels per second
        self.input = InputManager.get_instance()
        self.rigidbody = None

    def start(self):
        self.rigidbody = self.game_object.get_component(Rigidbody2D)
        if not self.rigidbody:
            raise Exception("TopDownMovement requires a Rigidbody2D")

    def update(self, dt):
        dx, dy = 0, 0

        # WASD / Arrow key input
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

        # Set velocity directly
        self.rigidbody.velocity[0] = dx * self.speed
        self.rigidbody.velocity[1] = dy * self.speed
