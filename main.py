import random
from copy import deepcopy
from itertools import product

import pygame


class Board:
    # создание поля
    def __init__(self, board_width, board_height):
        self.board_updating = False
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
                r = (self.left + j * self.cell_size,
                     self.top + i * self.cell_size,
                     self.cell_size, self.cell_size)
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), r)
                pygame.draw.rect(screen, (255, 255, 255), r, 1)

    def get_cell(self, mouse_pos):
        row = (mouse_pos[1] - self.top) // self.cell_size
        col = (mouse_pos[0] - self.left) // self.cell_size
        return (row, col) if (0 <= row < self.height and
                              0 <= col < self.width) else None

    def on_click(self, cell):
        self.board[cell[0]][cell[1]] ^= 1

    def process_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def update(self):
        new_board = deepcopy(self.board)
        for i in range(self.height):
            for j in range(self.width):
                neighbours = 0
                for di, dj in product((-1, 0, 1), repeat=2):
                    if di == dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        neighbours += self.board[ni][nj]
                if neighbours <= 1 or neighbours > 3:
                    new_board[i][j] = 0
                elif neighbours == 3:
                    new_board[i][j] = 1
        self.board = new_board


if __name__ == '__main__':
    pygame.init()
    size = width, height = 900, 600
    screen = pygame.display.set_mode(size)

    running = True
    fps = 30
    clock = pygame.time.Clock()
    BOARD_UPDATE = pygame.USEREVENT + 1

    board = Board(40, 25)
    board.set_view(10, 10, 20)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == BOARD_UPDATE:
                board.update()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.process_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.time.set_timer(BOARD_UPDATE, 0 if board.board_updating else 1000)
                    board.board_updating = not board.board_updating
        # обновление экрана
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
