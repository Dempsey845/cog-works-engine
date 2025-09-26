from component import Component
from components.rigidbody2d import Rigidbody2D
import pygame

from input_manager import InputManager


class PlatformerMovement(Component):
    """
    Simple 2D platformer movement using the Rigidbody2D system.
    Requires Rigidbody2D for physics and collision handling.
    """

    def __init__(self, speed=200, jump_force=500):
        super().__init__()
        self.speed = speed
        self.jump_force = jump_force
        self.input = InputManager.get_instance()
        self.rigidbody: Rigidbody2D = None

    def start(self):
        self.rigidbody = self.game_object.get_component(Rigidbody2D)
        if not self.rigidbody:
            raise Exception("PlatformerMovement requires a Rigidbody2D")

    def update(self, dt):
        if not self.rigidbody or not self.rigidbody.body:
            return

        body = self.rigidbody.body

        # Horizontal movement
        vx = 0
        if self.input.is_key_down(pygame.K_a) or self.input.is_key_down(pygame.K_LEFT):
            vx -= self.speed
        if self.input.is_key_down(pygame.K_d) or self.input.is_key_down(pygame.K_RIGHT):
            vx += self.speed

        # Preserve vertical velocity (gravity / jumping handled by Rigidbody2D)
        body.velocity = vx, body.velocity.y

        # Jumping
        if (self.input.is_key_down(pygame.K_SPACE) or
            self.input.is_key_down(pygame.K_w) or
            self.input.is_key_down(pygame.K_UP)):

            if self.is_grounded():
                # Apply an instantaneous upward impulse
                body.apply_impulse_at_local_point((0, -self.jump_force * body.mass))

    def is_grounded(self):
        """
        Simple grounded check: assume body is grounded if its vertical velocity is near 0.
        """
        return abs(self.rigidbody.body.velocity.y) < 0.1
