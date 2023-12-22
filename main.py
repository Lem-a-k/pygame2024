import random
import os
import sys

import pygame

MENU = 'menu'
GAME = 'game'
PAUSE = 'pause'

pygame.init()
size = width, height = 800, 400
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, *groups):
        super().__init__(*groups)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface([max(x2 - x1, 1), max(y2 - y1, 1)])
        self.rect = pygame.Rect(x1, y1, max(x2 - x1, 1), max(y2 - y1, 1))


class MovingSquare(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.color = 0
        self.pos = [10, 10]
        self.size = 50
        self.dx, self.dy = 0, 0
        self.image = pygame.Surface([self.size, self.size], pygame.SRCALPHA, 32)
        self.image.fill((self.color, self.color, self.color))
        self.rect = pygame.Rect(*self.pos, self.size, self.size)

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.dx = 10
            elif event.key == pygame.K_LEFT:
                self.dx = -10
            elif event.key == pygame.K_UP:
                self.dy = -10
            elif event.key == pygame.K_DOWN:
                self.dy = 10
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                self.dx = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                self.dy = 0

    def update(self):
        self.color = (self.color + 1) % 256
        self.pos[0] += self.dx
        self.pos[1] += self.dy
        self.image.fill((self.color, self.color, self.color))
        self.rect = pygame.Rect(*self.pos, self.size, self.size)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, *groups):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


if __name__ == '__main__':
    running = True
    fps = 20
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))

    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    square = pygame.sprite.GroupSingle()
    dragon = pygame.sprite.GroupSingle()

    Border(5, 5, width - 5, 5, horizontal_borders, all_sprites)
    Border(5, height - 5, width - 5, height - 5, horizontal_borders, all_sprites)
    Border(5, 5, 5, height - 5, vertical_borders, all_sprites)
    Border(width - 5, 5, width - 5, height - 5, vertical_borders, all_sprites)

    for i in range(10):
        Ball(20, 100, 100, balls, all_sprites)

    state = MENU
    ms = MovingSquare(square, all_sprites)
    drag = AnimatedSprite(load_image("pygame-8-1.png", -1), 8, 2,
                          width - 150, height - 150,
                          dragon, all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state == GAME:
                    if event.key == pygame.K_ESCAPE:
                        state = MENU
                    elif event.key == pygame.K_SPACE:
                        state = PAUSE
                    else:
                        ms.process_event(event)
                elif state == MENU:
                    if event.key == pygame.K_SPACE:
                        state = GAME
                elif state == PAUSE:
                    if event.key == pygame.K_SPACE:
                        state = GAME
                    elif event.key == pygame.K_ESCAPE:
                        state = MENU
            elif event.type == pygame.KEYUP:
                if state == GAME:
                    ms.process_event(event)
        # обновление экрана
        screen.fill((255, 255, 255),
                    (0, 0, width, height))
        if state == GAME:
            balls.update()
            square.update()
            dragon.update()
            vertical_borders.draw(screen)
            horizontal_borders.draw(screen)
            balls.draw(screen)
            square.draw(screen)
            dragon.draw(screen)
        elif state == PAUSE:
            vertical_borders.draw(screen)
            horizontal_borders.draw(screen)
            balls.draw(screen)
            square.draw(screen)
        elif state == MENU:
            intro_text = ["ЗАСТАВКА", "",
                          "Пробел - запуск игры и старт/пауза",
                          "Esc - выход в меню",
                          "",
                          "Если в правилах несколько строк,",
                          "приходится выводить их построчно"]

            fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('black'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
