from engine.game_objects.ui.button import Button
from engine.game_objects.ui.label import Label
from engine.game_objects.ui.ui_image import UIImage


def setup_menu_scene(engine):
    menu_scene = engine.create_scene("Menu")

    def start_game(go):
        engine.change_active_scene("Main")

    title_label = Label("Cog Works Engine", y=0, anchor="midtop", bg_color=(0, 0, 255))
    start_button = Button("Start Game", start_game, y=1, anchor="midbottom", min_width=200, min_height=50, max_width=200, max_height=50, z_index=2)
    logo_image = UIImage("assets/images/cog_works_icon.png")
    menu_scene.add_game_object(title_label)
    menu_scene.add_game_object(start_button)
    menu_scene.add_game_object(logo_image)


    return menu_scene
