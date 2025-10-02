from cogworks.engine import Engine
from assets.scenes.main_scene import setup_main_scene
from assets.scenes.menu_scene import setup_menu_scene

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

engine = Engine(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=180)

# Setup scenes
main_scene = setup_main_scene(engine)
menu_scene = setup_menu_scene(engine)

engine.set_active_scene("Menu")

# Run cogworks
engine.run()
