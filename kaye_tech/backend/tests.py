from django.test import TestCase
from .tabletop.calculator import Calculator

TEST_DATA = {
    "characterLevel": 11,
    "characterClass": "Fighter",
    "weapon": "Longsword",
    "fightingStyle": "Duelling",
    "subclass": "Eldritch Knight",
    "averageAC": 14,
    "attackStat": 3,
}


class CalculatorTest(TestCase):
    def test_running_calculator_method(self):
        test_calculator = Calculator(TEST_DATA)
        result = test_calculator.calculate_damage()
        print(result)
        assert isinstance(result, float)
