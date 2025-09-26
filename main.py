from engine import Engine
from scene_manager import Scene, GameObject

from components.transform import Transform
from components.sprite import Sprite
from components.rigidbody2d import Rigidbody2D
from components.platformer_movement import PlatformerMovement
from components.camera_controller import CameraController

# --- Window size ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# --- Setup engine and scene ---
engine = Engine(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

main_scene = Scene("Main")
engine.add_scene(main_scene)
engine.set_active_scene("Main")

# --- Player GameObject ---
player = GameObject("Player")
player.add_component(Sprite("player.png"))
player.add_component(Rigidbody2D(debug=True))
player.add_component(PlatformerMovement(speed=200, jump_force=500))

# Place player somewhere above the floor
player_transform = player.get_component(Transform)
player_transform.set_world_position(WINDOW_WIDTH, 0)
player_transform.set_local_scale(0.5)

main_scene.add_game_object(player)

# Shape physics object
shape = GameObject("Shape")
shape.add_component(Sprite("shape.png"))
shape.add_component(Rigidbody2D(debug=True))
shape.get_component(Transform).set_world_position(WINDOW_WIDTH, -400)
main_scene.add_game_object(shape)

# Test child object for player
child = GameObject("Child")
child.add_component(Sprite("shape.png"))
child.get_component(Transform).set_local_position(0, -100)
child.get_component(Transform).set_local_scale(0.2)
player.add_child(child)

# --- Camera Controller ---
main_scene.camera.add_component(CameraController(player_transform))
main_scene.camera_component.set_zoom(0.5)

# --- Floor GameObject ---
floor = GameObject("Floor")
floor_sprite = Sprite("floor.png")
floor.add_component(floor_sprite)
floor.add_component(Rigidbody2D(static=True, debug=True))

# Align floor to bottom of screen
floor_height = floor_sprite.image.get_height()
floor.get_component(Transform).set_world_position(WINDOW_WIDTH, WINDOW_HEIGHT)
main_scene.add_game_object(floor)

# --- Run ---
engine.run()
