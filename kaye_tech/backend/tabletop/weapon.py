from dataclasses import dataclass
from backend.models import Weapon
from .constants import Weapons
import math


@dataclass
class ShadowBlade:
    damage: float
    heavy: bool = False
    ranged: bool = False
    light: bool = False
    loading: bool = False
    versatile: bool = False
    magical: bool = False


class Blacksmith:
    def draw_weapon(self, weapon_name, magical):
        weapon = Weapon.objects.get(name=weapon_name)
        weapon.magical = magical
        return weapon

    def draw_bonus_weapon(self, magical, dual_wielder):
        weapon = Weapons.LONGSWORD if dual_wielder else Weapons.HANDAXE
        return self.draw_weapon(weapon, magical)

    def conjure_shadow_blade(self, caster_level):
        damage = 9 + 4.5 * min(math.floor((caster_level - 1) / 4), 3)
        return ShadowBlade(damage, light=True, ranged=True)
