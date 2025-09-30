from engine.game_objects.ui.button import Button
from engine.game_objects.ui.label import Label


def setup_menu_scene(engine):
    menu_scene = engine.create_scene("Menu")

    def start_game(go):
        engine.change_active_scene("Main")

    title_label = Label("Cog Works Engine", y=0.1, anchor="center", bg_color=(0, 0, 255))
    start_button = Button("Start Game", start_game)
    menu_scene.add_game_object(title_label)
    menu_scene.add_game_object(start_button)

    return menu_scene
