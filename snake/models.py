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
        self.segments.append(self.position)
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

    # concept?
    # def eat(self,food, callback_function):

    #     if  self.collides_with(food.position):
    #         if not food.in_snake:
    #             food.in_snake = True
    #             callback_function
    #     else:
    #         if food.in_snake:
    #             self.speed += 0.5
    #             self.add_segment(food.position)
    #             f.remove(food)



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
        self.prev_index = 0
        self.new_positions = []


    def get_direction(self, target_position, surface, wrapping):

        position_diff = Vector2(self.segments[0])-target_position
        abs_position_diff = (abs(position_diff[0]), abs(position_diff[1]))
        max_position_diff = max(abs_position_diff)

        index = abs_position_diff.index(max_position_diff)
        if index != self.prev_index and abs_position_diff[self.prev_index] !=0:
            index = self.prev_index

        #print(position_diff, " | ", abs_position_diff, " | ", max_position_diff ," | ", index )

        if index == 0:
            if position_diff[0] > 0:
                self.direction = self.check_direction(3)
            elif position_diff[0] < 0:
                self.direction = self.check_direction(4)

        if index == 1:
            if position_diff[1] > 0:
                self.direction = self.check_direction(1)
            elif position_diff[1] < 0:
                self.direction = self.check_direction(2)

        self.prev_index = index

    def check_direction(self, new_direction):
        ''' Prevenst changing direction for opposite '''

        # print(self.direction, ' | ', new_direction)

        if new_direction == 1 and self.direction == 2:
            return 3
        elif new_direction == 2 and self.direction == 1:
            return  4
        elif new_direction == 3 and self.direction == 4:
            return  1
        elif new_direction == 4 and self.direction == 3:
            return  2
        else:
            return new_direction

    def get_new_postion(self, surface, wrapping):
        # 1-up 2-down 3-left 4-right
        if self.direction > 4:
            self.direction = 1
        if self.direction == 1:
            new_position=wrap_position(self.segments[0] - Vector2(0, self.height), surface, wrapping)
        if self.direction == 2:
            new_position=wrap_position(self.segments[0] + Vector2(0, self.height), surface ,wrapping)
        if self.direction == 3:
            new_position=wrap_position(self.segments[0] - Vector2(self.height, 0), surface ,wrapping)
        if self.direction == 4:
            new_position=wrap_position(self.segments[0] + Vector2( self.height, 0), surface ,wrapping)
        return new_position

    # def check_postion(self, new_position):
    #     if self.collides_with(new_position):
    #         return False
    #     return True

    def get_new_direction(self,new_position):
        colliding_segment_index = self.segments.index(new_position)
        if colliding_segment_index + 1 < len(self.segments):
            next_segment = self.segments[colliding_segment_index  + 1 ]
            if self.segments[0].y == new_position.y:
                if self.segments[0].y - next_segment.y > 0:
                    self.direction = 1
                else:
                    self.direction = 2
            else:
                if self.segments[0].x - next_segment.x > 0:
                    self.direction = 3
                else:
                    self.direction = 4
        else:
            next_segment = self.segments[colliding_segment_index  - 1 ]
            if self.segments[0].y == new_position.y:
                if self.segments[0].y - next_segment.y < 0:
                    self.direction = 1
                else:
                    self.direction = 2
            else:
                if self.segments[0].x - next_segment.x < 0:
                    self.direction = 3
                else:
                    self.direction = 4




        print(self.segments[0], ' | ', new_position, ' | ', next_segment, ' | ',self.direction)



    def another_segment_in_proximity(self):
        for s in self.segments[2:]:
            if self.segments[0].distance_to(s) == 20:
                print("upsi")
                return True
        return False

    def move(self, target_position, surface, wrapping):
        self.get_direction(target_position, surface, wrapping)
        while True:
            new_position = self.get_new_postion( surface, wrapping)
            if not self.collides_with(new_position):
                break
            else:
                self.get_new_direction(new_position)
                #self.direction += 1
                #print("upsi | ", self.direction

        self.another_segment_in_proximity()
        self.segments.insert(0,new_position)
        self.segments.pop()

    def move1(self, target_position, surface, wrapping):
        self.calculate_possible_new_positions(surface)
        self.check_for_looping()
        self.select_closes_position(target_position)



        self.segments.insert(0,self.new_position)
        self.segments.pop()
        ''' self.calculate_possible_new_positions()
                self.check_new_postions_for_self)collision()
                # should get at least 2 possible new positions otherwise its already lost
                self.check_new_positions_for_looping
                self.select_closest_postion() - selects new_postion closestto food
                '''

    def calculate_possible_new_positions(self, surface):
        self.new_positions = []
        self.new_positions.append(wrap_position(self.segments[0]+(20,0),surface))
        self.new_positions.append(wrap_position(self.segments[0]+(0,20),surface))
        self.new_positions.append(wrap_position(self.segments[0]+(-20,0),surface))
        self.new_positions.append(wrap_position(self.segments[0]+(0,-20),surface))

        if len(self.segments)>1:
            self.new_positions.remove(self.segments[1])

        # to be checked if slicing is ok ??
        for s in self.segments:
            if s in self.new_positions:
                self.new_positions.remove(s)
        #print(f"current {self.segments[0]}")
        #print(f"neeck {self.segments[1]}")
        #print("New positions")
        # for p in self.new_positions:
        #     print(p)

    def select_closes_position(self, target_position):
        distance_to_target = []
        for n_p in self.new_positions:
            distance_to_target.append(n_p.distance_to(target_position))
            self.new_position =  self.new_positions[distance_to_target.index(min(distance_to_target))]
        # print(f"NEW: {self.new_position}")

    def check_for_looping(self):
        print("----")

        if len(self.segments) > 1:
            print(self.segments[0],'  ', self.segments[1])
            if self.segments[0].x == self.segments[1].x:
                front=Vector2(self.segments[0].x,self.segments[0].y + (self.segments[0].y - self.segments[1].y ))
            else:
                front=Vector2(self.segments[0].x + (self.segments[0].x - self.segments[1].x ),self.segments[0].y)
            print(front)





