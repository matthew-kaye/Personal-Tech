import math


def proficiency_bonus_by_level(level: int):
    return math.ceil(level / 4) + 1


def chance_to_hit(bonus_to_hit: int, armour_class: int, advantage: bool):
    chance_to_hit = max(1 - (armour_class - 1 - bonus_to_hit) / 20, 0.05)
    chance_to_hit = min(chance_to_hit, 0.95)
    return round(chance_if_advantage(chance_to_hit, advantage), 8)


def chance_if_advantage(chance: float, advantage: bool):
    return round(1 - (1 - chance) ** 2 if advantage else chance, 8)


def chance_of_an_instance(chance: float, attacks: int):
    return round(1 - (1 - chance) ** attacks, 8)
