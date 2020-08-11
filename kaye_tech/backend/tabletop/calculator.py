from .weapon import Blacksmith
from .character import Character
import json
import math


class Calculator:
    def __init__(self, data):
        self.data = data

    def calculate_damage(self):
        print(self.data)
        character = Character(self.data)
        weapon_damage = character.weapon.damage
        attacks = self.calculate_number_of_attacks(
            character
        )
        armour_class = int(self.data["averageAC"])
        chance_to_hit = self.calculate_chance_to_hit(
            armour_class, character
        )
        crit_chance = self.calculate_chance_of_crit(character.advantage)
        attack_damage = (weapon_damage + character.attack_stat)*chance_to_hit
        crit_damage = weapon_damage*crit_chance
        return (attack_damage + crit_damage)*attacks

    def calculate_chance_to_hit(self, armour_class, character):
        proficiency_bonus = self.calculate_proficiency_bonus(
            character.level
        )
        bonus_to_hit = character.attack_stat + proficiency_bonus
        chance_to_hit = max(1 - (armour_class-1-bonus_to_hit)/20, 0.05)
        chance_to_hit = min(chance_to_hit, 0.95)
        return 1-(1-chance_to_hit) ^ 2 if character.advantage else chance_to_hit

    def calculate_chance_of_crit(self, advantage):
        return 1 - 0.95 ^ 2 if advantage else 0.05

    def calculate_number_of_attacks(self, character):
        if character.weapon.loading:
            return 1
        if character.character_class == "Fighter":
            return self.calculate_fighter_attacks(character.level)
        elif character.character_class == "Ranger":
            return self.calculate_ranger_attacks(character.level)

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

    def calculate_proficiency_bonus(self, level):
        return math.ceil(level/4) + 1
