import pymunk

from cogworks.components.camera import Camera
from cogworks.game_object import GameObject
from cogworks.trigger_collision_manager import TriggerCollisionManager


class Scene:
    """
    A Scene represents a collection of GameObjects.
    Scenes handle updating, fixed updates, and rendering all their GameObjects.
    Each Scene has its own camera GameObject by default.
    """

    def __init__(self, name: str = "Scene", gravity=(0, 900)):
        """
        Initialize a Scene with a name and default camera.

        Args:
            name (str): The name of the scene.
        """
        self._needs_sort = False
        self.start_states = None
        self.name = name
        self.game_objects: list[GameObject] = []
        self.start_game_objects: list[GameObject] = []

        self.engine = None

        # Default camera setup
        self.camera = GameObject("Camera")
        self.camera_component = Camera()
        self.camera.add_component(self.camera_component)

        self.physics_space = pymunk.Space()
        self.gravity = gravity
        self.physics_space.gravity = self.gravity
        self.trigger_collision_manager = TriggerCollisionManager()


    def start(self):
        """
        Start the scene by adding the default camera GameObject.
        """
        self.start_game_objects = self.game_objects.copy()

        self.add_game_object(self.camera)

        # Start each original game object
        for go in self.game_objects:
            go.active = True
            go.start()

    def add_game_object(self, game_object: GameObject) -> None:
        """
        Add a GameObject to the scene, set its scene reference, and call its start method.

        Args:
            game_object (GameObject): The GameObject to add.
        """
        self.game_objects.append(game_object)
        game_object.scene = self
        self._needs_sort = True

    def remove_game_object(self, game_object: GameObject) -> None:
        """
        Remove a GameObject from the scene and optionally call `on_remove` on its components.

        Args:
            game_object (GameObject): The GameObject to remove.
        """
        if game_object in self.game_objects:
            for comp in game_object.components:
                if hasattr(comp, "on_remove"):
                    comp.on_remove()
            self.game_objects.remove(game_object)
            self._needs_sort = True

    def get_components(self, component_type):
        """
        Get all components of a given type from all GameObjects in the scene.

        Args:
            component_type (type): The class/type of component to search for.

        Returns:
            list: A list of matching components.
        """
        results = []
        for obj in self.game_objects:
            for comp in obj.components:
                if isinstance(comp, component_type):
                    results.append(comp)
        return results

    def update(self, dt: float) -> None:
        """
        Update all GameObjects and CollisionManagers in the scene.

        Args:
            dt (float): Delta time since last frame.
        """
        for obj in self.game_objects:
            obj.update(dt)

        if self.trigger_collision_manager:
            self.trigger_collision_manager.update(dt)

    def fixed_update(self, dt: float) -> None:
        """
        Fixed timestep update for physics or deterministic logic.
        Calls `fixed_update` on GameObjects and their components if implemented.

        Args:
            dt (float): Fixed delta time.
        """

        self.physics_space.step(dt)

        for obj in self.game_objects:
            if hasattr(obj, "fixed_update"):
                obj.fixed_update(dt)
            for comp in obj.components:
                if hasattr(comp, "fixed_update"):
                    comp.fixed_update(dt)

    def render(self, surface) -> None:
        """
        Render all GameObjects in the scene to the given surface in order of z_index.
        GameObjects without a z_index attribute default to 0.

        Args:
            surface: The surface to render onto (e.g., a Pygame surface).
        """
        # Sort game objects by z_index (default 0)
        if self._needs_sort:
            self.game_objects.sort(key=lambda obj: obj.z_index)
            self._needs_sort = False

        for obj in self.game_objects:
            obj.render(surface)

    def restart(self):
        # Create a new physics space
        self.physics_space = pymunk.Space()
        self.physics_space.gravity = self.gravity

        for go in self.game_objects:
            go.reset_to_start()

    def save_start_states(self):
        self.start_states = {}

        def save_go_state(go):
            transform = go.get_component("Transform")
            if transform:
                self.start_states[go.uuid] = {
                    "local_x": transform.local_x,
                    "local_y": transform.local_y,
                    "local_scale_x": transform.local_scale_x,
                    "local_scale_y": transform.local_scale_y,
                    "local_rotation": transform.local_rotation,
                }
            # Recurse through children
            for child in getattr(go, "children", []):
                save_go_state(child)

        for go in self.game_objects:
            save_go_state(go)

    def get_window_size(self) -> tuple[int, int]:
        """
        Get the current window size from the cogworks.

        Returns:
            tuple[int, int]: Width and height of the window.
        """
        return self.engine.window.get_size()

    def __repr__(self):
        return f"<Scene name='{self.name}', objects={len(self.game_objects)}>"


class SceneManager:
    """
    SceneManager handles adding, switching, and updating the currently active scene.
    """

    def __init__(self):
        self.scenes: dict[str, Scene] = {}
        self.active_scene: Scene | None = None

    def start_active_scene(self):
        """
        Call start() on the active scene if it exists.
        """
        if self.active_scene:
            self.active_scene.start()

    def add_scene(self, scene: Scene, engine) -> None:
        """
        Add a scene to the manager and assign it an cogworks reference.

        Args:
            scene (Scene): The scene to add.
            engine: The game cogworks instance.
        """
        scene.engine = engine
        self.scenes[scene.name] = scene

    def set_active_scene(self, scene_name: str) -> None:
        """
        Set a scene as the active scene by name.

        Args:
            scene_name (str): Name of the scene to activate.

        Raises:
            ValueError: If the scene name is not found in the manager.
        """
        if scene_name in self.scenes:
            self.active_scene = self.scenes[scene_name]
        else:
            raise ValueError(f"Scene '{scene_name}' not found in SceneManager.")

    def restart_active_scene(self):
        self.active_scene.restart()

    def update(self, dt: float) -> None:
        """
        Update the active scene.

        Args:
            dt (float): Delta time since last frame.
        """
        if self.active_scene:
            self.active_scene.update(dt)

    def fixed_update(self, dt: float) -> None:
        """
        Call fixed_update on the active scene.

        Args:
            dt (float): Fixed delta time.
        """
        if self.active_scene:
            self.active_scene.fixed_update(dt)

    def render(self, surface) -> None:
        """
        Render the active scene to the given surface.

        Args:
            surface: The surface to render onto.
        """
        if self.active_scene:
            self.active_scene.render(surface)
