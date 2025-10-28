import random
from planet_system import PlanetSystem
import math

def draw_planets(canvas, planets, show_radii=False):
    canvas.delete('all')
    drawn_sets = set()
    for planet in planets:
        friends_group = frozenset(planet.connections.union({planet}))
        if friends_group not in drawn_sets:
            drawn_sets.add(friends_group)
            color = average_color(friends_group)
            friend_list = list(friends_group)
            for i in range(len(friend_list)):
                for j in range(i + 1, len(friend_list)):
                    x1, y1 = friend_list[i].get_position()
                    x2, y2 = friend_list[j].get_position()
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
    for planet in planets:
        x, y = planet.get_position()
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=planet.color)
        if show_radii and planet.colonized:
            r = planet.detection_radius
            canvas.create_oval(x - r, y - r, x + r, y + r, outline='white')


def generate_planets(count, aggression_chance=0.5):
    planets = []
    for _ in range(count):
        theta = random.uniform(0, 2 * math.pi)
        r = (random.uniform(0, 1)) ** 0.5
        planet = PlanetSystem(theta, r, aggression_chance)
        planets.append(planet)
    return planets
