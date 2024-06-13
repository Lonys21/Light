import pygame
from game import Game

pygame.init()
p = pygame
pygame.display.set_caption("Light")
screen = pygame.display.set_mode((200, 200))
clock = pygame.time.Clock()
FPS = 60
g = Game(screen, FPS)

running = True
while running:

    g.update()
    p.display.flip()

    for ev in p.event.get():
        if ev.type == p.QUIT:
            running = False
            p.quit()

        elif ev.type == p.MOUSEBUTTONDOWN:
            if g.game_state == 'player':
                for light in g.lights:
                    if light.rect.collidepoint(ev.pos):
                        g.answer = g.verify(light.color)
                        light.turn_on()
    clock.tick(FPS)
