from .weapon import Blacksmith
from .character import Character
from .fighting_styles import Styles
import json


class Calculator:
    def __init__(self, data):
        self.enemy_armour_class = int(data["averageAC"])
        self.character = Character(data)

    def calculate_damage(self):
        attacks = self.character.number_of_attacks()
        chance_to_hit = self.chance_to_hit_by_ac(self.enemy_armour_class)
        crit_chance = self.chance_to_crit_by_advantage(self.character.advantage)
        attack_damage = self.calculate_attack_damage() * chance_to_hit
        crit_damage = self.character.weapon.damage * crit_chance
        return (attack_damage + crit_damage) * attacks

    def chance_to_hit_by_ac(self, armour_class):
        bonus_to_hit = self.character.bonus_to_hit()
        chance_to_hit = max(1 - (armour_class - 1 - bonus_to_hit) / 20, 0.05)
        chance_to_hit = min(chance_to_hit, 0.95)
        return (
            1 - (1 - chance_to_hit) ** 2 if self.character.advantage else chance_to_hit
        )

    def chance_to_crit_by_advantage(self, advantage):
        return round(1 - 0.95 ** 2 if advantage else 0.05, 8)

    def calculate_attack_damage(self):
        base_damage = self.character.weapon.damage + self.character.attack_stat
        weapon = self.character.weapon
        if (
            self.character.battle_class.fighting_style == Styles.DUELLING
            and not weapon.heavy
        ):
            return base_damage + 2
        else:
            return base_damage

