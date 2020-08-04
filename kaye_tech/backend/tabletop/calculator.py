from .weapon import Blacksmith


class Calculator:
    def __init__(self, data):
        self.data = data

    def calculate_damage(self):
        weapon = self.draw_weapon()
        attacks = 1 if weapon.loading else self.calculate_number_of_attacks(weapon)
        return float(weapon.damage) * attacks

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

    def calculate_number_of_attacks(self, weapon):
        characterClass = self.data["characterClass"]
        characterLevel = self.data["characterLevel"]
        if characterClass == "Fighter":
            return self.calculate_fighter_attacks(characterLevel)
        elif characterClass == "Ranger":
            return self.calculate_ranger_attacks(characterLevel)

    def calculate_fighter_attacks(self, level):
        if level == 20:
            return 4
        elif level >= 11:
            return 3
        elif level >= 5:
            return 2
        else:
            return 1

    def calculate_ranger_attacks(self, level):
        if level >= 5:
            return 2
        else:
            return 1
