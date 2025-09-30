import random

from engine import Engine
from game_object import GameObject
from game_objects.ui.Button import Button

from components.transform import Transform
from components.sprite import Sprite
from components.rigidbody2d import Rigidbody2D
from components.platformer_movement import PlatformerMovement
from components.camera_controller import CameraController
from components.circlebody2d import CircleBody2D
from components.linebody2d import LineBody2D

# --- Window size ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# --- Setup engine and scene ---
engine = Engine(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, fps=180)

main_scene = engine.create_scene("Main")
menu_scene = engine.create_scene("Menu")
engine.set_active_scene("Main")

# --- Player GameObject ---
player = GameObject("Player")
player.add_component(Sprite("cow.png"))
player.add_component(Rigidbody2D(debug=True, freeze_rotation=True))
player.add_component(PlatformerMovement(speed=500, jump_force=1000))

# --- Start Button ---
def start_game(go):
    engine.change_active_scene("Main")

start_button = Button("Start Game", start_game)
menu_scene.add_game_object(start_button)

# --- Exit Button ---
def exit_game(go):
    engine.change_active_scene("Menu")

exit_button = Button("Exit", exit_game, x=1, y=0, anchor="topright", bg_color=(255, 0, 0), hover_color=(255, 50, 50))
main_scene.add_game_object(exit_button)

# Place player somewhere above the floor
player_transform = player.get_component(Transform)
player_transform.set_world_position(WINDOW_WIDTH, 0)
player_transform.set_local_scale(2)

main_scene.add_game_object(player)

# Circle Container GameObject
circle_container = GameObject("Circle Container")
main_scene.add_game_object(circle_container)

# --- Circle GameObjects ---
for i in range(10):
    circle = GameObject(f"Circle{i}")
    circle.add_component(Sprite("football.png"))
    circle.add_component(CircleBody2D(radius=50, debug=False, freeze_rotation=False))

    circle_transform = circle.get_component(Transform)
    circle_transform.set_world_position(WINDOW_WIDTH + (i * 0.1), -300 - (i * 2))
    circle_transform.set_local_scale(random.random() * 0.5 + 0.5)

    circle_container.add_child(circle)

# --- Camera Controller ---
main_scene.camera.add_component(CameraController(player_transform))
main_scene.camera_component.set_zoom(0.5)

# --- Floor GameObject ---
floor = GameObject("Floor")
floor.get_component(Transform).set_local_scale(5)
floor.get_component(Transform).set_local_rotation(15)
floor_sprite = Sprite("floor.png")
floor.add_component(floor_sprite)
floor_transform = floor.get_component(Transform)
floor.add_component(LineBody2D(static=True, debug=True, offset=(0, -250)))

# Align floor to bottom of screen
floor_height = floor_sprite.image.get_height()
floor.get_component(Transform).set_world_position(WINDOW_WIDTH, WINDOW_HEIGHT)
main_scene.add_game_object(floor)

# -- Wall GameObject --
wall1 = GameObject("Wall 1")
wall1_transform = wall1.get_component(Transform)
wall1_transform.set_local_scale(5)

wall1_sprite = Sprite("Wall.png")
wall1.add_component(wall1_sprite)

wall1.add_component(Rigidbody2D(static=True, debug=True))

wall_width = wall1_sprite.get_width(wall1_transform)
wall_height = wall1_sprite.get_height(wall1_transform)

floor_x, floor_y = floor_transform.get_local_position()
left_side_of_floor = floor_x + (floor.get_component(Sprite).get_width(floor_transform) // 2)

wall1_transform.set_local_position(left_side_of_floor - wall_width//2, floor_y)

main_scene.add_game_object(wall1)

# --- Run ---
engine.run()
