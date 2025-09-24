from components.top_down_movement import TopDownMovement
from engine import Engine
from scene_manager import Scene, GameObject
from components.sprite import Sprite

engine = Engine()

# Create scenes
main_scene = Scene("Main")
second_scene = Scene("Second")
engine.add_scene(main_scene)
engine.add_scene(second_scene)
engine.set_active_scene("Second")

# Add a GameObject
player = GameObject("Player")
player.add_component(Sprite("player.png"))
main_scene.add_game_object(player)

shape = GameObject("Shape")
shape.add_component(Sprite("shape.png"))
shape.add_component(TopDownMovement())
second_scene.add_game_object(shape)

# Run the engine
engine.run()
