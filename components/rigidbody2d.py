from component import Component
from components.collider2d import Collider2D
from components.transform import Transform


class Rigidbody2D(Component):
    def __init__(self, gravity=0.0, mass=1.0):
        super().__init__()
        self.gravity = gravity
        self.mass = mass
        self.velocity = [0.0, 0.0]
        self.transform = None
        self.collider = None

    def start(self):
        self.transform = self.game_object.get_component(Transform)
        self.collider = self.game_object.get_component(Collider2D)
        if not self.transform or not self.collider:
            raise Exception("Rigidbody2D requires Transform and Collider2D components")

    def apply_force(self, fx, fy):
        self.velocity[0] += fx / self.mass
        self.velocity[1] += fy / self.mass

    def update(self, dt):
        self.velocity[1] += self.gravity * dt
        self.transform.x += self.velocity[0] * dt
        self.transform.y += self.velocity[1] * dt
        self.collider.update(dt)

        for other in self.game_object.scene.get_components(Collider2D):
            if other is self.collider:
                continue
            if self.collider.intersects(other):
                self._resolve_collision(other)

    def _resolve_collision(self, other):
        # Get colliders for convenience
        self_bottom = self.transform.y
        other_top = other.transform.y - other.height  # top of the other object

        if self.velocity[1] > 0:  # falling
            self.transform.y = other_top
        elif self.velocity[1] < 0:  # rising
            self.transform.y = other.transform.y + self.collider.height
        self.velocity[1] = 0
        self.collider.update(0)

