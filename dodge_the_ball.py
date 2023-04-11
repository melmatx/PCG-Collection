import config
from config import *
import main

player_color = lightYellow
background = navyBlue

score = 0


class Ball:
    def __init__(self, radius, speed):
        self.x = 0
        self.y = 0
        self.r = radius
        self.color = 0
        self.speed = speed
        self.angle = 0

    def create_ball(self):
        min_distance = 100
        mouse_pos = pygame.mouse.get_pos()
        while True:
            self.x = random.randint(self.r, width - self.r)
            self.y = random.randint(self.r, height - self.r)
            if self.check_distance(mouse_pos) >= min_distance:
                break
        self.color = random.choice(colors)
        self.angle = random.randint(-180, 180)

    def move(self):
        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))

        if self.x < self.r or self.x + self.r > width:
            self.angle = 180 - self.angle
        if self.y < self.r or self.y + self.r > height:
            self.angle *= -1

    def draw(self):
        pygame.draw.ellipse(display, self.color, (self.x - self.r, self.y - self.r, self.r * 2, self.r * 2))

    def collision(self, radius):
        pos = pygame.mouse.get_pos()

        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5

        if distance <= self.r + radius:
            game_over()

    def check_distance(self, mouse_pos):
        distance = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5
        return distance


class Target:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 20
        self.h = self.w

    def generate_new_coord(self):
        self.x = random.randint(self.w, width - self.w)
        self.y = random.randint(self.h, height - self.h)

    def draw(self):
        enemy_color = random.choice(colors)

        pygame.draw.rect(display, enemy_color, (self.x, self.y, self.w, self.h))


def game_over():
    game_over_text = main.font(100).render("Game Over!", True, (230, 230, 230))
    click_to_continue_text = main.font(50).render("Click to continue", True, (230, 230, 230))

    game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))
    click_to_continue_rect = click_to_continue_text.get_rect(center=(width // 2, height // 2 + 50))

    loop = True

    if sound_game_status:
        end_game.play()

    while loop:
        for event in pygame.event.get():
            main.check_event(event, game_loop)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player_name = main.get_player_name(game_loop)
                main.save_to_leaderboard(player_name, score, "Dodge the Ball")
                main.show_leaderboard(game_loop)

        display.fill(background)

        display.blit(game_over_text, game_over_rect.topleft)
        display.blit(click_to_continue_text, click_to_continue_rect.topleft)
        main.show_score(score)

        pygame.display.update()
        clock.tick()


def check_collision(target, d, obj_target):
    pos = pygame.mouse.get_pos()
    distance = ((pos[0] - target[0] - obj_target.w) ** 2 + (pos[1] - target[1] - obj_target.h) ** 2) ** 0.5

    if distance <= d + obj_target.w:
        return True
    return False


def draw_player_pointer(pos, r):
    pygame.draw.ellipse(display, player_color, (pos[0] - r, pos[1] - r, 2 * r, 2 * r))


def game_loop():
    global score

    if config.sound_game_status:
        mixer.music.stop()
        mixer.music.load(dodge_the_ball_music)
        mixer.music.play(-1)
        mixer.music.set_volume(.2)

    p_radius = 10

    # Reset
    score = 0
    balls = []
    loop = True

    for i in range(1):
        new_ball = Ball(p_radius + 2, 5)
        new_ball.create_ball()
        balls.append(new_ball)

    target = Target()
    target.generate_new_coord()

    while loop:
        for event in pygame.event.get():
            main.check_event(event, game_loop)

        display.fill(background)

        for i in range(len(balls)):
            balls[i].move()

        for i in range(len(balls)):
            balls[i].draw()

        for i in range(len(balls)):
            balls[i].collision(p_radius)

        player_pos = pygame.mouse.get_pos()
        draw_player_pointer((player_pos[0], player_pos[1]), p_radius)

        collide = check_collision((target.x, target.y), p_radius, target)

        if collide:
            if sound_game_status:
                gain_point.play()
            score += 1
            target.generate_new_coord()
        elif score == 2 and len(balls) == 1:
            new_ball = Ball(p_radius + 2, 5)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()
        elif score == 5 and len(balls) == 2:
            new_ball = Ball(p_radius + 2, 6)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()
        elif score == 10 and len(balls) == 3:
            new_ball = Ball(p_radius + 2, 7)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()
        elif score == 15 and len(balls) == 4:
            new_ball = Ball(p_radius + 2, 8)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()
        elif score == 20 and len(balls) == 5:
            new_ball = Ball(p_radius + 2, 9)
            new_ball.create_ball()
            balls.append(new_ball)
            target.generate_new_coord()

        target.draw()
        main.show_score(score)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
