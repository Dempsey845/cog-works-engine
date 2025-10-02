import pygame

from cogworks.pygame_wrappers.window import Window
from cogworks.pygame_wrappers.input_manager import InputManager
from cogworks.pygame_wrappers.event_manager import EventManager
from cogworks.scene_manager import Scene, SceneManager


class Engine:
    """
    The main cogworks class that manages the game/application loop.
    Provides update, render, event handling, and scene management.
    """

    def __init__(self, width: int = 500, height: int = 500, caption: str = "CogWorks Engine", fps: int = 60, world_bound_x: int = 5000, world_bound_y: int = 5000):
        """
        Initialise the cogworks with a window, scene manager, and runtime state.

        Args:
            width (int, optional): Initial width of the window. Defaults to 500.
            height (int, optional): Initial height of the window. Defaults to 500.
            caption (str, optional): The window caption. Defaults to "CogWorks Engine".
            fps (int, optional): Frames per second. Defaults to 60.
            world_bound_x (int, optional): World boundary x position for GameObject, if passes it, it gets destroyed
            world_bound_y (int, optional): World boundary y position for GameObject, if passes it, it gets destroyed
        """
        self.window = Window(pygame, width, height, caption, resizable=True)
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = fps  # Target frames per second
        self.world_bound_x = world_bound_x
        self.world_bound_y = world_bound_y

        # Scene manager
        self.scene_manager = SceneManager()

        # Input manager
        self.input = InputManager.get_instance()

        # Event manager
        self.event_manager = EventManager.get_instance()
        self.event_manager.subscribe(self.handle_event)
        self.window.subscribe_events(self.event_manager)

    # ---------------- Scene Management ---------------- #

    def add_scene(self, scene: Scene) -> None:
        """Add a scene to the scene manager."""
        self.scene_manager.add_scene(scene, self)

    def set_active_scene(self, scene_name: str) -> None:
        """Set the currently active scene by name."""
        self.scene_manager.set_active_scene(scene_name)

    def start_active_scene(self):
        """
        Call start() on the active scene if it exists.
        """
        self.scene_manager.start_active_scene()

    def change_active_scene(self, scene_name: str) -> None:
        """Change the currently active scene by name."""
        self.set_active_scene(scene_name)
        self.start_active_scene()
        self.scene_manager.restart_active_scene()

    def create_scene(self, scene_name: str, gravity=(0, 900)) -> Scene:
        """Create a new scene and add it to scene manager."""
        new_scene = Scene(scene_name, gravity)
        self.add_scene(new_scene)
        return new_scene

    # ---------------- Event Handling ---------------- #

    def handle_event(self, event):
        """Handle cogworks-specific events like QUIT."""
        if event.type == pygame.QUIT:
            self.quit()

    # ---------------- Engine Loop ---------------- #

    def render(self):
        """
        Render/draw content to the screen and the active scene.
        """
        self.window.render()

        self.scene_manager.render(self.window.screen)

        # FPS display, throttled to once per second
        if pygame.time.get_ticks() % 1000 < 16:
            pygame.display.set_caption(f"{self.window.caption} - FPS: {self.clock.get_fps():.2f}")

        pygame.display.flip()

    def quit(self):
        """Stop the cogworks loop and quit pygame."""
        self.running = False

    def run(self):
        """
        Run the main cogworks loop with a fixed timestep for physics.
        """
        fixed_dt = 1 / 60.0  # 60 FPS physics step
        accumulator = 0.0

        for scene in self.scene_manager.scenes.values():
            scene.save_start_states()

        # Start the active scene
        self.scene_manager.start_active_scene()

        while self.running:
            # Get frame time in seconds, clamp huge spikes
            frame_time = self.clock.tick(self.fps) / 1000.0
            frame_time = min(frame_time, 0.25)  # cap max 250ms

            accumulator += frame_time

            # Poll events and update input once per frame
            self.event_manager.poll_events()
            self.input.update()

            # Fixed timestep updates (physics / stable simulation)
            max_updates = 5
            updates = 0
            while accumulator >= fixed_dt and updates < max_updates:
                self.scene_manager.fixed_update(fixed_dt)
                accumulator -= fixed_dt
                updates += 1

            # Variable timestep updates (animations, UI, effects)
            self.scene_manager.update(frame_time)

            # Render the scene
            self.render()

