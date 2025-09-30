import random
from engine.game_object import GameObject
from engine.game_objects.ui.button import Button
from engine.components.transform import Transform
from engine.components.sprite import Sprite
from engine.components.rigidbody2d import Rigidbody2D
from engine.components.platformer_movement import PlatformerMovement
from engine.components.camera_controller import CameraController
from engine.components.linebody2d import LineBody2D
from engine.components.test_component import TestComponent

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

def setup_main_scene(engine):
    main_scene = engine.create_scene("Main")

    # --- Player Setup ---
    player = GameObject("Player")
    player.add_component(Sprite("assets/images/cow.png"))
    player.add_component(Rigidbody2D(debug=True, freeze_rotation=True))
    player.add_component(PlatformerMovement(speed=500, jump_force=1000))

    player_transform = player.get_component(Transform)
    player_transform.set_world_position(WINDOW_WIDTH, 0)
    player_transform.set_local_scale(2)
    main_scene.add_game_object(player)

    # --- Game Buttons ---
    def exit_game(go):
        engine.change_active_scene("Menu")

    exit_button = Button(
        "Exit",
        exit_game,
        width=0.1,
        height=0.05,
        x=1,
        y=0,
        anchor="topright",
        bg_color=(255, 0, 0),
        hover_color=(255, 50, 50),
    )
    main_scene.add_game_object(exit_button)

    # --- Test Object ---
    test_object = GameObject("Test")
    test_object.add_component(Sprite("assets/images/shape.png"))
    test_object.add_component(TestComponent())
    main_scene.add_game_object(test_object)

    # --- Circle Container & Circles ---
    circle_container = GameObject("Circle Container")
    main_scene.add_game_object(circle_container)

    for i in range(10):
        circle = GameObject(f"Circle{i}")
        circle.add_component(Sprite("assets/images/football.png"))
        circle.add_component(
            Rigidbody2D(shape_type="circle", radius=50, debug=True, freeze_rotation=False)
        )

        circle_transform = circle.get_component(Transform)
        circle_transform.set_local_position(WINDOW_WIDTH + (i * 0.1), -300 - (i * 2))
        circle_transform.set_local_scale(random.random() * 0.5 + 0.5)

        circle_container.add_child(circle)

    # --- Camera ---
    main_scene.camera.add_component(CameraController(player_transform))
    main_scene.camera_component.set_zoom(0.5)

    # --- Floor ---
    floor = GameObject("Floor")
    floor_transform = floor.get_component(Transform)
    floor_transform.set_local_scale(5)
    floor_transform.set_local_rotation(15)

    floor_sprite = Sprite("assets/images/floor.png")
    floor.add_component(floor_sprite)
    floor.add_component(LineBody2D(static=True, debug=True, offset=(0, -250)))

    floor_transform.set_world_position(WINDOW_WIDTH, WINDOW_HEIGHT)
    main_scene.add_game_object(floor)

    # --- Wall ---
    wall1 = GameObject("Wall 1")
    wall1_transform = wall1.get_component(Transform)
    wall1_transform.set_local_scale(5)

    wall1_sprite = Sprite("assets/images/Wall.png")
    wall1.add_component(wall1_sprite)
    wall1.add_component(Rigidbody2D(static=True, debug=True))

    floor_x, floor_y = floor_transform.get_local_position()
    left_side_of_floor = floor_x + (floor_sprite.get_width(floor_transform) // 2)
    wall1_transform.set_local_position(left_side_of_floor - wall1_sprite.get_width(wall1_transform) // 2, floor_y)

    main_scene.add_game_object(wall1)

    return main_scene
