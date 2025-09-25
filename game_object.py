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

    def add_component(self, component) -> None:
        """
        Attach a component to the GameObject.
        Ensures only one component of each type exists.
        """
        component_type = type(component)
        if self.get_component(component_type) is not None:
            raise ValueError(f"GameObject already has a component of type {component_type.__name__}")
        component.game_object = self  # link component to this GameObject
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

    def start(self) -> None:
        """
        Call start() on all components.
        """
        for comp in self.components:
            comp.start()

    def update(self, dt: float) -> None:
        """
        Update all components.
        """
        if not self.active:
            return
        for comp in self.components:
            comp.update(dt)

    def fixed_update(self, dt: float) -> None:
        """
        Fixed timestep update for physics or deterministic logic.
        Calls fixed_update on all components that implement it.
        """
        if not self.active:
            return
        for comp in self.components:
            comp.fixed_update(dt)

    def render(self, surface) -> None:
        """
        Render all components.
        """
        if not self.active:
            return
        for comp in self.components:
            if hasattr(comp, "render"):
                comp.render(surface)

    def __repr__(self):
        return f"<GameObject id={self.id}, uuid={self.uuid}, name='{self.name}'>"
