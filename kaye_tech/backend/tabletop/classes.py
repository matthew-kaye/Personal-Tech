from abc import ABC, abstractmethod
from .utilities import proficiency_bonus_by_level, chance_to_hit, chance_to_critical
from .constants import Styles
from .weapon import Weapons
import json
import math


class Wolf:
    bonus_to_hit: int
    average_damage_die: int = 5
    bite_damage: int
    attacks: int
    chance_to_hit: float
    chance_to_critical: float

    def __init__(self, ranger_level: int, enemy_armour: int, advantage: bool):
        self.bonus_to_hit = 4 + proficiency_bonus_by_level(ranger_level)
        self.bite_damage = 7 + proficiency_bonus_by_level(ranger_level)
        self.number_of_attacks = 2 if ranger_level >= 11 else 1
        self.chance_to_hit = chance_to_hit(self.bonus_to_hit, enemy_armour, advantage)
        self.chance_to_critical = chance_to_critical(0.05, advantage)

    def damage_output(self):
        base_damage = self.bite_damage * self.chance_to_hit
        critical_damage = self.average_damage_die * self.chance_to_critical
        return self.number_of_attacks * (base_damage + critical_damage)


class Class(ABC):
    name: str
    level: int
    fighting_style: str
    superiority_bonus: bool
    hunters_mark: bool
    colossus_slayer: bool
    advantage: bool
    war_magic: bool
    shadow_blade: bool
    subclass: str
    two_weapons: bool
    caster_multiclasses: int

    def __init__(self, data):
        abilities = json.loads(data["abilities"])
        bonuses = json.loads(data["bonuses"])
        self.name = data["characterClass"]
        self.level = int(data["characterLevel"])
        self.advantage = bonuses["advantage"]
        self.enemy_armour = int(data["averageAC"]) if data["averageAC"] else 0
        self.fighting_style = data["fightingStyle"]
        self.superiority_bonus = abilities["superiority"]
        self.hunters_mark = abilities["huntersMark"]
        self.colossus_slayer = abilities["colossusSlayer"]
        self.wolf_attack = abilities["wolfAttack"]
        self.war_magic = abilities["warMagic"]
        self.shadow_blade = abilities["shadowBlade"]
        self.subclass = data["subclass"]
        self.two_weapons = self.fighting_style == Styles.TWO_WEAPON
        self.caster_multiclasses = int(data["casterMulticlasses"])

    def average_dice_damage(self, weapon):
        if self.fighting_style == Styles.TWO_HANDED and (
            weapon.heavy or weapon.versatile
        ):
            weapon_damage = weapon.damage + 1 if weapon.versatile else weapon.damage
            if weapon == Weapons.GREATSWORD:
                return weapon_damage + 4 / 3
            dice_max = weapon_damage * 2 - 1
            reroll_chance = 2 / dice_max
            return round(
                reroll_chance * weapon_damage
                + (1 - reroll_chance) * (weapon_damage + 1),
                8,
            )
        return weapon.damage

    def style_damage(self, weapon):
        if self.fighting_style == Styles.DUELLING and not weapon.heavy:
            return 2
        return 0

    def style_bonus(self, weapon):
        return 2 if self.fighting_style == Styles.ARCHERY and weapon.ranged else 0

    def critical_chance(self):
        return 0.05

    @abstractmethod
    def number_of_attacks(self, level):
        pass

    @abstractmethod
    def caster_level(self):
        pass

    def damage_on_a_hit(self):
        return 0

    def damage_per_hit(self):
        return 0

    def other_damage(self):
        return 0


class Ranger(Class):
    def number_of_attacks(self, level):
        return 2 if level >= 5 and not self.wolf_attack else 1

    def damage_per_hit(self):
        return 3.5 if self.hunters_mark else 0

    def caster_level(self):
        return 0 if self.level == 1 else math.ceil(self.level / 2)


class Fighter(Class):
    def number_of_attacks(self, level):
        if self.war_magic:
            return 2
        if level == 20:
            return 4
        elif level >= 11:
            return 3
        elif level >= 5:
            return 2
        else:
            return 1

    def caster_level(self):
        return 0
