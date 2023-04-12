import os
import sys
import random
import json
from math import *

import pygame
from pygame import mixer

# Window Size
width = 500
height = 600

# Initialize PyGame
pygame.init()
display = pygame.display.set_mode((width, height))

# PyGame Timer
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Font
default_font = "Agency FB"
font_size = {"Smaller": 25, "Small": 30, "Medium": 40, "Large": 60}

# Color Codes
color = [(120, 40, 31), (148, 49, 38), (176, 58, 46), (203, 67, 53), (231, 76, 60), (236, 112, 99), (241, 148, 138),
         (245, 183, 177), (250, 219, 216), (253, 237, 236),
         (254, 249, 231), (252, 243, 207), (249, 231, 159), (247, 220, 111), (244, 208, 63), (241, 196, 15),
         (212, 172, 13), (183, 149, 11), (154, 125, 10), (125, 102, 8),
         (126, 81, 9), (156, 100, 12), (185, 119, 14), (202, 111, 30), (214, 137, 16), (243, 156, 18), (245, 176, 65),
         (248, 196, 113), (250, 215, 160), (253, 235, 208), (254, 245, 231),
         (232, 246, 243), (162, 217, 206), (162, 217, 206),
         (115, 198, 182), (69, 179, 157), (22, 160, 133),
         (19, 141, 117), (17, 122, 101), (14, 102, 85),
         (11, 83, 69),
         (21, 67, 96), (26, 82, 118), (31, 97, 141),
         (36, 113, 163), (41, 128, 185), (84, 153, 199),
         (127, 179, 213), (169, 204, 227), (212, 230, 241),
         (234, 242, 248),
         (251, 238, 230), (246, 221, 204), (237, 187, 153),
         (229, 152, 102), (220, 118, 51), (211, 84, 0),
         (186, 74, 0), (160, 64, 0), (135, 54, 0),
         (110, 44, 0)
         ]

# Colors
white = (230, 230, 230)
lightBlue = (174, 214, 241)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
darkBlue = (21, 67, 96)
green = (35, 155, 86)
yellow = (244, 208, 63)
lightYellow = (249, 231, 159)
blue = (46, 134, 193)
navyBlue = (23, 32, 42)
purple = (155, 89, 182)
orange = (243, 156, 18)
black = (30, 30, 30)
bluer = (58, 110, 165)

# Color list
colors = [red, green, purple, orange, yellow, blue]

# Files
curr_dir = os.getcwd()
path_to_assets = os.path.join(curr_dir, 'assets')
leaderboard_file = "leaderboard.json"

# Sounds
sound_game_status = True
menu_music = os.path.join(path_to_assets, 'omw-to-beat-the-big-bad.wav')  # BG music
balloon_shooter_music = os.path.join(path_to_assets, 'Caketown_1.mp3')  # BG music
dodge_the_ball_music = os.path.join(path_to_assets, 'Orbital Colossus.mp3')  # BG music
stacks_music = os.path.join(path_to_assets, '8Bit Title Screen.mp3')
hover_sound = mixer.Sound(os.path.join(path_to_assets, 'hbutton_sound.mp3'))
pop_sound = mixer.Sound(os.path.join(path_to_assets, 'pop-39222.mp3'))
stack_tower = mixer.Sound(os.path.join(path_to_assets, 'stack.mp3'))
end_game = mixer.Sound(os.path.join(path_to_assets, 'end.mp3'))
gain_point = mixer.Sound(os.path.join(path_to_assets, 'point.mp3'))
error_sound = mixer.Sound(os.path.join(path_to_assets, 'error.mp3'))



if __name__ == "__main__":
    print("=============================================")
    print("ERROR: Run main.py to start PCG Collection!")
    print("=============================================")
