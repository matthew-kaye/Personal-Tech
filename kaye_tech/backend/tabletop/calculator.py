from .weapon import Blacksmith


class Calculator:
    def __init__(self, data):
        self.data = data

    def calculate_damage(self):
        weapon = self.draw_weapon()
        return float(weapon.damage)

    def draw_weapon(self):
        blacksmith = Blacksmith()
        weapon_name = self.data["weapon"]
        if weapon_name == "Longsword":
            return blacksmith.make_longsword()
        elif weapon_name == "Greatsword":
            return blacksmith.make_greatsword()
        elif weapon_name == "Greataxe":
            return blacksmith.make_greataxe()
        elif weapon_name == "Handaxe":
            return blacksmith.make_handaxe()
        elif weapon_name == "Heavy Crossbow":
            return blacksmith.make_heavy_crossbow()
        elif weapon_name == "Longbow":
            return blacksmith.make_longbow()
