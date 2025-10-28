import math
import random

def distance(planet1, planet2):
    x1, y1 = planet1.get_position()
    x2, y2 = planet2.get_position()
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


import random


def apply_random_event(planets, log_func):
    event_chance = 0.005  # 0.5% шанс на событие за итерацию
    if random.random() > event_chance:
        return

    events = [solar_flare, volcanic_activity, meteor_shower, energy_storm,
              new_material_discovery, interstellar_communications, defensive_technology,
              cultural_exchange, internal_conflict, alliance_formation, resource_boom, economic_crisis]

    event = random.choice(events)
    event(planets, log_func)


def solar_flare(planets, log_func):
    victim = random.choice(planets)
    if victim.colonized:
        victim.tech_level = max(0, victim.tech_level - 2)
        victim.color = '#ff0000'
        log_func(f"Солнечная вспышка замедлила развитие {victim.name}")


def volcanic_activity(planets, log_func):
    victim = random.choice(planets)
    if victim.colonized:
        victim.hostility = min(1, victim.hostility + 0.7)
        log_func(f"Вулканическая активность повысила враждебность {victim.name}")


def meteor_shower(planets, log_func):
    victim = random.choice(planets)
    if victim.colonized:
        victim.colonized = False
        victim.tech_level = 0
        victim.color = '#ffff00'
        log_func(f"Метеоритный дождь уничтожил цивилизацию на {victim.name}")


def energy_storm(planets, log_func):
    for p in planets:
        if p.colonized:
            p.detection_radius = max(0, p.detection_radius - 5)
    log_func("Галактическая буря снизила радиусы обнаружения всех цивилизаций")


def new_material_discovery(planets, log_func):
    lucky = random.choice(planets)
    if lucky.colonized:
        lucky.tech_level += 5
        log_func(f"{lucky.name} совершила научный прорыв!")


def interstellar_communications(planets, log_func):
    candidates = [p for p in planets if p.colonized]
    if len(candidates) < 2:
        return
    lucky = random.choice(candidates)
    others = [p for p in candidates if p != lucky and p not in lucky.connections]
    if len(others) < 1:
        return
    new_friends = random.sample(others, min(3, len(others)))
    for friend in new_friends:
        lucky.add_friend(friend)
    log_func(f"{lucky.name} установила межзвёздные коммуникации с {len(new_friends)} цивилизациями")


def defensive_technology(planets, log_func):
    defender = random.choice(planets)
    if defender.colonized:
        defender.hostility = max(0, defender.hostility - 0.5)
        log_func(f"{defender.name} разработала оборонительные технологии")


def cultural_exchange(planets, log_func):
    colonized_planets = [p for p in planets if p.colonized]
    if len(colonized_planets) < 2:
        return  # недостаточно планет для события
    pair = random.sample(colonized_planets, 2)
    for p in pair:
        p.hostility = max(0, p.hostility - 0.3)
    log_func(f"Культурный обмен между {pair[0].name} и {pair[1].name} снизил враждебность")



def internal_conflict(planets, log_func):
    troubled = random.choice(planets)
    if troubled.colonized:
        troubled.tech_level = max(0, troubled.tech_level - 3)
        troubled.hostility = min(1, troubled.hostility + 0.6)
        log_func(f"Внутренний конфликт ослабил {troubled.name}")


def alliance_formation(planets, log_func):
    colonized = [p for p in planets if p.colonized]
    if len(colonized) < 3:
        return
    group = random.sample(colonized, 3)
    for p in group:
        for other in group:
            if other != p:
                p.add_friend(other)
    names = ", ".join(p.name for p in group)
    log_func(f"Формируется альянс между: {names}")


def resource_boom(planets, log_func):
    lucky = random.choice(planets)
    if lucky.colonized:
        lucky.tech_level += 3
        lucky.detection_radius += 5
        log_func(f"{lucky.name} переживает ресурсный бум")


def economic_crisis(planets, log_func):
    unlucky = random.choice(planets)
    if unlucky.colonized:
        unlucky.tech_level = max(0, unlucky.tech_level - 4)
        unlucky.hostility = min(1, unlucky.hostility + 0.4)
        log_func(f"Экономический кризис затронул {unlucky.name}")


def update_planets(planets, canvas, log_func, speed=0.01, spawn_chance=0.001):
    apply_random_event(planets, log_func)
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
