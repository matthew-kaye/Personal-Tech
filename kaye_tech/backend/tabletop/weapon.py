from dataclasses import dataclass
import math


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

    def magic_bonus(self):
        return 1 if self.magical else 0


@dataclass
class Weapons:
    HANDAXE: Weapon = Weapon(name="Handaxe", damage=3.5, light=True, ranged=True)
    HEAVY_CROSSBOW: Weapon = Weapon(
        name="Heavy Crossbow", damage=5.5, ranged=True, loading=True, heavy=True
    )
    LONGBOW: Weapon = Weapon(name="Longbow", damage=4.5, ranged=True, heavy=True)
    LONGSWORD: Weapon = Weapon(name="Longsword", damage=4.5, versatile=True)
    GREATAXE: Weapon = Weapon(name="Greataxe", damage=6.5, heavy=True)
    GREATSWORD: Weapon = Weapon(name="Greatsword", damage=7, heavy=True)


class Blacksmith:
    def make_weapon(self, weapon_name, magical):
        if weapon_name == Weapons.LONGSWORD.name:
            weapon = Weapons.LONGSWORD
        elif weapon_name == Weapons.HANDAXE.name:
            weapon = Weapons.HANDAXE
        elif weapon_name == Weapons.HEAVY_CROSSBOW.name:
            weapon = Weapons.HEAVY_CROSSBOW
        elif weapon_name == Weapons.LONGBOW.name:
            weapon = Weapons.LONGBOW
        elif weapon_name == Weapons.GREATAXE.name:
            weapon = Weapons.GREATAXE
        elif weapon_name == Weapons.GREATSWORD.name:
            weapon = Weapons.GREATSWORD
        weapon.magical = magical
        return weapon

    def draw_bonus_weapon(self, magical, dual_wielder):
        weapon = Weapons.LONGSWORD if dual_wielder else Weapons.HANDAXE
        weapon.magical = magical
        return weapon

    def conjure_shadow_blade(self, caster_level):
        damage = 9 + 4.5 * min(math.floor((caster_level - 1) / 4), 3)
        return Weapon("Shadow Blade", damage, light=True, ranged=True)
