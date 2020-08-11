# from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    damage: float
    heavy: bool = False
    ranged: bool = False
    light: bool = False
    loading: bool = False
    versatile: bool = False


class Blacksmith:
    def draw_weapon(self, weapon_name):
        if weapon_name == "Longsword":
            return self.make_longsword()
        elif weapon_name == "Greatsword":
            return self.make_greatsword()
        elif weapon_name == "Greataxe":
            return self.make_greataxe()
        elif weapon_name == "Handaxe":
            return self.make_handaxe()
        elif weapon_name == "Heavy Crossbow":
            return self.make_heavy_crossbow()
        elif weapon_name == "Longbow":
            return self.make_longbow()

    def make_longsword(self):
        return Weapon("Longsword", 4.5, versatile=True)

    def make_greataxe(self):
        return Weapon("Greataxe", 6.5, heavy=True)

    def make_greatsword(self):
        return Weapon("Greatsword", 7, heavy=True)

    def make_handaxe(self):
        return Weapon("Handaxe", 3.5, light=True, ranged=True)

    def make_heavy_crossbow(self):
        return Weapon("Heavy Crossbow", 5.5, ranged=True, loading=True, heavy=True)

    def make_longbow(self):
        return Weapon("Longbow", 4.5, ranged=True, heavy=True)
