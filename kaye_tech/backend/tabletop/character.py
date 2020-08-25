from dataclasses import dataclass
from .weapon import Weapon, Weapons, Blacksmith
from .fighting_styles import Styles
import math
import json


class Subclasses:
    BATTLE_MASTER = "Battle Master"
    BEAST_MASTER = "Beast Master"
    CHAMPION = "Champion"
    ELDRITCH_KNIGHT = "Eldritch Knight"
    HUNTER = "Hunter"


class Classes:
    RANGER = "Ranger"
    FIGHTER = "Fighter"


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
    subclass: str
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
        self.subclass = data["subclass"]
        self.proficiency_bonus = self.proficiency_bonus_by_level(self.level)

    def number_of_attacks(self):
        if self.weapon.loading:
            return 1
        if self.battle_class == Classes.FIGHTER:
            return self.fighter_attacks_by_level(self.level)
        elif self.battle_class == Classes.RANGER:
            return self.ranger_attacks_by_level(self.level)

    def chance_to_hit_by_ac(self, armour_class):
        bonus_to_hit = self.bonus_to_hit()
        chance_to_hit = max(1 - (armour_class - 1 - bonus_to_hit) / 20, 0.05)
        chance_to_hit = min(chance_to_hit, 0.95)
        return 1 - (1 - chance_to_hit) ** 2 if self.advantage else chance_to_hit

    def chance_to_crit(self):
        if self.subclass == Subclasses.CHAMPION and self.level >= 3:
            crit_chance = 0.15 if self.level >= 15 else 0.1
        else:
            crit_chance = 0.05
        return round(1 - (1 - crit_chance) ** 2 if self.advantage else crit_chance, 8)

    def bonus_to_hit(self):
        base_bonus = self.attack_stat + self.proficiency_bonus
        style_bonus = (
            2
            if self.battle_class.fighting_style == Styles.ARCHERY and self.weapon.ranged
            else 0
        )
        return base_bonus + style_bonus

    def average_dice_damage(self):
        if self.battle_class.fighting_style == Styles.TWO_HANDED and (
            self.weapon.heavy or self.weapon.versatile
        ):
            return self.great_weapon_damage(self.weapon)
        else:
            return self.weapon.damage

    def great_weapon_damage(self, weapon):
        weapon_damage = weapon.damage + 1 if weapon.versatile else weapon.damage
        if weapon == Weapons.GREATSWORD:
            return weapon_damage + 4 / 3
        dice_max = weapon_damage * 2 - 1
        reroll_chance = 2 / dice_max
        return reroll_chance * weapon_damage + (1 - reroll_chance) * (weapon_damage + 1)

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
