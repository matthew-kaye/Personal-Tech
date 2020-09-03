from dataclasses import dataclass
from .weapon import Weapon, Weapons, Blacksmith
from .subclasses import (
    Champion,
    EldritchKnight,
    BattleMaster,
    BeastMaster,
    Hunter,
    Subclasses,
)
from .classes import Classes, Class
from .utilities import (
    proficiency_bonus_by_level,
    chance_to_hit,
    chance_of_an_instance,
    chance_if_advantage,
)
from abc import ABC, abstractmethod
import json

SMITH = Blacksmith()


@dataclass
class Character:
    weapon: Weapon
    bonus_weapon: Weapon
    subclass: Class
    subclass: str
    attack_stat: int
    advantage: bool
    level: int
    proficiency_bonus: int
    enemy_armour_class: int
    dual_wielder: bool
    sharpshooter: bool
    great_weapon_master: bool

    def __init__(self, data):
        bonuses = json.loads(data["bonuses"])
        abilities = json.loads(data["abilities"])
        feats = json.loads(data["feats"])
        self.level = int(data["characterLevel"])
        self.proficiency_bonus = proficiency_bonus_by_level(self.level)
        self.enemy_armour_class = int(data["averageAC"]) if data["averageAC"] else 0
        if data["subclass"] == Subclasses.CHAMPION:
            self.subclass = Champion(data)
        elif data["subclass"] == Subclasses.BATTLE_MASTER:
            self.subclass = BattleMaster(data)
        elif data["subclass"] == Subclasses.ELDRITCH_KNIGHT:
            self.subclass = EldritchKnight(data)
        elif data["subclass"] == Subclasses.BEAST_MASTER:
            self.subclass = BeastMaster(data)
        elif data["subclass"] == Subclasses.HUNTER:
            self.subclass = Hunter(data)
        self.weapon = self.pick_weapon(data["weapon"], bonuses["magicWeapon"])
        self.advantage = bonuses["advantage"]
        self.dual_wielder = feats["dualWielder"]
        self.sharpshooter = feats["sharpshooter"]
        self.great_weapon_master = feats["greatWeaponMaster"]
        self.great_weapon_master_swing = feats["greatWeaponMasterSwing"]
        self.crossbow_expert = feats["crossbowExpert"]
        self.attack_stat = int(data["attackStat"])
        self.bonus_weapon = self.pick_bonus_weapon(bonuses["magicWeapon"])

    def damage_output(self):
        bonus_damage = self.bonus_attack_damage() + self.ability_damage()
        return self.average_attack_damage() * self.number_of_attacks() + bonus_damage

    def number_of_attacks(self):
        if self.weapon.loading and not self.crossbow_expert:
            return 1
        return self.subclass.number_of_attacks(self.level)

    def average_attack_damage(self):
        attack_damage = self.attack_damage() * self.chance_to_hit()
        crit_damage = self.average_dice_damage() * self.chance_to_crit()
        return attack_damage + crit_damage

    def attack_damage(self):
        base_damage = (
            self.average_dice_damage() + self.attack_stat + self.weapon.magic_bonus()
        )
        if self.attempting_bigger_hit():
            return base_damage + 10
        else:
            return base_damage + self.subclass.style_damage(self.weapon)

    def average_dice_damage(self):
        return self.subclass.average_dice_damage(self.weapon)

    def bonus_attack_damage(self):
        if self.subclass.two_weapons:
            return self.second_weapon_damage()
        elif self.great_weapon_master:
            return self.average_attack_damage() * self.chance_to_crit()
        return 0

    def second_weapon_damage(self):
        if self.weapon == Weapons.SHADOW_BLADE:
            bonus_to_hit = self.bonus_to_hit() + self.bonus_weapon.magic_bonus()
            hit_chance = chance_to_hit(
                bonus_to_hit, self.enemy_armour_class, self.advantage
            )
        else:
            hit_chance = self.chance_to_hit()
        if self.bonus_weapon.light or (
            self.dual_wielder and not self.bonus_weapon.heavy
        ):
            return (
                self.bonus_weapon.damage
                + self.attack_stat
                + self.bonus_weapon.magic_bonus()
            ) * hit_chance + self.bonus_weapon.damage * self.chance_to_crit()
        return 0

    def ability_damage(self):
        damage_on_hit = self.subclass.damage_on_a_hit() * (
            self.chance_of_a_hit() + self.chance_of_a_crit()
        )
        per_hit_chance = self.chance_to_hit() + self.chance_to_crit()
        damage_per_hit = (
            self.subclass.damage_per_hit() * self.number_of_attacks() * (per_hit_chance)
        )
        extra_damage = self.subclass.other_damage() + (
            self.subclass.booming_blade_damage() * per_hit_chance
            if self.subclass.war_magic
            else 0
        )
        return damage_on_hit + damage_per_hit + extra_damage

    def chance_to_hit(self):
        return chance_to_hit(
            self.bonus_to_hit(), self.enemy_armour_class, self.advantage
        )

    def chance_of_a_hit(self):
        attacks = self.subclass.number_of_attacks(self.level)
        return chance_of_an_instance(self.chance_to_hit(), attacks)

    def chance_to_crit(self):
        return round(
            chance_if_advantage(self.subclass.crit_chance(), self.advantage), 8
        )

    def chance_of_a_crit(self):
        return chance_of_an_instance(self.chance_to_crit(), self.number_of_attacks())

    def bonus_to_hit(self):
        base_bonus = (
            self.attack_stat + self.proficiency_bonus + self.weapon.magic_bonus()
        )
        style_bonus = self.subclass.style_bonus(self.weapon)
        ability_modifier = -5 if self.attempting_bigger_hit() else 0
        return base_bonus + style_bonus + ability_modifier

    def attempting_bigger_hit(self):
        sharpshooting = self.sharpshooter and self.weapon.ranged
        heavy_swing = self.great_weapon_master_swing and (
            self.weapon.heavy or self.weapon.versatile
        )
        return sharpshooting or heavy_swing

    def pick_weapon(self, weapon, magical):
        if self.subclass.shadow_blade:
            return SMITH.conjure_shadow_blade(self.subclass.caster_level())
        return SMITH.draw_weapon(weapon, magical)

    def pick_bonus_weapon(self, magical):
        weapon = Weapons.LONGSWORD if self.dual_wielder else Weapons.HANDAXE
        return SMITH.draw_weapon(weapon, magical)
