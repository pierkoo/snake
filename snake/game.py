import pygame
from models import Snake, Food, EnemySnake
from utils import get_random_position, get_mouse_pos
class SnakeGame:
    SPEED_CHANGE = 10


    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.Surface((800, 600))
        self.background.fill((50, 50, 50))
        self.clock = pygame.time.Clock()
        self.wraping = True
        self.play_mode = 3
        self.enemy_snake_grows = True
        self.setup_new_game(self.play_mode)

    def setup_new_game(self, play_mode):
        # play mode: 1 - only snake, 2 - with enemy snake, 3 - only enemy snake
        self.tick = True
        self.play_again = True
        self. direction_chage_flag = False
        self.pause = False
        self.speed = 30
        self.snake = None
        self.enemy_snake = None
        if play_mode == 1 or play_mode == 2:
            self.snake = Snake((300,400), (100, 200, 250))
        if play_mode == 2 or play_mode == 3:
            self.enemy_snake = EnemySnake((500,400), (200,0, 0))
            # for s in range(20):
            #     self.enemy_snake.add_segment((500,400))

        self.food = []
        self.eated_food =[]
        for r in range(1):
            self.spawn_food()

    def spawn_food(self, position = 0):
        if position == 0:
            while True:
                position = get_random_position(self.screen)
                if self.snake:
                    if not self.snake.collides_with(position):
                        break
                else:
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

            if event.type == pygame.KEYDOWN and self.snake and not self. direction_chage_flag:
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause

                if event.key == pygame.K_o:
                    self.change_speed(self.SPEED_CHANGE)
                if event.key == pygame.K_l:
                    self.change_speed(-self.SPEED_CHANGE)
                if event.key == pygame.K_r:
                    self.setup_new_game(self.play_mode)

            if event.type == pygame.MOUSEBUTTONUP:
                print(get_mouse_pos())

    def _process_game_logic(self):
        if not self.pause:
            if self.snake:
                self.snake.move(self.snake.direction, self.screen, self.wraping)

                for s in self.snake.segments:
                    if self.snake.collides_with_itself() or (self.enemy_snake and self.snake.collides_with(self.enemy_snake.segments[0])):
                        self.snake = None
                        break

                for f in self.food:
                    if self.snake.collides_with(f.position):
                        if not f.in_snake:
                            f.in_snake = True
                            self.spawn_food()
                    else:
                        if f.in_snake:
                            self.speed += 0.5
                            self.snake.add_segment(f.position)
                            self.food.remove(f)


                if not self.wraping:
                    if not self.screen.get_rect().collidepoint(self.snake.segments[0]):
                        self.snake = None

                self. direction_chage_flag = False

            ## enemy_snake_handling
            if self.enemy_snake:
                if self.tick:
                    #print("pre")
                    self.enemy_snake.move1(self.food[0].position, self.screen, self.wraping)
                    #print("past")
                #print(len(self.enemy_snake.segments))
                if self.play_mode != 3:
                    self.tick = not self.tick

                for f in self.food:
                    if self.enemy_snake_grows:
                        if self.enemy_snake.collides_with(f.position):
                            if not f.in_snake:
                                f.in_snake = True
                                self.spawn_food()
                        else:
                            if f.in_snake:
                                self.enemy_snake.add_segment(f.position)
                                self.food.remove(f)
                    else:
                        if self.enemy_snake.collides_with(f.position):
                            self.food.remove(f)
                            self.spawn_food()
                for s in self.enemy_snake.segments:
                    if self.enemy_snake.collides_with_itself():
                        print(len(self.enemy_snake.segments))
                        #print(*self.enemy_snake.segments)
                        self.pause=True
                        #self.setup_new_game(self.play_mode)
                        #self.enemy_snake = None
                        break

                # print(self.enemy_snake.segments[0].distance_to(self.food[0].position))


    def _draw(self):
        if not self.pause:
            #print("frame")
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




