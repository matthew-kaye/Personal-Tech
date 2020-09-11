from dataclasses import dataclass
from .weapon import Weapon, Blacksmith
from .subclasses import (
    Champion,
    EldritchKnight,
    BattleMaster,
    BeastMaster,
    Hunter,
    Subclasses,
)
from .classes import Class
from .utilities import (
    proficiency_bonus_by_level,
    chance_to_hit,
    chance_of_an_instance,
    chance_to_critical,
)
import json

SMITH = Blacksmith()


@dataclass
class Character:
    weapon: Weapon
    bonus_weapon: Weapon
    subclass: Class
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
        self.bonus_weapon = SMITH.draw_bonus_weapon(
            bonuses["magicWeapon"], self.dual_wielder
        )

    def damage_data(self):
        extra_damage_on_move = (
            self.booming_blade_damage_on_move() if self.subclass.war_magic else 0
        )
        return {
            "damage": self.damage_output(),
            "damageIfMoves": self.damage_output() + extra_damage_on_move,
        }

    def damage_output(self):
        bonus_damage = self.bonus_attack_damage() + self.ability_damage()
        return round(
            self.average_attack_damage() * self.number_of_attacks() + bonus_damage, 8
        )

    def number_of_attacks(self):
        if self.weapon.loading and not self.crossbow_expert:
            return 1
        return self.subclass.number_of_attacks(self.level)

    def average_attack_damage(self):
        attack_damage = self.attack_damage() * self.chance_to_hit()
        critical_damage = self.average_dice_damage() * self.chance_to_critical()
        return attack_damage + critical_damage

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
            return round(self.average_attack_damage() * self.chance_to_critical(), 8)
        return 0

    def second_weapon_damage(self):
        if self.subclass.shadow_blade:
            bonus_to_hit = self.bonus_to_hit() + self.bonus_weapon.magic_bonus()
            hit_chance = chance_to_hit(
                bonus_to_hit, self.enemy_armour_class, self.advantage
            )
        else:
            hit_chance = self.chance_to_hit()
        if self.bonus_weapon.light or (
            self.dual_wielder and not self.bonus_weapon.heavy
        ):
            return round(
                (
                    self.bonus_weapon.damage
                    + self.attack_stat
                    + self.bonus_weapon.magic_bonus()
                )
                * hit_chance
                + self.bonus_weapon.damage * self.chance_to_critical(),
                8,
            )
        return 0

    def ability_damage(self):
        damage_on_hit = self.subclass.damage_on_a_hit() * (
            self.chance_of_a_hit() + self.chance_of_a_critical()
        )
        per_hit_chance = self.chance_to_hit() + self.chance_to_critical()
        damage_per_hit = (
            self.subclass.damage_per_hit() * self.number_of_attacks() * per_hit_chance
        )
        extra_damage = self.subclass.other_damage() + (
            self.subclass.booming_blade_damage() * per_hit_chance
            if self.subclass.war_magic
            else 0
        )
        return round(damage_on_hit + damage_per_hit + extra_damage, 8)

    def booming_blade_damage_on_move(self):
        return (self.subclass.booming_blade_damage() + 4.5) * self.chance_to_hit()

    def chance_to_hit(self):
        return chance_to_hit(
            self.bonus_to_hit(), self.enemy_armour_class, self.advantage
        )

    def chance_of_a_hit(self):
        attacks = self.subclass.number_of_attacks(self.level)
        return chance_of_an_instance(self.chance_to_hit(), attacks)

    def chance_to_critical(self):
        return chance_to_critical(self.subclass.critical_chance(), self.advantage)

    def chance_of_a_critical(self):
        return chance_of_an_instance(
            self.chance_to_critical(), self.number_of_attacks()
        )

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
