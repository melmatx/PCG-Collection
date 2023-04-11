import config
from config import *
import main

background = navyBlue

colorIndex = 0

brickH = 10
brickW = 100

speed = 3
score = 0


# Single Brick Class
class Brick:
    def __init__(self, x, y, br_color, br_speed):
        self.x = x
        self.y = y
        self.w = brickW
        self.h = brickH
        self.color = br_color
        self.speed = br_speed

    def draw(self):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h))

    def move(self):
        self.x += self.speed
        if self.x > width:
            self.speed *= -1
        if self.x + self.w < 1:
            self.speed *= -1


# Complete Stack
class Stack:
    def __init__(self):
        global colorIndex
        self.stack = []
        self.initSize = 25
        for i in range(self.initSize):
            new_brick = Brick(width / 2 - brickW / 2, height - (i + 1) * brickH, color[colorIndex], 0)
            colorIndex += 1
            self.stack.append(new_brick)

    def show(self):
        for i in range(self.initSize):
            self.stack[i].draw()

    def move(self):
        for i in range(self.initSize):
            self.stack[i].move()

    def add_new_brick(self):
        global colorIndex, speed

        if colorIndex >= len(color):
            colorIndex = 0

        y = self.peek().y
        if score > 50:
            speed += 0
        elif score % 5 == 0:
            speed += 1

        new_brick = Brick(width, y - brickH, color[colorIndex], speed)
        colorIndex += 1
        self.initSize += 1
        self.stack.append(new_brick)

    def peek(self):
        return self.stack[self.initSize - 1]

    def push_to_stack(self):
        global brickW, score
        b = self.stack[self.initSize - 2]
        b2 = self.stack[self.initSize - 1]
        if b2.x <= b.x and not (b2.x + b2.w < b.x):
            if sound_game_status:
                stack_tower.play()
            self.stack[self.initSize - 1].w = self.stack[self.initSize - 1].x + self.stack[self.initSize - 1].w - b.x
            self.stack[self.initSize - 1].x = b.x
            if self.stack[self.initSize - 1].w > b.w:
                self.stack[self.initSize - 1].w = b.w
            self.stack[self.initSize - 1].speed = 0
            score += 1
        elif b.x <= b2.x <= b.x + b.w:
            if sound_game_status:
                stack_tower.play()
            self.stack[self.initSize - 1].w = b.x + b.w - b2.x
            self.stack[self.initSize - 1].speed = 0
            score += 1
        else:
            game_over()

        for i in range(self.initSize):
            self.stack[i].y += brickH

        brickW = self.stack[self.initSize - 1].w


# Game Over
def game_over():
    game_over_text = main.font(60).render("Game Over!", True, white)
    click_to_continue_text = main.font(40).render("Click to continue", True, white)

    game_over_rect = game_over_text.get_rect(center=(width / 2, height / 2 - 80))
    click_to_continue_rect = click_to_continue_text.get_rect(center=(width / 2, height / 2 + 20))

    loop = True

    if sound_game_status:
        end_game.play()

    while loop:
        for event in pygame.event.get():
            main.check_event(event, game_loop)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player_name = main.get_player_name(game_loop)
                main.save_to_leaderboard(player_name, score, "Stacks")
                main.show_leaderboard(game_loop)

        display.blit(game_over_text, game_over_rect.topleft)
        display.blit(click_to_continue_text, click_to_continue_rect.topleft)

        pygame.display.update()
        clock.tick()


# The Main Game Loop
def game_loop():
    global brickW, brickH, score, colorIndex, speed

    if config.sound_game_status:
        mixer.music.stop()
        mixer.music.load(stacks_music)
        mixer.music.play(-1)
        mixer.music.set_volume(.5)

    # Reset
    score = 0
    colorIndex = 0
    speed = 3
    loop = True

    brickH = 10
    brickW = 100

    stack = Stack()
    stack.add_new_brick()

    while loop:
        for event in pygame.event.get():
            main.check_event(event, game_loop)

            if event.type == pygame.MOUSEBUTTONDOWN:
                stack.push_to_stack()
                stack.add_new_brick()

        display.fill(background)

        stack.move()
        stack.show()

        main.show_score(score)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    game_loop()
