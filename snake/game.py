import pygame
from models import Snake, Food
class SnakeGame:

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display .set_mode((800, 600))
        self.background = pygame.Surface((800, 600))
        self.background.fill((50, 50, 50))
        self.clock = pygame.time.Clock()
        self.play_again = True
        self.pause = False
        self.setup_new_game()

    def setup_new_game(self):
        self.eating = False
        self.eating_prev = False
        self.snake = Snake((400,300))
        self.food = Food((100,100))

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

            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.direction = 1
                if event.key == pygame.K_DOWN:
                    self.snake.direction = 2
                if event.key == pygame.K_LEFT:
                    self.snake.direction = 3
                if event.key == pygame.K_RIGHT:
                    self.snake.direction = 4
                if event.key == pygame.K_SPACE:
                    if self.pause == False:
                        self.pause = True
                    else:
                        self.pause = False

    def _process_game_logic(self):
        self.eating_prev = self.eating
        if not self.pause:
            self.snake.move(self.snake.direction)
        if self.food.collides_with(self.snake.segments[0]) or self.food.collides_with(self.snake.segments[1]) :
            self.eating = True

            #self.snake.add_segment(self.food.position)
        else:
            self.eating = False

        if self.eating == False and self.eating_prev == True:
            print("helo")
            self.snake.add_segment(self.food.position)





    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.food:
            self.food.draw(self.screen)

        self.snake.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(10)

