def update_planets(planets, speed=0.01, spawn_chance=0.001):
    for planet in planets:
        planet.theta += speed
        planet.try_spawn_civilization(spawn_chance)
