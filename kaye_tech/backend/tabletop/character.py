from dataclasses import dataclass
from .weapon import Weapon, Weapons, Blacksmith
from .fighting_styles import Styles
from .classes import Classes, Subclasses, Class, Ranger, Fighter
from .utilities import proficiency_bonus_by_level, chance_to_hit, chance_of_an_instance, chance_if_advantage
from abc import ABC, abstractmethod
import json

SMITH = Blacksmith()


@dataclass
class Character:
    weapon: Weapon
    bonus_weapon: Weapon
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
        feats = json.loads(data["feats"])
        self.level = int(data["characterLevel"])
        self.proficiency_bonus = proficiency_bonus_by_level(self.level)
        self.enemy_armour_class = int(
            data["averageAC"]) if data["averageAC"] else 0
        self.battle_class = (
            Fighter(data) if data["characterClass"] == Classes.FIGHTER else Ranger(
                data)
        )
        self.weapon = self.pick_weapon(data["weapon"])
        self.advantage = bonuses["advantage"]
        self.magic_weapon = bonuses["magicWeapon"]
        self.dual_wielder = feats["dualWielder"]
        self.sharpshooter = feats["sharpshooter"]
        self.great_weapon_master = feats["greatWeaponMaster"]
        self.great_weapon_master_swing = feats["greatWeaponMasterSwing"]
        self.crossbow_expert = feats["crossbowExpert"]
        self.attack_stat = int(data["attackStat"])
        self.bonus_weapon = self.pick_bonus_weapon()

    def damage_output(self):
        bonus_damage = self.bonus_attack_damage() + self.ability_damage()
        print(bonus_damage)
        print(self.average_attack_damage())
        return self.average_attack_damage() * self.number_of_attacks() + bonus_damage

    def number_of_attacks(self):
        if self.weapon.loading and not self.crossbow_expert:
            return 1
        return self.battle_class.number_of_attacks(self.level)

    def average_attack_damage(self):
        attack_damage = self.attack_damage() * self.chance_to_hit()
        crit_damage = self.average_dice_damage() * self.chance_to_crit()
        return attack_damage + crit_damage

    def attack_damage(self):
        base_damage = self.average_dice_damage() + self.attack_stat + self.magic_bonus()
        if (
            self.battle_class.fighting_style == Styles.DUELLING
            and not self.weapon.heavy
        ):
            return base_damage + 2
        elif self.attempting_bigger_hit():
            return base_damage + 10
        return base_damage

    def average_dice_damage(self):
        if self.battle_class.fighting_style == Styles.TWO_HANDED and (
            self.weapon.heavy or self.weapon.versatile
        ):
            return self.great_weapon_damage(self.weapon)
        return self.weapon.damage

    def bonus_attack_damage(self):
        if self.battle_class.fighting_style == Styles.TWO_WEAPON:
            return self.second_weapon_damage()
        elif self.great_weapon_master:
            return self.average_attack_damage() * self.chance_to_crit()
        return 0

    def second_weapon_damage(self):
        if self.bonus_weapon.light or (self.dual_wielder and not self.bonus_weapon.heavy):
            return (
                self.bonus_weapon.damage + self.attack_stat + self.magic_bonus()
            ) * self.chance_to_hit() + self.bonus_weapon.damage * self.chance_to_crit()
        return 0

    def ability_damage(self):
        damage_on_hit = self.battle_class.damage_on_a_hit(
        ) * (self.chance_of_a_hit() + self.chance_of_a_crit())
        per_hit_chance = self.chance_to_hit()+self.chance_to_crit()
        damage_per_hit = self.battle_class.damage_per_hit(
        ) * self.number_of_attacks() * (per_hit_chance)
        extra_damage = self.battle_class.other_damage(
        ) + (self.battle_class.booming_blade_damage() * per_hit_chance if self.battle_class.war_magic else 0)
        return damage_on_hit + damage_per_hit + extra_damage

    def chance_to_hit(self):
        return chance_to_hit(self.bonus_to_hit(), self.enemy_armour_class, self.advantage)

    def chance_of_a_hit(self):
        attacks = self.battle_class.number_of_attacks(self.level)
        return chance_of_an_instance(self.chance_to_hit(), attacks)

    def chance_to_crit(self):
        if self.battle_class.subclass == Subclasses.CHAMPION and self.level >= 3:
            crit_chance = 0.15 if self.level >= 15 else 0.1
        else:
            crit_chance = 0.05
        return round(chance_if_advantage(crit_chance, self.advantage), 8)

    def chance_of_a_crit(self):
        return chance_of_an_instance(self.chance_to_crit(), self.number_of_attacks())

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
        heavy_swing = self.great_weapon_master_swing and (
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

    def pick_weapon(self, weapon):
        if self.battle_class.shadow_blade:
            return SMITH.conjure_shadow_blade(self.battle_class.caster_level())
        return SMITH.draw_weapon(weapon)

    def pick_bonus_weapon(self):
        return SMITH.make_longsword() if self.dual_wielder else SMITH.make_handaxe()
