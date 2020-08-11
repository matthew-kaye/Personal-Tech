from django.test import TestCase
from .tabletop.calculator import Calculator
from .tabletop.character import Character
import json

TEST_DATA = {
    "characterLevel": "11",
    "characterClass": "Fighter",
    "weapon": "Longsword",
    "fightingStyle": "Duelling",
    "subclass": "Eldritch Knight",
    "averageAC": 14,
    "attackStat": 3,
    "bonuses": json.dumps({
        "advantage": False
    })
}

TEST_CALCULATOR = Calculator(TEST_DATA)
TEST_CHARACTER = Character(TEST_DATA)


class CalculatorTest(TestCase):
    def test_calculator_returns_number(self):
        result = TEST_CALCULATOR.calculate_damage()
        assert isinstance(result, float)

    def test_proficiency_bonus_calculation(self):
        assert TEST_CALCULATOR.calculate_proficiency_bonus(1) == 2
        assert TEST_CALCULATOR.calculate_proficiency_bonus(5) == 3
        assert TEST_CALCULATOR.calculate_proficiency_bonus(9) == 4
        assert TEST_CALCULATOR.calculate_proficiency_bonus(13) == 5
        assert TEST_CALCULATOR.calculate_proficiency_bonus(20) == 6

    def test_fighter_attack_calculation(self):
        assert TEST_CALCULATOR.calculate_fighter_attacks(1) == 1
        assert TEST_CALCULATOR.calculate_fighter_attacks(5) == 2
        assert TEST_CALCULATOR.calculate_fighter_attacks(11) == 3
        assert TEST_CALCULATOR.calculate_fighter_attacks(20) == 4

    def test_ranger_attack_calculation(self):
        assert TEST_CALCULATOR.calculate_ranger_attacks(1) == 1
        assert TEST_CALCULATOR.calculate_ranger_attacks(5) == 2

    def test_crit_calculation(self):
        assert TEST_CALCULATOR.calculate_chance_of_crit(False) == 0.05
        assert TEST_CALCULATOR.calculate_chance_of_crit(True) == 0.0975
