import config
from config import *
import main
# ETO 3RD TEST
background = lightBlue

margin = 100
lowerBound = 60

maxTimeInSeconds = 30
score = 0
remaining_time = 0


# Balloon Class
class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.probPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice(colors)
        self.pop_animation = False
        self.pop_animation_radius = 0

    # Move balloon around the Screen
    def move(self):
        direct = random.choice(self.probPool)

        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    # Show/Draw the balloon
    def show(self):
        if self.pop_animation:
            center_x = int(self.x + self.a / 2)
            center_y = int(self.y + self.b / 2)
            pygame.draw.circle(display, white, (center_x, center_y), self.pop_animation_radius, 5)
            self.pop_animation_radius += 5
            if self.pop_animation_radius > self.a:
                self.reset()
        else:
            pygame.draw.line(display, darkBlue, (self.x + self.a / 2, self.y + self.b),
                             (self.x + self.a / 2, self.y + self.b + self.length))
            pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
            pygame.draw.ellipse(display, self.color, (self.x + self.a / 2 - 5, self.y + self.b - 3, 10, 10))

    # Check if Balloon is popped
    def burst(self):
        global score
        pos = pygame.mouse.get_pos()

        if on_balloon(self.x, self.y, self.a, self.b, pos):
            if sound_game_status:
                pop_sound.play()
            score += 1
            self.pop_animation = True

    # Reset the Balloon
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed -= 0.002
        self.probPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue])
        self.pop_animation = False
        self.pop_animation_radius = 0


balloons = []
noBalloon = 10


def create_balloons():
    balloons.clear()
    for i in range(noBalloon):
        obj = Balloon(random.choice([1, 1, 2, 2, 2, 2, 3, 3, 3, 4]))
        balloons.append(obj)


def on_balloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False


# show the location of Mouse
def pointer():
    pos = pygame.mouse.get_pos()
    right = 25
    left = 20
    player_color = lightGreen
    for i in range(noBalloon):
        if on_balloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            player_color = red
    pygame.draw.ellipse(display, player_color, (pos[0] - right / 2, pos[1] - right / 2, right, right), 4)
    pygame.draw.line(display, player_color, (pos[0], pos[1] - left / 2), (pos[0], pos[1] - left), 4)
    pygame.draw.line(display, player_color, (pos[0] + left / 2, pos[1]), (pos[0] + left, pos[1]), 4)
    pygame.draw.line(display, player_color, (pos[0], pos[1] + left / 2), (pos[0], pos[1] + left), 4)
    pygame.draw.line(display, player_color, (pos[0] - left / 2, pos[1]), (pos[0] - left, pos[1]), 4)


def lower_platform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))


def show_timer():
    timer_text = main.font(25).render("Remaining Time : " + str(remaining_time), True, white)
    display.blit(timer_text, (170, height - lowerBound + 25))


def game_over():
    go_text = main.font(50).render("Game Over", True, darkGray)
    click_to_continue_text = main.font(30).render("Click to continue", True, darkGray)

    go_rect = go_text.get_rect(center=(width // 2, height // 2 - 50))
    click_to_continue_rect = click_to_continue_text.get_rect(center=(width // 2, height // 2 + 20))

    display.blit(go_text, go_rect.topleft)
    display.blit(click_to_continue_text, click_to_continue_rect.topleft)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.time.wait(300)
                player_name = main.get_player_name(game_loop)
                main.save_to_leaderboard(player_name, score, "Balloon Shooter")
                main.show_leaderboard(game_loop)


def game_loop():
    global score, remaining_time

    if config.sound_game_status:
        mixer.music.stop()
        mixer.music.load(balloon_shooter_music)
        mixer.music.play(-1)
        mixer.music.set_volume(.5)

    # Reset
    score = 0
    remaining_time = maxTimeInSeconds
    loop = True

    create_balloons()

    while loop:
        if remaining_time > 0:
            display.fill(background)

            for i in range(noBalloon):
                balloons[i].show()

            pointer()

            for i in range(noBalloon):
                balloons[i].move()
        else:
            game_over()

        for event in pygame.event.get():
            main.check_event(event, game_loop)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0

            if event.type == pygame.USEREVENT:
                if remaining_time > 0:
                    remaining_time -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(noBalloon):
                    balloons[i].burst()
                if remaining_time <= 0:
                    score = 0
                    game_loop()

        lower_platform()
        main.show_score(score, darkGray)
        show_timer()
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
