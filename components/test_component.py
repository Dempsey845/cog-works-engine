from component import Component


class TestComponent(Component):
    def __init__(self):
        super().__init__()

    def update(self, dt:float):
        self.game_object.transform.local_x += 50 * dt
