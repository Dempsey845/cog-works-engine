from game_object import GameObject


class Scene:
    """
    A Scene represents a collection of GameObjects.
    Scenes handle updating and rendering all their GameObjects.
    """

    def __init__(self, name: str = "Scene"):
        self.name = name
        self.game_objects: list[GameObject] = []

    def add_game_object(self, game_object: GameObject) -> None:
        """
        Add a GameObject to the scene and start it.

        Args:
            game_object (GameObject): The GameObject to add.
        """
        self.game_objects.append(game_object)
        game_object.start()

    def remove_game_object(self, game_object: GameObject) -> None:
        """
        Remove a GameObject from the scene.

        Args:
            game_object (GameObject): The GameObject to remove.
        """
        if game_object in self.game_objects:
            # Optionally call on_remove on all components
            for comp in game_object.components:
                if hasattr(comp, "on_remove"):
                    comp.on_remove()
            self.game_objects.remove(game_object)

    def update(self, dt: float) -> None:
        """
        Update all GameObjects in the scene.

        Args:
            dt (float): Delta time since last frame.
        """
        for obj in self.game_objects:
            obj.update(dt)

    def render(self, surface) -> None:
        """
        Render all GameObjects in the scene.

        Args:
            surface: The pygame surface to render onto.
        """
        for obj in self.game_objects:
            obj.render(surface)

    def __repr__(self):
        return f"<Scene name='{self.name}', objects={len(self.game_objects)}>"

class SceneManager:
    """
    SceneManager handles switching between scenes and managing the current active scene.
    """

    def __init__(self):
        self.scenes: dict[str, Scene] = {}
        self.active_scene: Scene | None = None

    def add_scene(self, scene: Scene) -> None:
        """
        Add a scene to the manager.

        Args:
            scene (Scene): The scene to add.
        """
        self.scenes[scene.name] = scene

    def set_active_scene(self, scene_name: str) -> None:
        """
        Switch to a different scene by name.

        Args:
            scene_name (str): Name of the scene to activate.
        """
        if scene_name in self.scenes:
            self.active_scene = self.scenes[scene_name]
        else:
            raise ValueError(f"Scene '{scene_name}' not found in SceneManager.")

    def update(self, dt: float) -> None:
        """Update the active scene if it exists."""
        if self.active_scene:
            self.active_scene.update(dt)

    def render(self, surface) -> None:
        """Render the active scene if it exists."""
        if self.active_scene:
            self.active_scene.render(surface)
