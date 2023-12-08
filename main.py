import os
import sys
import random
from copy import deepcopy
from itertools import product

import pygame

pygame.init()
size = width, height = 500, 500
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


class Car(pygame.sprite.Sprite):
    image = load_image("car_tr.png")
    move = 10

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(height - self.rect.height)

    def update(self):
        self.rect = self.rect.move(random.randrange(3) - 1, 0)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(event.pos):
            self.rect = self.rect.move(0, Car.move * (1 if random.randrange(2) else -1))


class CarsGroup(pygame.sprite.Group):
    def process_event(self, event):
        for sprite in self.sprites():
            sprite.process_event(event)


if __name__ == '__main__':
    all_sprites = CarsGroup()

    for _ in range(4):
        Car(all_sprites)

    running = True
    fps = 30
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.process_event(event)

        # обновление экрана
        screen.fill((10, 150, 10))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()

        clock.tick(fps)
    pygame.quit()
