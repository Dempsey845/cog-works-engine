import pygame
from cogworks.component import Component
from cogworks.pygame_wrappers.event_manager import EventManager


class UITransform(Component):
    """
    UITransform defines the position, size, and anchor of a UI element.

    Features:
        - Supports absolute or relative positioning and sizing.
        - Anchors elements to corners or center of the screen.
        - Updates automatically when the window is resized.
        - Integrates with `UILayout` to allow parent-managed positioning.
        - Provides setters for position, size, and anchor.
    """

    def __init__(self, x=0, y=0, width=1, height=1, anchor="topleft", relative=True):
        """
        Initialise a UITransform component.

        Args:
            x (int | float, optional): X position of the element. If `relative` is True,
                                       treated as a fraction of screen width (default: 0).
            y (int | float, optional): Y position of the element. If `relative` is True,
                                       treated as a fraction of screen height (default: 0).
            width (int | float, optional): Width of the element. If `relative` is True,
                                           treated as a fraction of screen width (default: 1).
            height (int | float, optional): Height of the element. If `relative` is True,
                                            treated as a fraction of screen height (default: 1).
            anchor (str, optional): Alignment of the rect relative to (x, y).
                                    Options: "topleft", "topright", "bottomleft", "bottomright", "center".
                                    (default: "topleft")
            relative (bool, optional): If True, interpret x, y, width, height as relative
                                       fractions of screen size. If False, interpret as pixels. (default: True)
        """
        super().__init__()
        self.anchor = anchor
        self.relative = relative
        self._x, self._y = x, y
        self._width, self._height = width, height
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.layout = None

    def start(self):
        EventManager.get_instance().subscribe(self._on_event)
        self.layout = self.game_object.get_component("UILayout")
        self.update_rect()

    def update_rect(self):
        parent_go = getattr(self.game_object, "parent", None)
        parent_transform = None
        if parent_go:
            parent_transform = parent_go.get_component("UITransform")

        if parent_go and parent_go.has_component("UILayout"):
            # Layout manages this child's rect
            return

        screen_width, screen_height = pygame.display.get_window_size()
        if parent_transform and self.relative:
            width = int(self._width * parent_transform.rect.width)
            height = int(self._height * parent_transform.rect.height)
            x = int(self._x * parent_transform.rect.width)
            y = int(self._y * parent_transform.rect.height)
        elif self.relative:
            width = int(self._width * screen_width)
            height = int(self._height * screen_height)
            x = int(self._x * screen_width)
            y = int(self._y * screen_height)
        else:
            width, height, x, y = int(self._width), int(self._height), int(self._x), int(self._y)

        # Apply anchor first (relative to its own local rect)
        if self.anchor == "center":
            x -= width // 2
            y -= height // 2
        elif self.anchor == "topright":
            x -= width
        elif self.anchor == "bottomleft":
            y -= height
        elif self.anchor == "bottomright":
            x -= width
            y -= height

        # Offset by parent global position
        if parent_transform:
            x += parent_transform.rect.x
            y += parent_transform.rect.y

        self.rect = pygame.Rect(x, y, width, height)

    def set_position(self, x, y):
        """
        Set the element's position and update its rect.

        Args:
            x (int | float): X position (absolute pixels or relative fraction).
            y (int | float): Y position (absolute pixels or relative fraction).
        """
        self._x, self._y = x, y
        self.update_rect()

    def set_size(self, width, height):
        """
        Set the element's size and update its rect.

        Args:
            width (int | float): Width (absolute pixels or relative fraction).
            height (int | float): Height (absolute pixels or relative fraction).
        """
        self._width, self._height = width, height
        self.update_rect()

    def set_anchor(self, anchor):
        """
        Set the element's anchor and update its rect.

        Args:
            anchor (str): Alignment of the rect relative to (x, y).
                          Options: "topleft", "topright", "bottomleft", "bottomright", "center".
        """
        self.anchor = anchor
        self.update_rect()

    def _on_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.update_rect()
            if self.layout:
                self.layout.update_layout()

    def on_destroy(self):
        EventManager.get_instance().unsubscribe(self._on_event)
