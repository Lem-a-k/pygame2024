import random

import pygame


class Board:
    # создание поля
    def __init__(self, board_width, board_height):
        self.width = board_width
        self.height = board_height
        self.board = [[None] * self.width for _ in range(self.height)]
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
                r = (self.left + j * self.cell_size,
                     self.top + i * self.cell_size,
                     self.cell_size, self.cell_size)
                # r_b = (r[0] + 1, r[1] + 1, r[2] - 2, r[3] - 2)
                if self.board[i][j] is not None:
                    # r_inner = (r_b[0] + 1, r_b[1] + 1,
                    #            r_b[2] - 2, r_b[3] - 2)
                    pygame.draw.rect(screen, self.board[i][j], r)
                pygame.draw.rect(screen, (255, 255, 255), r, 1)


    def get_cell(self, mouse_pos):
        row = (mouse_pos[1] - self.top) // self.cell_size
        col = (mouse_pos[0] - self.left) // self.cell_size
        return (row, col) if (0 <= row < self.height and
                              0 <= col < self.width) else None

    def on_click(self, cell):
        for i in range(self.height):
            self.board[i][cell[1]] = (random.randint(0, 255),
                                      random.randint(0, 255),
                                      random.randint(0, 255))
        for j in range(self.width):
            self.board[cell[0]][j] = (random.randint(0, 255),
                                      random.randint(0, 255),
                                      random.randint(0, 255))

    def process_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 600
    screen = pygame.display.set_mode(size)

    running = True
    fps = 30
    clock = pygame.time.Clock()
    # MY_EVENT = pygame.USEREVENT + 1
    # pygame.time.set_timer(MY_EVENT, 1000)
    board = Board(7, 5)  # n = 5, m = 7
    board.set_view(20, 50, 100)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == MY_EVENT:
            #     # 123
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.process_click(event.pos)
        # обновление экрана
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
