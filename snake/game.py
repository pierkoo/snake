import pygame
from models import Snake, Food, EnemySnake
from utils import get_random_position
class SnakeGame:
    SPEED_CHANGE = 10

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface((800, 600))
        self.background.fill((50, 50, 50))
        self.clock = pygame.time.Clock()
        self.wraping = True
        self.setup_new_game()

    def setup_new_game(self):
        self.tick = False
        self.play_again = True
        self. direction_chage_flag = False
        self.pause = False
        self.speed = 10
        self.snake = Snake((300,400), (100, 200, 250))
        self.enemy_snake = EnemySnake((500,400), (200,0, 0))
        self.food = []
        self.eated_food =[]
        for r in range(1):
            self.spawn_food()


    def spawn_food(self, position = 0):
        if position == 0:
            while True:
                position = get_random_position(self.screen)
                if not self.snake.collides_with(position):
                    break
        self.food.insert(0,Food(position))

    def change_speed(self, speed_change):
        self.speed += speed_change
        if self.speed < 10:
            self.speed = 10

    def main_loop(self):
        while self.play_again == True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Snake")


    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

            if event.type ==pygame.KEYDOWN and self.snake and not self. direction_chage_flag:
                if event.key == pygame.K_w and self.snake.direction != 2 :
                    self.snake.direction = 1
                    self. direction_chage_flag = True
                if event.key == pygame.K_s and self.snake.direction != 1 :
                    self.snake.direction = 2
                    self. direction_chage_flag = True
                if event.key == pygame.K_a and self.snake.direction != 4 :
                    self.snake.direction = 3
                    self. direction_chage_flag = True
                if event.key == pygame.K_d and self.snake.direction != 3 :
                    self.snake.direction = 4
                    self. direction_chage_flag = True

            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.pause == False:
                        self.pause = True
                    else:
                        self.pause = False
                if event.key == pygame.K_o:
                    self.change_speed(self.SPEED_CHANGE)
                if event.key == pygame.K_l:
                    self.change_speed(-self.SPEED_CHANGE)
                if event.key == pygame.K_r:
                    self.setup_new_game()

    def _process_game_logic(self):

        if not self.pause and self.snake:
            self.snake.move(self.snake.direction, self.screen, self.wraping)
            if  self.tick:
                self.enemy_snake.get_direction(self.food[0].position, self.screen, self.wraping)

        if self.snake:
            for s in self.snake.segments:
                if self.snake.collides_with_itself() or self.snake.collides_with(self.enemy_snake.segments[0]):
                    self.snake = None
                    break


        for f in self.food:
            if self.snake  and self.snake.collides_with(f.position):
                if not f.in_snake:
                    f.in_snake = True
                    self.spawn_food()
            else:
                if self.snake and  f.in_snake:
                    self.speed += 0.5
                    self.snake.add_segment(f.position)
                    self.food.remove(f)
            if self.enemy_snake and self.enemy_snake.collides_with(f.position):
                self.food.remove(f)
                self.spawn_food()




        if not self.wraping and self.snake:
            #print ((self.snake.segments[0]))
            if (self.snake.segments[0].x<0
                or self.snake.segments[0].x> self.screen.get_width()
                or self.snake.segments[0].y<0
                or self.snake.segments[0].y> self.screen.get_height()
            ) :
                self.snake= None
        self. direction_chage_flag = False

        self.tick = not self.tick
    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.food:
            for f in self.food:
                f.draw(self.screen)
        if self.snake:
            self.snake.draw(self.screen)

        if self.enemy_snake:
            self.enemy_snake.draw(self.screen)


        self.clock.tick(self.speed)

        pygame.display.flip()




