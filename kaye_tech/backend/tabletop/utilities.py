import math


def proficiency_bonus_by_level(level: int):
    return math.ceil(level / 4) + 1


def chance_to_hit(
    bonus_to_hit: int,
    armour_class: int,
    advantage: bool = False,
    disadvantage: bool = False,
):
    chance_to_hit = max(1 - (armour_class - 1 - bonus_to_hit) / 20, 0.05)
    chance_to_hit = min(chance_to_hit, 0.95)
    return probability(chance_to_hit, advantage, disadvantage)


def chance_to_critical(
    chance: float, advantage: bool = False, disadvantage: bool = False
):
    return probability(chance, advantage, disadvantage)


def probability(chance: float, advantage: bool, disadvantage: bool):
    if advantage and not disadvantage:
        return round(1 - (1 - chance) ** 2, 8)
    elif disadvantage and not advantage:
        return round(chance ** 2, 8)
    return chance


def chance_of_an_instance(chance: float, attacks: int):
    return round(1 - (1 - chance) ** attacks, 8)
