from engine.components.ui.ui_button import UIButton
from engine.components.ui.ui_image import UIImage
from engine.components.ui.ui_layout import UILayout
from engine.components.ui.ui_transform import UITransform
from engine.game_object import GameObject


def setup_menu_scene(engine):
    menu_scene = engine.create_scene("Menu")

    def start_game(go):
        engine.change_active_scene("Main")

    def exit_game(go):
        engine.quit()

    # Create a layout
    layout = GameObject("MenuLayout")
    layout.add_component(UITransform(x=0.5, y=0.5, width=0.4, height=0.6, anchor="center"))
    layout.add_component(UILayout(vertical=True, spacing=10))
    menu_scene.add_game_object(layout)

    # Logo
    logo = GameObject("LogoImage")
    logo.add_component(UITransform(width=0.5, height=0.5))
    logo.add_component(UIImage("images/cog_works_icon_2.png", True))
    layout.add_child(logo)

    # Add buttons
    play_btn = GameObject("PlayButton")
    play_btn.add_component(UITransform(width=1, height=0.2))  # relative to parent layout
    play_btn.add_component(UIButton("Play", on_click=start_game))
    layout.add_child(play_btn)

    exit_btn = GameObject("ExitButton")
    exit_btn.add_component(UITransform(width=1, height=0.2))
    exit_btn.add_component(UIButton("Exit", on_click=exit_game))
    layout.add_child(exit_btn)

    return menu_scene
