import random

import pygame

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)

    running = True
    fps = 30
    clock = pygame.time.Clock()
    MY_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MY_EVENT, 1000)
    special_color = 0
    pos = [10, 10]
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pos[0] += 10
                elif event.key == pygame.K_LEFT:
                    pos[0] -= 10
                elif event.key == pygame.K_UP:
                    pos[1] -= 10
                elif event.key == pygame.K_DOWN:
                    pos[1] += 10
            if event.type == MY_EVENT:
                screen.fill((0, 0, 0),
                            (0, 0, width, height))
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for i in range(100):
                    screen.fill(color,
                                (random.random() * width,
                                 random.random() * height, 5, 5))
        # обновление экрана
        special_color = (special_color + 1) % 256
        screen.fill((special_color, special_color, special_color), (*pos, 50, 50))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
