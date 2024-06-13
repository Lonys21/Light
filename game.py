import random
import pygame

p = pygame

class Game:
    def __init__(self, screen, FPS):
        # screen
        self.screen = screen
        self.FPS = FPS
        self.background_color = "black"
        self.actual_screen = "game"


        # game_state
        self.game_state = "demonstrate_off"  # demonstrate/ player
        self.round = 1
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


    def update(self):
        a = 0
        self.screen.fill(self.background_color)
        for light in self.lights:
            if light.update():
                a = 1
            self.screen.blit(light.image, (light.rect.x, light.rect.y))
        if a == 0:
            self.light_on = False
        else:
            self.light_on = True
        if self.game_state == 'demonstrate_off':
            self.add_light()
        elif self.game_state == 'demonstrate_on':
            self.demonstrate()
        elif self.game_state == 'player':
            if not self.answer and self.num_light_clicked != 0:
                print("loose")
            elif self.num_light_clicked == len(self.lights_demonstrated) and not self.light_on:
                if self.timer_between_states():
                    self.game_state = 'demonstrate_off'




    def add_light(self):
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
