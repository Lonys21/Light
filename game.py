import random
import pygame

p = pygame

class Game:
    def __init__(self, screen, FPS):
        # screen
        # self.INFOS_SIZE = 100
        self.screen = screen
        self.FPS = FPS
        self.background_color_demonstration = (5, 5, 5)
        self.background_color_player = "Black"
        self.background_color = self.background_color_demonstration

        # menu
        self.actual_screen = "welcome_screen"
        self.welcome_screen = p.image.load("assets/Welcome_screen.png")

        # buttons
        self.BUTTON_WIDTH = 100
        self.BUTTON_HEIGHT = 60
        self.play_button = Button("Play", self.screen.get_width()/2 - self.BUTTON_WIDTH/2, self.screen.get_height()*13/20 , self)
        self.replay_button = Button("Replay", self.screen.get_width()/2 - self.BUTTON_WIDTH/2, self.screen.get_height()/2 - self.BUTTON_HEIGHT/2, self)


        # game_state
        self.game_state = "demonstrate_off"  # demonstrate_off/ demonstrate_on / player
        self.TIMER_BETWEEN_STATES = self.FPS*0.5
        self.timer_states = self.TIMER_BETWEEN_STATES

        # light
        self.LIGHT_SIZE = 100
        self.LIGHT_TIME_ON = 0.8
        self.TIMER_SAME_COLOR = 0.2*self.FPS
        self.timer_same_color = self.TIMER_SAME_COLOR
        self.lights = []
        self.colors = (("Blue", 0, 0),
                       ("Red", self.screen.get_width() - self.LIGHT_SIZE, 0),
                       ('Yellow', 0, self.screen.get_height() - self.LIGHT_SIZE),
                       ("Green", self.screen.get_width() - self.LIGHT_SIZE, self.screen.get_height() - self.LIGHT_SIZE))
        for color in self.colors:
            self.lights.append(Light(self, color[0], color[1], color[2]))
        self.lights_demonstrated = []
        self.light_on = False
        self.num_light_clicked = 0
        self.answer = True

        # round
        self.round = 1
        self.font_round = p.font.SysFont("Arial", 30)
        self.font_color = "white"
        self.font_score = p.font.SysFont("Arial", 18)




    def replay(self):
        # game_state
        self.game_state = 'demonstrate_off'
        # color
        self.lights_demonstrated = []
        self.light_on = False
        self.num_light_clicked = 0
        self.answer = True

        # round
        self.round = 1

    def update(self):
        a = 0
        self.screen.fill(self.background_color)
        if self.actual_screen == 'welcome_screen':
            self.screen.blit(self.welcome_screen, (0, 0))
            self.screen.blit(self.play_button.image, (self.play_button.rect.x, self.play_button.rect.y))
        elif self.actual_screen == 'game':
            if not self.game_state == 'display_round':
                for light in self.lights:
                    if light.update():
                        a = 1
                    self.screen.blit(light.image, (light.rect.x, light.rect.y))
                text = str(self.round)
                self.screen.blit(self.font_round.render(text, True, self.font_color),  # display the round
                                 (self.screen.get_width() / 2 - self.font_round.size(text)[0] / 2,
                                  self.screen.get_height() / 2 - self.font_round.size(text)[1] / 2))  # Center the text
            if a == 0:
                self.light_on = False
            else:
                self.light_on = True
            if self.game_state == 'demonstrate_off':
                if self.timer_between_states():
                    self.add_light()
            elif self.game_state == 'demonstrate_on':
                self.demonstrate()
            elif self.game_state == 'player':
                if not self.answer and self.num_light_clicked != 0:
                    self.actual_screen = 'loose_screen'
                elif self.num_light_clicked == len(self.lights_demonstrated) and not self.light_on:
                    if self.timer_between_states():
                        self.round += 1
                        self.game_state = 'demonstrate_off'
        elif self.actual_screen == 'loose_screen':
            text = "You passed " + str(self.round) + " rounds"
            self.screen.blit(self.font_score.render(text, True, self.font_color),  # display the text
                             (self.screen.get_width() / 2 - self.font_score.size(text)[0] / 2, # Center the text horizontally
                              self.screen.get_height()* 1/4 - self.font_score.size(text)[1] / 2))
            self.screen.blit(self.replay_button.image, (self.replay_button.rect.x, self.replay_button.rect.y)) # displat the replay button




    def add_light(self):
        self.background_color = self.background_color_demonstration # change the background color --> turn to the demonstration, don't click
        self.num_light_clicked = 0
        color = random.choice(self.colors)
        color_dictionnary = {"color": color[0], "Done": False}
        self.lights_demonstrated.append(color_dictionnary)
        for light in self.lights_demonstrated:
            light["Done"] = False
        for light in self.lights:
            light.activated = False
        self.game_state = 'demonstrate_on'
        # dictionnary ({"color":red, "Done":True/False}, )
    def demonstrate(self):
        previous_color = None
        for color in self.lights_demonstrated:
            if not color["Done"]:
                for light in self.lights:
                    if light.color == color["color"]:
                        if light.on_timer <= 0:  # light is off
                            if not light.activated: # off and not activated
                                if previous_color == color['color']:
                                    if self.timer_same_color == 0:
                                        light.turn_on()
                                        self.timer_same_color = self.TIMER_SAME_COLOR
                                    else:
                                        self.timer_same_color -= 1
                                else:
                                    light.turn_on()
                                return
                            elif light.activated: # off and been activated
                                color["Done"] = True
                                light.activated = False
                                return
                        else:  # light is on
                            return
            previous_color = color['color']
        if self.timer_between_states():
            self.background_color = self.background_color_player # change the color of the background --> turn of the player
            self.game_state = 'player'

    def verify(self, color):
        self.num_light_clicked += 1
        if color == self.lights_demonstrated[self.num_light_clicked-1]["color"]:
            return True
        else:
            return False

    def timer_between_states(self):
        if self.timer_states == 0:
            self.timer_states = self.TIMER_BETWEEN_STATES
            return True
        elif self.timer_states > 0:
            self.timer_states -= 1
            return False




class Light(p.sprite.Sprite):

    def __init__(self, game, color, x, y):
        super().__init__()
        self.g = game
        self.image_off = p.image.load("assets/" + color + "_off.png")
        self.image_on = p.image.load("assets/" + color + "_on.png")
        self.image = self.image_off
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.on_timer = 0
        self.activated = False

    def update(self):
        if self.on_timer <= 0:
            self.image = self.image_off
            return False
        else:
            self.on_timer -= 1
            return True
    def turn_on(self):
        self.activated = True
        self.image = self.image_on
        self.on_timer = self.g.FPS*self.g.LIGHT_TIME_ON


class Button(pygame.sprite.Sprite):
    def __init__(self, file, x, y, game):
        super().__init__()
        self.image_idle = p.transform.scale(pygame.image.load("assets/" + file + "_button_idle.png"), (game.BUTTON_WIDTH, game.BUTTON_HEIGHT))
        self.image_mouse_on = p.transform.scale(pygame.image.load("assets/" + file + "_button_mouse_on.png"), (game.BUTTON_WIDTH, game.BUTTON_HEIGHT))
        self.image = self.image_idle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
