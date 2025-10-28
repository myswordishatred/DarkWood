import random
import math

def generate_planets(count):
    planets = []
    for _ in range(count):
        theta = random.uniform(0, 2 * math.pi)
        r = math.sqrt(random.uniform(0, 1))
        planets.append([theta, r])
    return planets
