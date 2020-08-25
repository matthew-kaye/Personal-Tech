from .weapon import Blacksmith
from .character import Character
from .fighting_styles import Styles
import json


class Calculator:
    def __init__(self, data):
        self.enemy_armour_class = int(data["averageAC"]) if data["averageAC"] else 0
        self.character = Character(data)

    def calculate_damage(self):
        attacks = self.character.number_of_attacks()
        chance_to_hit = self.character.chance_to_hit_by_ac(self.enemy_armour_class)
        crit_chance = self.character.chance_to_crit()
        attack_damage = self.calculate_attack_damage() * chance_to_hit
        crit_damage = self.character.average_dice_damage() * crit_chance
        return (attack_damage + crit_damage) * attacks

    def calculate_attack_damage(self):
        base_damage = self.character.average_dice_damage() + self.character.attack_stat
        weapon = self.character.weapon
        if (
            self.character.battle_class.fighting_style == Styles.DUELLING
            and not weapon.heavy
        ):
            return base_damage + 2
        else:
            return base_damage

