import uuid
from components.transform import Transform


class GameObject:
    """
    A base class representing any entity in the game world.
    GameObjects can hold components that define their behaviour,
    such as rendering, physics, or custom logic.
    """

    _id_counter = 0  # class-level counter for incremental IDs

    def __init__(self, name: str = "GameObject"):
        """
        Initialise a new GameObject with a unique identifier.
        Automatically adds a Transform component.
        """
        # Assign unique IDs
        self.uuid = uuid.uuid4()          # Globally unique identifier
        self.id = GameObject._id_counter  # Local incremental ID
        GameObject._id_counter += 1

        # Meta information
        self.name = name
        self.active = True

        # Scene
        self.scene = None

        # Component storage
        self.components: list = []

        # Add default Transform component
        self.transform = Transform()
        self.add_component(self.transform)

        # ---------------- Hierarchy ----------------
        self.parent: "GameObject | None" = None  # Parent GameObject
        self.children: list["GameObject"] = []   # List of child GameObjects

    # ---------------- Component Management ----------------
    def add_component(self, component) -> None:
        """
        Attach a component to the GameObject.
        Ensures only one component of each type exists.
        Prevents adding Rigidbody2D to a child GameObject.
        """
        component_type = type(component)

        # Only allow one Transform
        if component_type is Transform and self.get_component(Transform):
            raise ValueError("GameObject already has a Transform component")

        # Prevent duplicate components
        if self.get_component(component_type) is not None:
            raise ValueError(f"GameObject already has a component of type {component_type.__name__}")

        # Prevent adding Rigidbody2D to child objects
        if component_type.__name__ == "Rigidbody2D" and self.parent is not None:
            raise ValueError("Cannot add Rigidbody2D to a child GameObject")

        component.game_object = self
        self.components.append(component)

    def remove_component(self, component_type) -> bool:
        """
        Remove the first component of the given type from the GameObject.
        """
        # Do not allow removing Transform
        if component_type is Transform:
            print("Cannot remove Transform component from GameObject.")
            return False

        for i, comp in enumerate(self.components):
            if isinstance(comp, component_type):
                if hasattr(comp, "on_remove"):
                    comp.on_remove()
                self.components.pop(i)
                return True
        return False

    def get_component(self, component_type):
        """
        Retrieve the first component of a given type.
        """
        for comp in self.components:
            if isinstance(comp, component_type):
                return comp
        return None

    # ---------------- Hierarchy Management ----------------
    def add_child(self, child: "GameObject") -> None:
        """
        Add a child GameObject to this GameObject.
        Automatically removes child from previous parent if needed
        and propagates this GameObject's scene to the child hierarchy.
        """
        if child.parent:
            child.parent.remove_child(child)
        child.parent = self
        self.children.append(child)
        child._set_scene_recursive(self.scene)  # propagate scene to child and descendants

    def _set_scene_recursive(self, scene) -> None:
        """
        Set the scene for this GameObject and all its children recursively.
        """
        self.scene = scene
        for child in self.children:
            child._set_scene_recursive(scene)

    def remove_child(self, child: "GameObject") -> None:
        """
        Remove a child GameObject from this GameObject and clear its scene.
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            child._set_scene_recursive(None)  # remove scene from child and its descendants

    def get_children(self) -> list["GameObject"]:
        """
        Return a list of child GameObjects.
        """
        return self.children

    # ---------------- Lifecycle ----------------
    def start(self) -> None:
        """
        Call start() on all components and children.
        """
        for comp in self.components:
            comp.start()
        for child in self.children:
            child.start()

    def update(self, dt: float) -> None:
        """
        Update all components and children.
        """
        if not self.active:
            return
        for comp in self.components:
            comp.update(dt)
        for child in self.children:
            child.update(dt)

    def fixed_update(self, dt: float) -> None:
        """
        Fixed timestep update for physics or deterministic logic.
        Calls fixed_update on all components that implement it, including children.
        """
        if not self.active:
            return
        for comp in self.components:
            comp.fixed_update(dt)
        for child in self.children:
            child.fixed_update(dt)

    def render(self, surface) -> None:
        """
        Render all components and children.
        """
        if not self.active:
            return
        for comp in self.components:
            if hasattr(comp, "render"):
                comp.render(surface)
        for child in self.children:
            child.render(surface)

    # ---------------- Utilities ----------------
    def get_world_position(self):
        return self.transform.get_world_position()

    def __repr__(self):
        return f"<GameObject id={self.id}, uuid={self.uuid}, name='{self.name}'>"
