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

    def __eq__(self, other):
        return self.name == other


class Blacksmith:
    def draw_weapon(self, weapon_name):
        if weapon_name == Weapons.LONGSWORD:
            return self.make_longsword()
        elif weapon_name == Weapons.GREATSWORD:
            return self.make_greatsword()
        elif weapon_name == Weapons.GREATAXE:
            return self.make_greataxe()
        elif weapon_name == Weapons.HANDAXE:
            return self.make_handaxe()
        elif weapon_name == Weapons.HEAVY_CROSSBOW:
            return self.make_heavy_crossbow()
        elif weapon_name == Weapons.LONGBOW:
            return self.make_longbow()

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
        damage = 9 + 4.5*min(math.floor((caster_level-1)/4), 3)
        return Weapon(Weapons.SHADOW_BLADE, damage, light=True, ranged=True)
