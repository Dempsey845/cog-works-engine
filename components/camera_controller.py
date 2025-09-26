from component import Component
from components.camera import Camera
from components.transform import Transform


class CameraController(Component):
    """
    CameraController is a component that allows a camera to follow a target Transform.
    It updates the camera's offset to keep the target roughly centred on the screen.
    """

    def __init__(self, target_transform: Transform):
        """
        Initialize the CameraController with a target Transform to follow.

        Args:
            target_transform (Transform): The Transform of the target GameObject.
        """
        super().__init__()
        self.target_transform = target_transform
        self.camera_component: Camera | None = None

    def start(self):
        self.camera_component = self.game_object.scene.camera_component

    def update(self, dt: float) -> None:
        width, height = self.game_object.scene.get_window_size()

        zoom = self.camera_component.zoom

        # Center camera on target
        self.camera_component.center_on(
            self.target_transform.local_x,
            self.target_transform.local_y,
            width,
            height
        )

