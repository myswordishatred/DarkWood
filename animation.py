import math
import random

def distance(planet1, planet2):
    x1, y1 = planet1.get_position()
    x2, y2 = planet2.get_position()
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def update_planets(planets, canvas, log_func, speed=0.01, spawn_chance=0.001):
    for planet in planets:
        pre_colonized = planet.colonized
        planet.theta += speed
        planet.try_spawn_civilization(spawn_chance)
        if not pre_colonized and planet.colonized:
            log_func(f"Цивилизация создана на планете {planet.name}")
        planet.update_detection_radius()
        planet.update_tech_from_friends(log_func)

    for planet in planets:
        if not planet.colonized:
            continue
        for other in planets:
            if other is planet or not other.colonized:
                continue
            dist = distance(planet, other)
            if dist <= planet.detection_radius:
                if other not in planet.connections:
                    if planet.hostility:
                        targets = other.connections.union({other})
                        for target in targets:
                            if not target.colonized:
                                continue
                            level_diff = planet.tech_level - target.tech_level
                            kill_prob = max(0.0, min(1.0, 0.5 + 0.1 * level_diff))
                            if random.random() < kill_prob:
                                target.weaken()
                                planet.record_destruction(target)
                                log_func(f"{planet.name} атаковала {target.name}")
                                if not target.colonized:
                                    log_func(f"{target.name} уничтожена!")
                                planet_fire(canvas, planet, target)
                    else:
                        planet.add_friend(other)
                        log_func(f"{planet.name} подружилась с {other.name}")

def planet_fire(canvas, attacker, target):
    x1, y1 = attacker.get_position()
    x2, y2 = target.get_position()
    line_id = canvas.create_line(x1, y1, x2, y2, fill='red', width=2)
    def remove_line():
        canvas.delete(line_id)
    canvas.after(300, remove_line)
