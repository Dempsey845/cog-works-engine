from components.camera import Camera
from game_object import GameObject


class Scene:
    """
    A Scene represents a collection of GameObjects.
    Scenes handle updating, fixed updates, and rendering all their GameObjects.
    Each Scene has its own camera GameObject by default.
    """

    def __init__(self, name: str = "Scene"):
        """
        Initialize a Scene with a name and default camera.

        Args:
            name (str): The name of the scene.
        """
        self.name = name
        self.game_objects: list[GameObject] = []

        self.engine = None

        # Default camera setup
        self.camera = GameObject("Camera")
        self.camera_component = Camera()
        self.camera.add_component(self.camera_component)

    def start(self):
        """
        Start the scene by adding the default camera GameObject.
        """
        self.add_game_object(self.camera)
        for go in self.game_objects:
            go.start()

    def add_game_object(self, game_object: GameObject) -> None:
        """
        Add a GameObject to the scene, set its scene reference, and call its start method.

        Args:
            game_object (GameObject): The GameObject to add.
        """
        self.game_objects.append(game_object)
        game_object.scene = self

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
        Update all GameObjects in the scene.

        Args:
            dt (float): Delta time since last frame.
        """
        for obj in self.game_objects:
            obj.update(dt)

    def fixed_update(self, dt: float) -> None:
        """
        Fixed timestep update for physics or deterministic logic.
        Calls `fixed_update` on GameObjects and their components if implemented.

        Args:
            dt (float): Fixed delta time.
        """
        for obj in self.game_objects:
            if hasattr(obj, "fixed_update"):
                obj.fixed_update(dt)
            for comp in obj.components:
                if hasattr(comp, "fixed_update"):
                    comp.fixed_update(dt)

    def render(self, surface) -> None:
        """
        Render all GameObjects in the scene to the given surface.

        Args:
            surface: The surface to render onto (e.g., a Pygame surface).
        """
        for obj in self.game_objects:
            obj.render(surface)

    def get_window_size(self) -> tuple[int, int]:
        """
        Get the current window size from the engine.

        Returns:
            tuple[int, int]: Width and height of the window.
        """
        width = self.engine.window.width
        height = self.engine.window.height
        return width, height

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
        Add a scene to the manager and assign it an engine reference.

        Args:
            scene (Scene): The scene to add.
            engine: The game engine instance.
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
