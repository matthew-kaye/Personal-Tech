from dataclasses import dataclass
from .utilities import proficiency_bonus_by_level
import math


class Weapons:
    HANDAXE = "Handaxe"
    HEAVY_CROSSBOW = "Heavy Crossbow"
    LONGBOW = "Longbow"
    LONGSWORD = "Longsword"
    GREATAXE = "Greataxe"
    GREATSWORD = "Greatsword"
    SHADOW_BLADE = "Shadow Blade"


@dataclass
class Weapon:
    name: str
    damage: float
    heavy: bool = False
    ranged: bool = False
    light: bool = False
    loading: bool = False
    versatile: bool = False
    magical: bool = False

    def __eq__(self, other):
        return self.name == other

    def magic_bonus(self):
        return 1 if self.magical and not self == Weapons.SHADOW_BLADE else 0

    def great_weapon_damage(self):
        weapon_damage = self.damage + 1 if self.versatile else self.damage
        if self.heavy or self.versatile:
            if self == Weapons.GREATSWORD:
                return weapon_damage + 4 / 3
            dice_max = weapon_damage * 2 - 1
            reroll_chance = 2 / dice_max
            return reroll_chance * weapon_damage + (1 - reroll_chance) * (
                weapon_damage + 1
            )
        return self.damage


class Blacksmith:
    def draw_weapon(self, weapon_name, magical):
        if weapon_name == Weapons.LONGSWORD:
            weapon = self.make_longsword()
        elif weapon_name == Weapons.GREATSWORD:
            weapon = self.make_greatsword()
        elif weapon_name == Weapons.GREATAXE:
            weapon = self.make_greataxe()
        elif weapon_name == Weapons.HANDAXE:
            weapon = self.make_handaxe()
        elif weapon_name == Weapons.HEAVY_CROSSBOW:
            weapon = self.make_heavy_crossbow()
        elif weapon_name == Weapons.LONGBOW:
            weapon = self.make_longbow()
        weapon.magical = magical
        return weapon

    def make_longsword(self):
        return Weapon(Weapons.LONGSWORD, 4.5, versatile=True)

    def make_greataxe(self):
        return Weapon(Weapons.GREATAXE, 6.5, heavy=True)

    def make_greatsword(self):
        return Weapon(Weapons.GREATSWORD, 7, heavy=True)

    def make_handaxe(self):
        return Weapon(Weapons.HANDAXE, 3.5, light=True, ranged=True)

    def make_heavy_crossbow(self):
        return Weapon(
            Weapons.HEAVY_CROSSBOW, 5.5, ranged=True, loading=True, heavy=True
        )

    def make_longbow(self):
        return Weapon(Weapons.LONGBOW, 4.5, ranged=True, heavy=True)

    def conjure_shadow_blade(self, caster_level):
        damage = 9 + 4.5 * min(math.floor((caster_level - 1) / 4), 3)
        return Weapon(Weapons.SHADOW_BLADE, damage, light=True, ranged=True)
