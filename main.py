import config
from config import *

import balloon_shooter
import dodge_the_ball
import stacks


class Button:
    def __init__(self, text, w, h, pos, elevation, flat_style=False):
        # Core attributes
        self.pressed = False
        self.played = False
        self.flat_style = flat_style

        # Location, Resting State (not pressed)
        self.elevation = elevation if not flat_style else 0
        # Location, Pressed State
        self.dynamic_elevation = self.elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (w, h))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (w, h))
        self.bottom_color = '#354B5E'
        # text
        self.text = text
        self.text_surf = font(font_size["Small"]).render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def change_text(self, new_text):
        self.text_surf = font(font_size["Small"]).render(new_text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        border_radius = 0 if self.flat_style else 12

        if not self.flat_style:
            self.bottom_rect.midtop = self.top_rect.midtop
            # Lowers the height of the shadow
            self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
            pygame.draw.rect(display, self.bottom_color,
                             self.bottom_rect, border_radius=border_radius)

        pygame.draw.rect(display, self.top_color,
                         self.top_rect, border_radius=border_radius)
        display.blit(self.text_surf, self.text_rect)
        return self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if not self.played:
                self.played = True
                hover_sound.play()
            self.top_color = '#4B8FD7' if self.flat_style else '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0 if self.flat_style else self.elevation // 2
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    self.change_text(self.text)
                    return True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'
            self.played = False  # Reset the boolean flag when not hovering over the button
        return False


def font(size, font_name=default_font):
    return pygame.font.SysFont(font_name, size)


def show_controls():
    back_button = Button("Back", 100, 40, (width // 2 - 50, height - 80), 4, flat_style=True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        display.fill('#DCDDD8')

        # Render texts
        r_text = font(font_size["Medium"]).render(
            "Press 'r' to restart game", True, '#475F77')
        q_text = font(font_size["Medium"]).render(
            "Press 'q' to quit game", True, '#475F77')
        esc_text = font(font_size["Small"]).render(
            "Press 'esc' to go back to main menu", True, '#475F77')
        about1_text = font(font_size["Large"]).render(
            "Made by:", True, '#475F77')
        about2_text = font(font_size["Smaller"]).render(
            "Mel Mathew Palaña and Jeffrey Mamac", True, '#475F77')

        r_text_rect = r_text.get_rect(center=(width // 2, height // 6))
        q_text_rect = q_text.get_rect(center=(width // 2, height // 4))
        esc_text_rect = esc_text.get_rect(center=(width // 2, height // 2.5))
        about1_text_rect = about1_text.get_rect(center=(width // 2, height - 200))
        about2_text_rect = about2_text.get_rect(center=(width // 2, height - 160))

        display.blit(r_text, r_text_rect)
        display.blit(q_text, q_text_rect)
        display.blit(esc_text, esc_text_rect)
        display.blit(about1_text, about1_text_rect)
        display.blit(about2_text, about2_text_rect)

        # Render back button
        if back_button.draw():
            main(False)

        pygame.display.update()


def show_leaderboard(game_loop=None):
    if not os.path.exists(leaderboard_file):
        leaderboard = []
    else:
        with open(leaderboard_file, "r") as f:
            leaderboard = json.load(f)

    return_button = Button("Back", 100, 40, (width // 2 - 50, height - 80), 4, flat_style=True)
    music_reset = True if game_loop else False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main(music_reset)

        display.fill(black)
        title = font(font_size["Large"]).render("Leaderboard", True, white)
        display.blit(title, (width // 2 - title.get_width() // 2, 30))

        if return_button.draw():
            if game_loop:
                game_loop()
            else:
                main(music_reset)

        if not leaderboard:
            empty_text = font(font_size["Medium"]).render("Leaderboard is empty.", True, white)
            display.blit(empty_text, (width // 2 - empty_text.get_width() // 2, height // 2))
        else:
            for i, entry in enumerate(leaderboard):
                text_format = f"{i + 1}. {entry['name']} - {entry['score']} ({entry['game']})"
                entry_text = font(font_size["Small"]).render(text_format, True, white)
                display.blit(entry_text, (width // 2 - entry_text.get_width() // 2, 110 + i * 40))

        pygame.display.update()


def save_to_leaderboard(name, score, game):
    if not name:
        return

    if not os.path.exists(leaderboard_file):
        with open(leaderboard_file, "w") as f:
            json.dump([], f)

    with open(leaderboard_file, "r") as f:
        leaderboard = json.load(f)

    leaderboard.append({"name": name, "score": score, "game": game})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

    with open(leaderboard_file, "w") as f:
        json.dump(leaderboard, f)


def get_player_name(game_loop=None):
    if config.sound_game_status:
        mixer.music.stop()
        mixer.music.load(os.path.join('assets', 'game_completed.mp3'))
        mixer.music.play()
        mixer.music.set_volume(.5)

    input_box = pygame.Rect(width // 2 - 100, height // 2 - 25, 200, 50)
    enter_button = Button("Enter", 100, 40, (width // 2 + 15, height - 80), 4, flat_style=True)
    cancel_button = Button("Cancel", 100, 40, (width // 2 - 115, height - 80), 4, flat_style=True)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    input_color = color_active
    active = True
    text = ''
    max_len = 16
    button_activation_time = pygame.time.get_ticks() + 100

    while True:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                input_color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return ''
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif len(text) < max_len and event.unicode.isalnum() or event.unicode in ('-', '_'):
                        text += event.unicode

        display.fill(black)
        txt_surface = font(font_size["Small"]).render(text, True, input_color)
        width_txt = max(200, txt_surface.get_width() + 10)
        input_box.w = width_txt
        display.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(display, input_color, input_box, 2)
        instruction = font(font_size["Small"]).render("Enter your name and press Enter:", True, white)
        display.blit(instruction, (width // 2 - instruction.get_width() // 2, height // 2 - 75))

        save_text = font(font_size["Medium"]).render("Add to Leaderboard", True, white)
        save_text_rect = save_text.get_rect(center=(width // 2, 50))
        display.blit(save_text, save_text_rect)

        if current_time >= button_activation_time:
            if enter_button.draw():
                if len(text) > 0:
                    return text
                else:
                    input_color = red

            if cancel_button.draw():
                game_loop()

        pygame.display.flip()
        clock.tick(30)


def show_score(score, text_color=white):
    text = font(font_size["Small"]).render("Score: " + str(score), True, text_color)
    display.blit(text, (10, 10))


def close():
    pygame.quit()
    sys.exit()


def mute_game(btn):
    if config.sound_game_status:
        mixer.music.set_volume(0)
        hover_sound.set_volume(0)
        pop_sound.set_volume(0)
        stack_tower.set_volume(0)
        end_game.set_volume(0)
        gain_point.set_volume(0)
        btn.change_text("Unmute")
    else:
        mixer.music.set_volume(.5)
        hover_sound.set_volume(1)
        pop_sound.set_volume(1)
        stack_tower.set_volume(1)
        end_game.set_volume(1)
        gain_point.set_volume(1)
        btn.change_text("Mute")
        play_menu_music()
    config.sound_game_status = not config.sound_game_status


def check_event(event, game_loop):
    if event.type == pygame.QUIT:
        close()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            close()
        if event.key == pygame.K_r:
            game_loop()
        if event.key == pygame.K_ESCAPE:
            show_confirmation_dialog()


def show_confirmation_dialog():
    confirmation_font = pygame.font.Font(None, 32)
    confirmation_text = confirmation_font.render("Are you sure you want to leave the game?", True, (255, 255, 255))
    confirmation_text_rect = confirmation_text.get_rect(center=(width // 2, height // 2 - 40))

    yes_button = Button("Yes", 100, 40, (width // 2 - 120, height // 2), 4, flat_style=True)
    no_button = Button("No", 100, 40, (width // 2 + 20, height // 2), 4, flat_style=True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display.fill(black)

        display.blit(confirmation_text, confirmation_text_rect)

        if yes_button.draw():
            main()
        if no_button.draw():
            return

        pygame.display.update()


def play_menu_music():
    mixer.music.stop()
    mixer.music.load(menu_music)
    mixer.music.play(-1)
    mixer.music.set_volume(.5)


def btn_pos(index, x=150, y=240, gap=60):
    return x, y + (gap * index)  # Result: (150, 320) for index=1


""" Setup """
btn_width = 200
btn_height = 40
btn_shadow = 5
smaller_btn_width = 80
smaller_btn_height = 50

# Name, Width, Height, Position (X n Y), Elevation (Shadow)
game1_btn = Button('Game 1', btn_width, btn_height, btn_pos(0), btn_shadow)
game2_btn = Button('Game 2', btn_width, btn_height, btn_pos(1), btn_shadow)
game3_btn = Button('Game 3', btn_width, btn_height, btn_pos(2), btn_shadow)
controls_btn = Button('Controls', btn_width, btn_height, btn_pos(3), btn_shadow)
leaderboard_btn = Button('Leaderboard', btn_width, btn_height, btn_pos(4), btn_shadow)
mute_btn = Button("Mute", smaller_btn_width, smaller_btn_height, btn_pos(5, x=400), btn_shadow)

# Title Text
first_text = font(font_size["Large"]).render(
    'Point and Click', True, '#475F77')
second_text = font(font_size["Large"]).render(
    'Games Collection', True, '#475F77')
text_rect_first = first_text.get_rect(center=(width / 2, height / 6))
text_rect_second = second_text.get_rect(center=(width / 2, height / 4))


def main(music_reset=True):
    # Sound verification
    if config.sound_game_status and music_reset:
        play_menu_music()
    elif not config.sound_game_status:
        config.sound_game_status = True
        mute_game(mute_btn)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display.fill('#DCDDD8')
        display.blit(first_text, text_rect_first)
        display.blit(second_text, text_rect_second)
        pygame.display.set_caption('PCG Collection')

        if game1_btn.draw():
            pygame.display.set_caption("Balloon Shooter")
            balloon_shooter.game_loop()
        if game2_btn.draw():
            pygame.display.set_caption("Dodge the Ball")
            dodge_the_ball.game_loop()
        if game3_btn.draw():
            pygame.display.set_caption("Stacks")
            stacks.game_loop()
        if controls_btn.draw():
            pygame.display.set_caption("Controls")
            show_controls()
        if leaderboard_btn.draw():
            pygame.display.set_caption("Leaderboard")
            show_leaderboard()
        if mute_btn.draw():
            mute_game(mute_btn)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
