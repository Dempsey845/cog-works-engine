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
        self.input.update()         # Update input states per frame
        self.scene_manager.update(self.clock.get_time() / 1000)  # dt in seconds

    def render(self):
        """
        Render/draw content to the screen and the active scene.
        """
        self.window.screen.fill((30, 30, 30))  # Clear screen with dark grey
        self.scene_manager.render(self.window.screen)
        pygame.display.flip()

    def quit(self):
        """Stop the engine loop and quit pygame."""
        self.running = False

    def run(self):
        """
        Run the main engine loop.
        Continuously updates and renders until quit() is called.
        """
        while self.running:
            self.update()
            self.render()
            self.clock.tick(self.fps)  # Limit FPS to reduce CPU usage
