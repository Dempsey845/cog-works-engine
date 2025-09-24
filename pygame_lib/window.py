class Window:
    """
    A wrapper class around pygame's display window handling.
    Provides convenient methods for creating and resizing the window.
    """

    def __init__(self, pygame, width: int, height: int, caption: str, resizable: bool = False, fullscreen: bool = False):
        """
        Initialise a window with the given dimensions and caption.

        Args:
            pygame: The pygame module instance.
            width (int): The initial width of the window.
            height (int): The initial height of the window.
            caption (str): The caption/title of the window.
            resizable (bool, optional): If True, allows the window to be resizable. Defaults to False.
            fullscreen (bool, optional): If True, starts the window in fullscreen mode. Defaults to False.
        """
        self.pygame = pygame
        self.width = width
        self.height = height
        self.caption = caption
        self.resizable = resizable
        self.fullscreen = fullscreen

        pygame.init()
        self.screen = self._create_window()

    def _create_window(self):
        """Internal helper to create the pygame window with the current settings."""
        flags = 0
        if self.resizable:
            flags |= self.pygame.RESIZABLE
        if self.fullscreen:
            flags |= self.pygame.FULLSCREEN

        self.pygame.display.set_caption(self.caption)
        return self.pygame.display.set_mode((self.width, self.height), flags)

    def configure(self, width: int = None, height: int = None, resizable: bool = None, fullscreen: bool = None):
        """
        Reconfigure the window size or settings.

        Args:
            width (int, optional): New width of the window. If None, keeps current width.
            height (int, optional): New height of the window. If None, keeps current height.
            resizable (bool, optional): Update whether the window should be resizable.
            fullscreen (bool, optional): Update whether the window should be fullscreen.
        """
        if width:
            self.width = width
        if height:
            self.height = height
        if resizable is not None:
            self.resizable = resizable
        if fullscreen is not None:
            self.fullscreen = fullscreen

        self.screen = self._create_window()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode on or off."""
        self.fullscreen = not self.fullscreen
        self.screen = self._create_window()

    def resize(self, width: int, height: int):
        """
        Resize the window to the given dimensions.

        Args:
            width (int): The new width.
            height (int): The new height.
        """
        self.configure(width=width, height=height)

    def get_size(self):
        """
        Get the current size of the window.

        Returns:
            tuple: (width, height)
        """
        return self.screen.get_size()
