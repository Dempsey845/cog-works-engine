import random

from components.circlebody2d import CircleBody2D
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
engine = Engine(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=180)

main_scene = Scene("Main")
engine.add_scene(main_scene)
engine.set_active_scene("Main")

# --- Player GameObject ---
player = GameObject("Player")
player.add_component(Sprite("player.png"))
player.add_component(Rigidbody2D(debug=True, freeze_rotation=True))
player.add_component(PlatformerMovement(speed=800, jump_force=500))

# Place player somewhere above the floor
player_transform = player.get_component(Transform)
player_transform.set_world_position(WINDOW_WIDTH, 0)
player_transform.set_local_scale(0.5)

main_scene.add_game_object(player)

# Shape physics object
shape = GameObject("Shape")
shape.add_component(Sprite("shape.png"))
shape.add_component(Rigidbody2D(debug=True, freeze_rotation=False))
shape.get_component(Transform).set_world_position(WINDOW_WIDTH, -400)
main_scene.add_game_object(shape)

# Circle Container GameObject
circle_container = GameObject("Circle Container")
main_scene.add_game_object(circle_container)

# --- Circle GameObjects ---
for i in range(100):
    circle = GameObject(f"Circle{i}")
    circle.add_component(Sprite("circle.png"))
    circle.add_component(CircleBody2D(radius=50, debug=False, freeze_rotation=False))

    circle_transform = circle.get_component(Transform)
    circle_transform.set_world_position(WINDOW_WIDTH + (i * 5), -300 - (i * 10))
    circle_transform.set_local_scale(random.random() * 2 + 0.2)

    circle_container.add_child(circle)

# --- Camera Controller ---
main_scene.camera.add_component(CameraController(player_transform))
main_scene.camera_component.set_zoom(0.5)

# --- Floor GameObject ---
floor = GameObject("Floor")
floor_sprite = Sprite("floor.png")
floor.add_component(floor_sprite)
floor.add_component(Rigidbody2D(static=True, debug=True))
floor.get_component(Transform).set_local_scale(20, 1)

# Align floor to bottom of screen
floor_height = floor_sprite.image.get_height()
floor.get_component(Transform).set_world_position(WINDOW_WIDTH, WINDOW_HEIGHT)
main_scene.add_game_object(floor)

# --- Run ---
engine.run()
