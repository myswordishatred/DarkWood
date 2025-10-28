import random
from planet_system import PlanetSystem

def generate_planets(count):
    planets = []
    for _ in range(count):
        theta = random.uniform(0, 2 * 3.14159265359)
        r = (random.uniform(0, 1)) ** 0.5
        planet = PlanetSystem(theta, r)
        # Можно задать случайное начальное состояние, если нужно
        planets.append(planet)
    return planets
