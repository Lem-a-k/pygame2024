import random

import pygame


class Board:
    # создание поля
    def __init__(self, board_width, board_height):
        self.width = board_width
        self.height = board_height
        self.board = [[0] * self.width for _ in range(self.height)]
        # значения по умолчанию
        self.left = 50
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                r = (self.left + j * self.cell_size + 1,
                     self.top + i * self.cell_size + 1,
                     self.cell_size - 2, self.cell_size - 2)
                pygame.draw.rect(screen, (255, 255, 255), r, 1)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 600
    screen = pygame.display.set_mode(size)

    running = True
    fps = 30
    clock = pygame.time.Clock()
    # MY_EVENT = pygame.USEREVENT + 1
    # pygame.time.set_timer(MY_EVENT, 1000)
    board = Board(4, 3)  # n = 3, m = 4
    board.set_view(20, 50, 100)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == MY_EVENT:
            #     # 123
        # обновление экрана
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
