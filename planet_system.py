import math
import random

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
        self.color = 'yellow'
        self.detection_radius = 0
        self.hostility = random.random() < aggression_chance  # bool
        self.connections = set()
        self.destroyed_planets = set()

    def get_position(self):
        x = 300 + 250 * self.r * math.cos(self.theta)
        y = 250 + 150 * self.r * math.sin(self.theta)
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
        growth_speed = 0.1 * (self.tech_level + 1)
        if self.colonized:
            self.detection_radius += growth_speed

    def weaken(self, amount=1):
        self.tech_level = max(0, self.tech_level - amount)
        if self.tech_level == 0:
            self.colonized = False
            self.color = 'yellow'
            self.detection_radius = 0
            self.connections.clear()

    def add_friend(self, other):
        all_friends = self.connections.union(other.connections, {self, other})
        for friend in all_friends:
            friend.connections = all_friends

    def update_tech_from_friends(self, log_func=None):
        if not self.colonized:
            return
        base_growth = 0.01
        max_tech = max((friend.tech_level for friend in self.connections), default=self.tech_level)
        growth = base_growth
        if max_tech > self.tech_level:
            growth += 0.1
        old_level = self.tech_level
        self.tech_level += growth
        if log_func and self.tech_level - old_level >= 0.05:
            log_func(f"{self.name} увеличила уровень технологий с {old_level:.2f} до {self.tech_level:.2f}")
        green_val = min(255, int(255 * min(1.0, self.tech_level / (max_tech + 1))))
        self.color = f'#00{green_val:02x}00'

    def record_destruction(self, planet):
        self.destroyed_planets.add(planet.name)
