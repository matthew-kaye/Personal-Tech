from dataclasses import dataclass
from .weapon import Weapon, Weapons, Blacksmith
from .fighting_styles import Styles
from .classes import Classes, Class, Ranger, Fighter
from abc import ABC, abstractmethod
import math
import json

SMITH = Blacksmith()


class Subclasses:
    BATTLE_MASTER = "Battle Master"
    BEAST_MASTER = "Beast Master"
    CHAMPION = "Champion"
    ELDRITCH_KNIGHT = "Eldritch Knight"
    HUNTER = "Hunter"


@dataclass
class Character:
    weapon: Weapon
    battle_class: Class
    subclass: str
    attack_stat: int
    advantage: bool
    level: int
    proficiency_bonus: int
    enemy_armour_class: int
    dual_wielder: bool
    sharpshooter: bool
    great_weapon_master: bool
    magic_weapon: bool

    def __init__(self, data):
        bonuses = json.loads(data["bonuses"])
        abilities = json.loads(data["abilities"])
        self.enemy_armour_class = int(
            data["averageAC"]) if data["averageAC"] else 0
        self.weapon = SMITH.draw_weapon(data["weapon"])
        self.level = int(data["characterLevel"])
        self.advantage = bonuses["advantage"]
        self.magic_weapon = bonuses["magicWeapon"]
        self.dual_wielder = abilities["dualWielder"]
        self.sharpshooter = abilities["sharpshooter"]
        self.great_weapon_master = abilities["greatWeaponMaster"]
        self.attack_stat = int(data["attackStat"])
        self.battle_class = (
            Fighter(data) if data["characterClass"] == Classes.FIGHTER else Ranger(
                data)
        )
        self.subclass = data["subclass"]
        self.proficiency_bonus = self.proficiency_bonus_by_level(self.level)

    def damage_output(self):
        attacks = self.number_of_attacks()
        chance_to_hit = self.chance_to_hit_by_ac(self.enemy_armour_class)
        crit_chance = self.chance_to_crit()
        attack_damage = self.attack_damage() * chance_to_hit
        crit_damage = self.average_dice_damage() * crit_chance
        bonus_damage = self.bonus_attack_damage() + self.ability_damage()
        return (attack_damage + crit_damage) * attacks + bonus_damage

    def number_of_attacks(self):
        if self.weapon.loading:
            return 1
        else:
            return self.battle_class.number_of_attacks(self.level)

    def attack_damage(self):
        base_damage = self.average_dice_damage() + self.attack_stat + self.magic_bonus()
        if (
            self.battle_class.fighting_style == Styles.DUELLING
            and not self.weapon.heavy
        ):
            return base_damage + 2
        elif self.attempting_bigger_hit():
            return base_damage + 10
        else:
            return base_damage

    def average_dice_damage(self):
        if self.battle_class.fighting_style == Styles.TWO_HANDED and (
            self.weapon.heavy or self.weapon.versatile
        ):
            return self.great_weapon_damage(self.weapon)
        else:
            return self.weapon.damage

    def bonus_attack_damage(self):
        if self.battle_class.fighting_style == Styles.TWO_WEAPON:
            return self.second_weapon_damage()
        else:
            return 0

    def second_weapon_damage(self):
        chance_to_hit = self.chance_to_hit_by_ac(self.enemy_armour_class)
        if self.weapon.light or (self.dual_wielder and not self.weapon.heavy):
            return (
                self.weapon.damage + self.attack_stat + self.magic_bonus()
            ) * chance_to_hit + self.weapon.damage * self.chance_to_crit()
        else:
            return 0

    def ability_damage(self):
        damage = self.battle_class.superiority_die_damage(self.level)
        return damage*(self.chance_of_a_hit() + self.chance_of_a_crit())

    def chance_to_hit_by_ac(self, armour_class):
        bonus_to_hit = self.bonus_to_hit()
        chance_to_hit = max(1 - (armour_class - 1 - bonus_to_hit) / 20, 0.05)
        chance_to_hit = min(chance_to_hit, 0.95)
        return 1 - (1 - chance_to_hit) ** 2 if self.advantage else chance_to_hit

    def chance_of_a_hit(self):
        chance_to_hit = self.chance_to_hit_by_ac(self.enemy_armour_class)
        return 1 - (1 - chance_to_hit)**self.battle_class.number_of_attacks(self.level)

    def chance_to_crit(self):
        if self.subclass == Subclasses.CHAMPION and self.level >= 3:
            crit_chance = 0.15 if self.level >= 15 else 0.1
        else:
            crit_chance = 0.05
        return round(1 - (1 - crit_chance) ** 2 if self.advantage else crit_chance, 8)

    def chance_of_a_crit(self):
        return 1 - (1-self.chance_to_crit())**self.battle_class.number_of_attacks(self.level)

    def bonus_to_hit(self):
        base_bonus = self.attack_stat + self.proficiency_bonus + self.magic_bonus()
        style_bonus = (
            2
            if self.battle_class.fighting_style == Styles.ARCHERY and self.weapon.ranged
            else 0
        )
        ability_modifier = -5 if self.attempting_bigger_hit() else 0
        return base_bonus + style_bonus + ability_modifier

    def attempting_bigger_hit(self):
        sharpshooting = self.sharpshooter and self.weapon.ranged
        heavy_swing = self.great_weapon_master and (
            self.weapon.heavy or self.weapon.versatile
        )
        return sharpshooting or heavy_swing

    def great_weapon_damage(self, weapon):
        weapon_damage = weapon.damage + 1 if weapon.versatile else weapon.damage
        if weapon == Weapons.GREATSWORD:
            return weapon_damage + 4 / 3
        dice_max = weapon_damage * 2 - 1
        reroll_chance = 2 / dice_max
        return reroll_chance * weapon_damage + (1 - reroll_chance) * (weapon_damage + 1)

    def magic_bonus(self):
        return 1 if self.magic_weapon else 0

    def proficiency_bonus_by_level(self, level):
        return math.ceil(level / 4) + 1
