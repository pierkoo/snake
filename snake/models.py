from pygame.math import Vector2
import pygame
from utils import wrap_position

class GameObject:
    def __init__(self, position):
        self.position = Vector2(position)
        self.sprite = pygame.Surface((20, 20))
        self.height = self.sprite.get_width()

    def draw(self, surface):
        blit_position = self.position #- Vector2(self.height)
        surface.blit(self.sprite, blit_position)



    def collides_with(self, position):
        return self.position == position


class Snake(GameObject):
    def __init__(self, position, color):
        super().__init__(position)
        self.sprite.fill((250, 250, 250))
        self.head_sprite = pygame.Surface((20, 20))
        #self.head_sprite.fill((200, 200, 250))
        self.head_sprite.fill(color)
        self.segments = []
        self.segments.append(position)
        self.direction = 1

    def draw(self, surface):
        for s in self.segments:
            if self.segments.index(s) == 0:
                blit_position = s #- Vector2(self.height)
                surface.blit(self.head_sprite, blit_position)
            else:
                blit_position = s #- Vector2(self.height)
                surface.blit(self.sprite, blit_position)

    def move(self, direction, surface, wrapping):
        # 1-up 2-down 3-left 4-right

        if direction == 1:
            new_position=wrap_position(self.segments[0] - Vector2(0, self.height), surface, wrapping)
        if direction == 2:
            new_position=wrap_position(self.segments[0] + Vector2(0, self.height), surface ,wrapping)
        if direction == 3:
            new_position=wrap_position(self.segments[0] - Vector2(self.height, 0), surface ,wrapping)
        if direction == 4:
            new_position=wrap_position(self.segments[0] + Vector2( self.height, 0), surface ,wrapping)

        self.segments.insert(0,new_position)
        self.segments.pop()


    def add_segment(self, position):
        self.segments.append(position)

    def collides_with(self, position):
        if position in self.segments:
            return True
        else:
            return False


    def collides_with_itself(self):
        if self.segments[0] in self.segments[1:]:
            return True
        else:
            return False


class Food(GameObject):
    def __init__(self, position):
        super().__init__(position)
        self.sprite.fill((0, 250, 100))
        self.in_snake = False

    def eaten(self):
        pass

class EnemySnake(Snake):
    def __init__(self, position, color):
        super().__init__(position, color)

    def get_direction(self, target_position, surface, wrapping):
        position_diff = Vector2(self.segments[0])-target_position
        abs_position_diff = (abs(position_diff[0]), abs(position_diff[1]))
        max_position_diff=max(abs_position_diff)
        index = abs_position_diff.index(max_position_diff)
        stop = False
        if index == 0:
            if position_diff[0] > 0:
                self.direction = 3
            elif position_diff[0] < 0:
                self.direction = 4
            else:
                stop = True
        if index == 1:
            if position_diff[1] > 0:
                self.direction = 1
            elif position_diff[1] < 0:
                self.direction = 2
            else:
                stop = True
        if not stop:
            self.move(self.direction, surface, wrapping)


        #print(self.position.distance_to(target_position))




