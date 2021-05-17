from pygame.math import Vector2
from random import randrange, randint
from math import floor
from pygame import mouse

def wrap_position(position, surface, wrapping = 1):
    if wrapping:
        x, y = position
        w, h = surface.get_size()
        return Vector2(x % w, y % h)
    else:
        return position

def get_random_position(surface):
    return Vector2(
        randrange((surface.get_width()/20)) * 20,
        randrange((surface.get_height()/20)) * 20,
    )

def get_mouse_pos():
    return  [int(a / 20)*20 for a in mouse.get_pos()]

