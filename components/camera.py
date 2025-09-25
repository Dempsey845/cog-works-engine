from component import Component


class Camera(Component):
    def __init__(self):
        super().__init__()
        self.offset_x = 0
        self.offset_y = 200

    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def world_to_screen(self, x, y):
        return x - self.offset_x, y - self.offset_y
