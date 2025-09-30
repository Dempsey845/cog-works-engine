from engine.component import Component


class TestComponent(Component):
    def __init__(self):
        super().__init__()
        self.transform = None
        self.speed = 200
        
    def start(self) -> None:
        self.transform = self.game_object.transform

    def update(self, dt:float):
        dir_x, dir_y = self.transform.get_forward()
        self.transform.local_x += dir_x * self.speed * dt
        self.transform.local_y += dir_y * self.speed * dt
        self.transform.rotate(50 * dt)
