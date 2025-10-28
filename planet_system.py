import math
import random

def distance(planet1, planet2):
    x1, y1 = planet1.get_position()
    x2, y2 = planet2.get_position()
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

class PlanetSystem:
    _id_counter = 1

    def __init__(self, theta, r, aggression_chance=0.5):
        self.id = PlanetSystem._id_counter
        PlanetSystem._id_counter += 1
        self.name = f"Планета #{self.id}"
        self.theta = theta
        self.r = r
        self.colonized = False
        self.tech_level = 0
        self.color = '#ffff00'
        self.detection_radius = 0
        self.hostility = random.random() < aggression_chance  # bool
        self.connections = set()
        self.destroyed_planets = set()

    def get_position(self):
        x = 500 + 400 * self.r * math.cos(self.theta)
        y = 300 + 200 * self.r * math.sin(self.theta)
        return x, y

    def try_spawn_civilization(self, chance=0.001):
        if not self.colonized and random.random() < chance:
            self.colonized = True
            self.color = self.random_color()
            self.detection_radius = 1

    def random_color(self):
        r = lambda: random.randint(0, 255)
        return f'#{r():02x}{r():02x}{r():02x}'

    def update_detection_radius(self):
        max_fast_growth_level = 10
        if self.colonized:
            if self.tech_level < max_fast_growth_level:
                # Быстрый рост
                growth_speed = 0.1
            else:
                # Очень медленный рост
                growth_speed = 0.005
                # Или даже реже, добавьте условие
                if random.random() < 0.01:  # 1% шанс на скачок
                    growth_speed += 0.05
            self.detection_radius += growth_speed

    def weaken(self, amount=1):
        self.tech_level = max(0, self.tech_level - amount)
        if self.tech_level == 0:
            self.colonized = False
            self.color = '#ffff00'
            self.detection_radius = 0
            self.connections.clear()

    def add_friend(self, other_planet):
        # возможно данный метод надо дополнить проверкой расстояния
        dist = distance(self, other_planet)  # функция расстояния между планетами
        if dist <= self.detection_radius and dist <= other_planet.detection_radius:
            self.connections.add(other_planet)
            other_planet.connections.add(self)

    def update_tech_from_friends(self, log_func=None):
        max_fast_growth_level = 10
        if not self.colonized:
            return
        base_growth = 0.01
        max_tech = max((friend.tech_level for friend in self.connections), default=self.tech_level)
        growth = base_growth
        if max_tech > self.tech_level:
            growth += 0.1
        old_level = self.tech_level

        if self.tech_level < max_fast_growth_level:
            # Быстрый равномерный рост
            self.tech_level += growth
        else:
            # Медленный рост с редкими скачками
            self.tech_level += growth * 0.1
            if random.random() < 0.05:  # 5% шанс скачка
                self.tech_level += growth

        if log_func and self.tech_level - old_level >= 0.05:
            log_func(f"{self.name} увеличила уровень технологий с {old_level:.2f} до {self.tech_level:.2f}")

        # Цвета для отображения уровня технологий можно улучшить здесь
        level_ratio = min(1.0, self.tech_level / (max_tech + 1))
        red_val = int(255 * (1 - level_ratio))
        green_val = int(255 * level_ratio)
        blue_val = int(255 * (0.5 * (1 - level_ratio)))
        self.color = f'#{red_val:02x}{green_val:02x}{blue_val:02x}'

    def record_destruction(self, planet):
        self.destroyed_planets.add(planet.name)
