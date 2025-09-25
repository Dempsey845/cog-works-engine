# engine.py
import pygame
from pygame_lib.window import Window
from scene_manager import SceneManager, Scene
from input_manager import InputManager
from event_manager import EventManager

class Engine:
    """
    The main engine class that manages the game/application loop.
    Provides update, render, event handling, and scene management.
    """

    def __init__(self, width: int = 500, height: int = 500, caption: str = "CogWorks Engine", fps: int = 60):
        """
        Initialise the engine with a window, scene manager, and runtime state.

        Args:
            width (int, optional): Initial width of the window. Defaults to 500.
            height (int, optional): Initial height of the window. Defaults to 500.
            caption (str, optional): The window caption. Defaults to "CogWorks Engine".
            fps (int, optional): Frames per second. Defaults to 60.
        """
        self.window = Window(pygame, width, height, caption, resizable=True)
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = fps  # Target frames per second

        # Scene manager
        self.scene_manager = SceneManager()

        # Input manager
        self.input = InputManager.get_instance()

        # Event manager
        self.event_manager = EventManager.get_instance()
        self.event_manager.subscribe(self.handle_event)

    # ---------------- Scene Management ---------------- #

    def add_scene(self, scene: Scene) -> None:
        """Add a scene to the scene manager."""
        self.scene_manager.add_scene(scene)

    def set_active_scene(self, scene_name: str) -> None:
        """Set the currently active scene by name."""
        self.scene_manager.set_active_scene(scene_name)

    # ---------------- Event Handling ---------------- #

    def handle_event(self, event):
        """Handle engine-specific events like QUIT."""
        if event.type == pygame.QUIT:
            self.quit()

    # ---------------- Engine Loop ---------------- #

    def update(self):
        """
        Handle input and update game/application state and the active scene.
        """
        self.event_manager.poll_events()  # Poll and dispatch events
        self.input.update()  # Update input states per frame

        # dt in seconds, but clamp to avoid explosions
        dt = self.clock.get_time() / 1000.0
        dt = min(dt, 0.05)  # max step = 50ms (~20 FPS physics)

        self.scene_manager.update(dt)

    def render(self):
        """
        Render/draw content to the screen and the active scene.
        """
        self.window.screen.fill((30, 30, 30))  # Clear screen with dark grey
        self.scene_manager.render(self.window.screen)
        # FPS display
        pygame.display.set_caption(f"{self.window.caption} - FPS: {self.clock.get_fps():.2f}")
        pygame.display.flip()

    def quit(self):
        """Stop the engine loop and quit pygame."""
        self.running = False

    def run(self):
        """
        Run the main engine loop with a fixed timestep for physics.
        """
        fixed_dt = 1 / 60.0  # 60 FPS physics step
        accumulator = 0.0

        while self.running:
            # Get frame time in seconds, clamp huge spikes
            frame_time = self.clock.tick(self.fps) / 1000.0
            frame_time = min(frame_time, 0.25)  # cap max 250ms

            accumulator += frame_time

            # Poll events and update input once per frame
            self.event_manager.poll_events()
            self.input.update()

            # Fixed timestep updates (physics / stable simulation)
            while accumulator >= fixed_dt:
                self.scene_manager.fixed_update(fixed_dt)
                accumulator -= fixed_dt

            # Variable timestep updates (animations, UI, effects)
            self.scene_manager.update(frame_time)

            # Render the scene
            self.render()

