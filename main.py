import random

import pygame

pygame.init()
size = width, height = 800, 400
screen = pygame.display.set_mode(size)


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
        self.dx, self.dy = 0, 0
        self.image = pygame.Surface([])
        screen.fill((self.color, self.color, self.color), (*self.pos, 50, 50))

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

    def move(self):
        self.color = (self.color + 1) % 256
        self.pos[0] += self.dx
        self.pos[1] += self.dy



if __name__ == '__main__':
    running = True
    fps = 30
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))

    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    balls = pygame.sprite.Group()

    Border(5, 5, width - 5, 5, horizontal_borders, all_sprites)
    Border(5, height - 5, width - 5, height - 5, horizontal_borders, all_sprites)
    Border(5, 5, 5, height - 5, vertical_borders, all_sprites)
    Border(width - 5, 5, width - 5, height - 5, vertical_borders, all_sprites)

    for i in range(10):
        Ball(20, 100, 100, balls, all_sprites)

    # ms = MovingSquare()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.KEYDOWN:
            #     ms.process_event(event)
            # elif event.type == pygame.KEYUP:
            #     ms.process_event(event)
        # обновление экрана
        # ms.move()
        screen.fill((255, 255, 255),
                    (0, 0, width, height))
        balls.update()
        vertical_borders.draw(screen)
        horizontal_borders.draw(screen)
        balls.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
