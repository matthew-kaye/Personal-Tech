from .weapon import Blacksmith
from .character import Character
import json
import math


class Calculator:
    def __init__(self, data):
        self.data = data

    def calculate_damage(self):
        character = Character(self.data)
        weapon_damage = character.weapon.damage
        attacks = character.number_of_attacks()
        armour_class = int(self.data["averageAC"])
        chance_to_hit = self.calculate_chance_to_hit(
            armour_class, character
        )
        crit_chance = self.calculate_chance_of_crit(character.advantage)
        attack_damage = self.calculate_attack_damage(character) *chance_to_hit
        crit_damage = character.weapon.damage*crit_chance
        return (attack_damage + crit_damage)*attacks

    def calculate_chance_to_hit(self, armour_class, character):
        proficiency_bonus = self.calculate_proficiency_bonus(
            character.level
        )
        bonus_to_hit = character.attack_stat + proficiency_bonus
        chance_to_hit = max(1 - (armour_class-1-bonus_to_hit)/20, 0.05)
        chance_to_hit = min(chance_to_hit, 0.95)
        return 1-(1-chance_to_hit) ** 2 if character.advantage else chance_to_hit

    def calculate_chance_of_crit(self, advantage):
        return round(1 - 0.95 ** 2 if advantage else 0.05, 8)

    def calculate_attack_damage(self, character):
        base_damage = character.weapon.damage + character.attack_stat
        if character.battle_class.fighting_style=="Duelling" and (character.weapon.light or character.weapon.versatile):
            return base_damage+2
        else:
            return base_damage

    def calculate_proficiency_bonus(self, level):
        return math.ceil(level/4) + 1
