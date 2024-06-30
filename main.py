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

        elif ev.type == p.MOUSEMOTION:
            if g.actual_screen == 'welcome_screen':
                if g.play_button.rect.collidepoint(ev.pos):
                    g.play_button.image = g.play_button.image_mouse_on
                else:
                    g.play_button.image = g.play_button.image_idle
            elif g.actual_screen == 'loose_screen':
                if g.replay_button.rect.collidepoint(ev.pos):
                    g.replay_button.image = g.replay_button.image_mouse_on
                else:
                    g.replay_button.image = g.replay_button.image_idle

        elif ev.type == p.MOUSEBUTTONDOWN:
            if g.actual_screen == 'welcome_screen':
                if g.play_button.rect.collidepoint(ev.pos):
                    g.actual_screen = 'game'
            elif g.actual_screen == 'game':
                if g.game_state == 'player':
                    for light in g.lights:
                        if light.rect.collidepoint(ev.pos) and g.num_light_clicked < len(g.lights_demonstrated):
                            g.answer = g.verify(light.color)
                            light.turn_on()
            elif g.actual_screen == 'loose_screen':
                if g.replay_button.rect.collidepoint(ev.pos):
                    g.replay()
                    g.actual_screen = 'game'

    clock.tick(FPS)
