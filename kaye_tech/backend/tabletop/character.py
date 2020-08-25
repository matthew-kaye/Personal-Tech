from dataclasses import dataclass
from .weapon import Weapon, Blacksmith
import math
import json


@dataclass
class Class:
    name: str
    fighting_style: str

    def __init__(self, name, fighting_style):
        self.name = name
        self.fighting_style = fighting_style

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other


@dataclass
class Character:
    weapon: Weapon
    battle_class: Class
    attack_stat: int
    advantage: bool
    level: int
    proficiency_bonus: int

    def __init__(self, data):
        blacksmith = Blacksmith()
        self.weapon = blacksmith.draw_weapon(data["weapon"])
        self.level = int(data["characterLevel"])
        self.advantage = json.loads(data["bonuses"])["advantage"]
        self.attack_stat = int(data["attackStat"])
        self.battle_class = Class(data["characterClass"], data["fightingStyle"])
        self.proficiency_bonus = self.proficiency_bonus_by_level(self.level)

    def number_of_attacks(self):
        if self.weapon.loading:
            return 1
        if self.battle_class == "Fighter":
            return self.fighter_attacks_by_level(self.level)
        elif self.battle_class == "Ranger":
            return self.ranger_attacks_by_level(self.level)

    def bonus_to_hit(self):
        base_bonus = self.attack_stat + self.proficiency_bonus
        style_bonus = (
            2
            if self.battle_class.fighting_style == "Archery" and self.weapon.ranged
            else 0
        )
        return base_bonus + style_bonus

    def proficiency_bonus_by_level(self, level):
        return math.ceil(level / 4) + 1

    def fighter_attacks_by_level(self, level):
        if level == 20:
            return 4
        elif level >= 11:
            return 3
        elif level >= 5:
            return 2
        else:
            return 1

    def ranger_attacks_by_level(self, level):
        return 2 if level >= 5 else 1
