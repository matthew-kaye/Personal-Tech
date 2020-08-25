from django.test import TestCase
from .tabletop.character import Character, Classes, Subclasses
from .tabletop.weapon import Weapon, Weapons, Blacksmith
from .tabletop.fighting_styles import Styles
import json
from dataclasses import dataclass


@dataclass
class TestData:
    character_level: int = 11
    character_class: str = Classes.FIGHTER
    weapon: str = Weapons.LONGSWORD
    fighting_style: str = Styles.DEFENCE
    subclass: str = Subclasses.ELDRITCH_KNIGHT
    average_AC: int = 17
    attack_stat: int = 5

    def data(self, bonuses=None):
        return {
            "characterLevel": self.character_level,
            "characterClass": self.character_class,
            "weapon": self.weapon,
            "fightingStyle": self.fighting_style,
            "subclass": self.subclass,
            "averageAC": self.average_AC,
            "attackStat": self.attack_stat,
            "bonuses": json.dumps(bonuses if bonuses else {"advantage": False}),
        }


TEST_CHARACTER = Character(TestData().data())
TEST_SMITH = Blacksmith()


class CharacterTest(TestCase):
    def test_damage_output_returns_number(self):
        result = TEST_CHARACTER.damage_output()
        assert isinstance(result, float)

    def test_attack_damage_calculation(self):
        assert TEST_CHARACTER.calculate_attack_damage() == 9.5
        duellist = Character(TestData(fighting_style=Styles.DUELLING).data())
        assert duellist.calculate_attack_damage() == 11.5

    def test_proficiency_bonus_calculation(self):
        assert TEST_CHARACTER.proficiency_bonus_by_level(1) == 2
        assert TEST_CHARACTER.proficiency_bonus_by_level(5) == 3
        assert TEST_CHARACTER.proficiency_bonus_by_level(9) == 4
        assert TEST_CHARACTER.proficiency_bonus_by_level(13) == 5
        assert TEST_CHARACTER.proficiency_bonus_by_level(20) == 6

    def test_chance_to_hit_calculation(self):
        assert TEST_CHARACTER.chance_to_hit_by_ac(1) == 0.95
        assert TEST_CHARACTER.chance_to_hit_by_ac(17) == 0.65
        assert TEST_CHARACTER.chance_to_hit_by_ac(20) == 0.5
        assert TEST_CHARACTER.chance_to_hit_by_ac(30) == 0.05
        assert TEST_CHARACTER.chance_to_crit() == 0.05

    def test_flanking_hit_chance_calculation(self):
        flanker = Character(TestData().data({"advantage": True}))
        assert round(flanker.chance_to_hit_by_ac(0), 6) == 0.9975
        assert round(flanker.chance_to_hit_by_ac(17), 6) == 0.8775
        assert flanker.chance_to_crit() == 0.0975

    def test_fighter_attack_calculation(self):
        assert TEST_CHARACTER.fighter_attacks_by_level(1) == 1
        assert TEST_CHARACTER.fighter_attacks_by_level(5) == 2
        assert TEST_CHARACTER.fighter_attacks_by_level(11) == 3
        assert TEST_CHARACTER.fighter_attacks_by_level(20) == 4

    def test_ranger_attack_calculation(self):
        assert TEST_CHARACTER.ranger_attacks_by_level(1) == 1
        assert TEST_CHARACTER.ranger_attacks_by_level(5) == 2

    def test_archery_bonus_calculation(self):
        assert TEST_CHARACTER.bonus_to_hit() == 9
        archer = Character(
            TestData(fighting_style=Styles.ARCHERY, weapon=Weapons.LONGBOW).data()
        )
        assert archer.bonus_to_hit() == 11

    def test_great_weapon_fighting_bonus(self):
        greatsword = TEST_SMITH.draw_weapon(Weapons.GREATSWORD)
        longsword = TEST_SMITH.draw_weapon(Weapons.LONGSWORD)
        greatswordsman = Character(
            TestData(fighting_style=Styles.TWO_HANDED, weapon=Weapons.GREATSWORD).data()
        )
        two_handed_swordsman = Character(
            TestData(fighting_style=Styles.TWO_HANDED).data()
        )
        assert TEST_CHARACTER.average_dice_damage() == 4.5
        assert greatswordsman.average_dice_damage() == 25 / 3
        assert round(two_handed_swordsman.average_dice_damage(), 1) == 6.3

    def test_bonus_attack_damage(self):
        axe_wielder = Character(
            TestData(fighting_style=Styles.TWO_WEAPON, weapon=Weapons.HANDAXE).data()
        )
        assert TEST_CHARACTER.bonus_attack_damage() == 0
        assert axe_wielder.bonus_attack_damage() == 5.7
