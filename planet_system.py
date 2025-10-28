import math
import random

class PlanetSystem:
    def __init__(self, theta, r):
        self.theta = theta
        self.r = r
        self.colonized = False
        self.tech_level = 0
        self.color = 'yellow'
        self.detection_radius = 0  # начальный радиус обнаружения

    def get_position(self):
        x = 300 + 250 * self.r * math.cos(self.theta)
        y = 250 + 150 * self.r * math.sin(self.theta)
        return x, y

    def try_spawn_civilization(self, chance=0.001):
        if not self.colonized and random.random() < chance:
            self.colonized = True
            self.color = self.random_color()
            self.detection_radius = 1  # стартовый радиус при рождении цивилизации

    def random_color(self):
        r = lambda: random.randint(0, 255)
        return f'#{r():02x}{r():02x}{r():02x}'

    def update_detection_radius(self):
        # скорость увеличения радиуса пропорциональна уровню технологии
        growth_speed = 0.1 * (self.tech_level + 1)  # например, базовая 0.1, умноженная на tech_level+1
        if self.colonized:
            self.detection_radius += growth_speed
