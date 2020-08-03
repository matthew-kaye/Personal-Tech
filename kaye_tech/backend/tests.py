from django.test import TestCase
from .tabletop.calculator import Calculator


class CalculatorTest(TestCase):
    def test_running_calculator_method(self):
        test_calculator = Calculator(
            {"characterLevel": 1, "characterClass": "Fighter", "weapon": "Longsword"}
        )
        result = test_calculator.calculate_damage()
        assert isinstance(result, float)
