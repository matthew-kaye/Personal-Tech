from django.test import TestCase
from .tabletop.calculator import Calculator
from .tabletop.character import Character
from .tabletop.weapon import Weapon, Blacksmith
import json
from dataclasses import dataclass


@dataclass
class TestData:
    characterLevel: int = 11
    characterClass: str = "Fighter"
    weapon: str = "Longsword"
    fightingStyle: str = "Defence"
    subclass: str = "Eldritch Knight"
    averageAC: int = 16
    attackStat: int = 5

    def data(self, bonuses=None):
        return {
            "characterLevel": self.characterLevel,
            "characterClass": self.characterClass,
            "weapon": self.weapon,
            "fightingStyle": self.fightingStyle,
            "subclass": self.subclass,
            "averageAC": self.averageAC,
            "attackStat": self.attackStat,
            "bonuses": json.dumps(bonuses if bonuses else {"advantage": False}),
        }


TEST_CALCULATOR = Calculator(TestData().data())
TEST_CHARACTER = Character(TestData().data())


class CalculatorTest(TestCase):
    def test_calculator_returns_number(self):
        result = TEST_CALCULATOR.calculate_damage()
        assert isinstance(result, float)

    def test_crit_calculation(self):
        assert TEST_CALCULATOR.chance_to_crit_by_advantage(False) == 0.05
        assert TEST_CALCULATOR.chance_to_crit_by_advantage(True) == 0.0975

    def test_chance_to_hit_calculation(self):
        assert TEST_CALCULATOR.chance_to_hit_by_ac(20) == 0.5
        assert TEST_CALCULATOR.chance_to_hit_by_ac(30) == 0.05
        assert TEST_CALCULATOR.chance_to_hit_by_ac(1) == 0.95

    def test_attack_damage_calculation(self):
        assert TEST_CALCULATOR.calculate_attack_damage() == 9.5
        TEST_DUELLIST_CALCULATOR = Calculator(TestData(fightingStyle="Duelling").data())
        assert TEST_DUELLIST_CALCULATOR.calculate_attack_damage() == 11.5


class CharacterTest(TestCase):
    def test_proficiency_bonus_calculation(self):
        assert TEST_CHARACTER.proficiency_bonus_by_level(1) == 2
        assert TEST_CHARACTER.proficiency_bonus_by_level(5) == 3
        assert TEST_CHARACTER.proficiency_bonus_by_level(9) == 4
        assert TEST_CHARACTER.proficiency_bonus_by_level(13) == 5
        assert TEST_CHARACTER.proficiency_bonus_by_level(20) == 6

    def test_fighter_attack_calculation(self):
        assert TEST_CHARACTER.fighter_attacks_by_level(1) == 1
        assert TEST_CHARACTER.fighter_attacks_by_level(5) == 2
        assert TEST_CHARACTER.fighter_attacks_by_level(11) == 3
        assert TEST_CHARACTER.fighter_attacks_by_level(20) == 4

    def test_ranger_attack_calculation(self):
        assert TEST_CHARACTER.ranger_attacks_by_level(1) == 1
        assert TEST_CHARACTER.ranger_attacks_by_level(5) == 2

    def test_ranger_attack_calculation(self):
        assert TEST_CHARACTER.bonus_to_hit() == 9
        archer = Character(TestData(fightingStyle="Archery", weapon="Longbow").data())
        assert archer.bonus_to_hit() == 11
