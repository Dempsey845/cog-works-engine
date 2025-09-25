from engine import Engine
from scene_manager import Scene, GameObject

from components.transform import Transform
from components.sprite import Sprite
from components.collider2d import Collider2D
from components.rigidbody2d import Rigidbody2D
from components.platformer_movement import PlatformerMovement  # <- changed

# --- Window size ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# --- Setup engine and scene ---
engine = Engine(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

main_scene = Scene("Main")
engine.add_scene(main_scene)
engine.set_active_scene("Main")

# --- Player GameObject ---
player = GameObject("Player")
player.add_component(Sprite("player.png"))
player.add_component(Collider2D(debug=True))
player.add_component(Rigidbody2D(gravity=1000.0))
player.add_component(PlatformerMovement(speed=200, jump_force=500))

# Place player somewhere above the floor
player.get_component(Transform).set_position(WINDOW_WIDTH // 2, 0)
player.get_component(Transform).set_scale(0.5)

main_scene.add_game_object(player)

# --- Floor GameObject ---
floor = GameObject("Floor")
floor_sprite = Sprite("floor.png")
floor.add_component(floor_sprite)
floor.add_component(Collider2D(debug=True))

# Align floor to bottom of screen
floor_height = floor_sprite.image.get_height()
floor.get_component(Transform).set_position(WINDOW_WIDTH // 2, WINDOW_HEIGHT)


main_scene.add_game_object(floor)

# --- Run ---
engine.run()
