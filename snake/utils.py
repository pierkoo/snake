from pygame.math import Vector2
from random import randrange, randint
from math import floor

def wrap_position(position, surface, wrapping):
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
