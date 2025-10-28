import math
import random

class PlanetSystem:
    def __init__(self, theta, r):
        self.theta = theta
        self.r = r
        self.colonized = False
        self.tech_level = 0
        self.color = 'yellow'  # цвет по умолчанию

    def get_position(self):
        x = 300 + 250 * self.r * math.cos(self.theta)
        y = 250 + 150 * self.r * math.sin(self.theta)
        return x, y

    def try_spawn_civilization(self, chance=0.001):
        if not self.colonized and random.random() < chance:
            self.colonized = True
            self.color = self.random_color()

    def random_color(self):
        # Возвращает случайный цвет, например, в HEX формате
        r = lambda: random.randint(0,255)
        return f'#{r():02x}{r():02x}{r():02x}'
