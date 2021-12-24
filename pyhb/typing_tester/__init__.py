import time
from pyhb.typing_tester.display import *
from pyhb.typing_tester.settings import Settings
from pyhb.typing_tester.text_manager import TextManager
from pyhb.typing_tester.cursor import Cursor
from pyhb.typing_tester.dynamic_color import return_color
from pyhb.typing_tester.exp_circle import ExpandingCircles
from pyhb.typing_tester.settings import Settings


def main():
    settings = Settings(screen)

    # Connecting vars
    color = [0, 0, 0]
    bg_color = settings.theme.bg_color
    direction = "up"
    state = "typing_test"

    # Object init
    console = TextManager(
        screen,
        punctuation=settings.preferences["punctuation"],
        color=(255, 255, 255),
        duration=settings.preferences["duration"],
    )
    cursor = Cursor(color, 2)
    expanding_circles = ExpandingCircles(
        init_radius=5, max_radius=40, increment=3, colour=(255, 255, 255), width=10
    )

    # Set theme
    settings.theme.set_theme(settings, console, (0, 0, 0))

    # Flags
    first_frame = True

    # Comparison frame values
    last_screen_center = screen.get_rect().center
    last_theme = settings.theme._id
    current_s_icon_color = (0, 0, 0)
    start = time.perf_counter()

    run = True
    while run:
        clock.tick()

        # Calculating Delta Time
        end = time.perf_counter()

        dt = end - start
        dt *= FPS
        start = time.perf_counter()

        # Mouse pos
        mouse_pos = pygame.mouse.get_pos()

        # Check if screen has been resized
        current_screen_center = screen.get_rect().center
        resize_frame = current_screen_center != last_screen_center
        last_screen_center = screen.get_rect().center

        # Check if theme has been changed
        current_theme = settings.theme._id
        if current_theme != last_theme:
            settings.theme.set_theme(settings, console, current_s_icon_color)
            bg_color = settings.theme.bg_color
            settings.punctuation_txt = settings.font.render("Punctuation", True, settings.theme.font_color)
            settings.theme_txt = settings.font.render("Themes", True, settings.theme.font_color)
            current_s_icon_color = settings.theme.settings_icon_color

        last_theme = settings.theme._id

        # Event handler
        # c_event = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                settings.save_preferences(console.duration)
                run = False

        # Draw background
        screen.fill(bg_color)

        # Dynamic color
        color, direction = return_color(color, direction, dt)

        if state == "typing_test":
            # Text console
            console.update(events, dt, resize_frame)
            console.draw()

            if console.show_results:
                settings.state = "settings"
        elif state == "settings":
            if console.show_results:
                console.get_results()

        # Settings
        settings.update(mouse_pos, events, dt)
        settings.draw(screen, resize_frame, console)

        state = settings.state

        # Click effect
        expanding_circles.update(events, mouse_pos)
        expanding_circles.draw(screen, dt)

        # Cursor
        cursor.colour = color
        cursor.update(*mouse_pos, screen, dt)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
