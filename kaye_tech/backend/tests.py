from django.test import TestCase
from .tabletop.character import Character
from .tabletop.subclasses import (
    Champion,
    EldritchKnight,
    BattleMaster,
    BeastMaster,
    Hunter,
    Subclasses,
)
from .tabletop.classes import Classes, Wolf
from .tabletop.weapon import Weapons, Blacksmith
from .tabletop.fighting_styles import Styles
from .tabletop.utilities import (
    proficiency_bonus_by_level,
    chance_to_hit,
    chance_of_an_instance,
    chance_to_critical,
)
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
    sharpshooter: bool = False
    great_weapon_master: bool = False
    great_weapon_master_swing: bool = False
    dual_wielder: bool = False
    crossbow_expert: bool = False
    advantage: bool = False
    magic_weapon: bool = False
    superiority: bool = False
    hunters_mark: bool = False
    colossus_slayer: bool = False
    wolf_attack: bool = False
    war_magic: bool = False
    shadow_blade: bool = False
    caster_multiclasses: int = 0

    def data(self):
        return {
            "characterLevel": self.character_level,
            "characterClass": self.character_class,
            "weapon": self.weapon,
            "fightingStyle": self.fighting_style,
            "subclass": self.subclass,
            "averageAC": self.average_AC,
            "attackStat": self.attack_stat,
            "casterMulticlasses": self.caster_multiclasses,
            "bonuses": json.dumps(
                {"advantage": self.advantage, "magicWeapon": self.magic_weapon}
            ),
            "abilities": json.dumps(
                {
                    "superiority": self.superiority,
                    "huntersMark": self.hunters_mark,
                    "colossusSlayer": self.colossus_slayer,
                    "wolfAttack": self.wolf_attack,
                    "warMagic": self.war_magic,
                    "shadowBlade": self.shadow_blade,
                }
            ),
            "feats": json.dumps(
                {
                    "dualWielder": self.dual_wielder,
                    "sharpshooter": self.sharpshooter,
                    "greatWeaponMaster": self.great_weapon_master,
                    "greatWeaponMasterSwing": self.great_weapon_master_swing,
                    "crossbowExpert": self.crossbow_expert,
                }
            ),
        }


TEST_CHARACTER = Character(TestData().data())
SMITH = Blacksmith()


class CharacterTest(TestCase):
    def test_damage_output_returns_number(self):
        result = TEST_CHARACTER.damage_output()
        assert isinstance(result, float)

    def test_attack_damage_calculation(self):
        assert TEST_CHARACTER.attack_damage() == 9.5
        assert TEST_CHARACTER.ability_damage() == 0
        duellist = Character(TestData(fighting_style=Styles.DUELLING).data())
        assert duellist.attack_damage() == 11.5

    def test_number_of_attacks(self):
        crossbowman = Character(TestData(weapon=Weapons.HEAVY_CROSSBOW).data())
        assert crossbowman.number_of_attacks() == 1
        assert TEST_CHARACTER.number_of_attacks() == 3

    def test_chance_to_hit_calculation(self):
        assert TEST_CHARACTER.chance_to_hit() == 0.65
        assert TEST_CHARACTER.chance_to_critical() == 0.05

    def test_flanking_hit_chance_calculation(self):
        flanker = Character(TestData(advantage=True).data())
        assert flanker.chance_to_hit() == 0.8775
        assert flanker.chance_to_critical() == 0.0975

    def test_archery_bonus_calculation(self):
        assert TEST_CHARACTER.bonus_to_hit() == 9
        archer = Character(
            TestData(fighting_style=Styles.ARCHERY, weapon=Weapons.LONGBOW).data()
        )
        assert archer.bonus_to_hit() == 11

    def test_great_weapon_fighting_bonus(self):
        greatsword = SMITH.draw_weapon(Weapons.GREATSWORD, False)
        longsword = SMITH.draw_weapon(Weapons.LONGSWORD, False)
        assert greatsword.great_weapon_damage() == 25 / 3
        assert longsword.great_weapon_damage() == 6.3
        greatswordsman = Character(
            TestData(fighting_style=Styles.TWO_HANDED, weapon=Weapons.GREATSWORD).data()
        )
        two_handed_swordsman = Character(
            TestData(fighting_style=Styles.TWO_HANDED).data()
        )
        assert TEST_CHARACTER.average_dice_damage() == 4.5
        assert greatswordsman.average_dice_damage() == 25 / 3
        assert two_handed_swordsman.average_dice_damage() == 6.3

    def test_bonus_attack_damage(self):
        axe_wielder = Character(
            TestData(fighting_style=Styles.TWO_WEAPON, weapon=Weapons.HANDAXE).data()
        )
        assert TEST_CHARACTER.bonus_attack_damage() == 0
        assert axe_wielder.bonus_attack_damage() == 5.7

    def test_magic_weapon(self):
        magic_swordsman = Character(TestData(magic_weapon=True).data())
        magic_sword = SMITH.draw_weapon(Weapons.LONGSWORD, True)
        assert magic_sword.magic_bonus() == TEST_CHARACTER.weapon.magic_bonus() + 1
        assert SMITH.conjure_shadow_blade(10).magic_bonus() == 0
        assert magic_swordsman.attack_damage() == TEST_CHARACTER.attack_damage() + 1
        assert magic_swordsman.bonus_to_hit() == TEST_CHARACTER.bonus_to_hit() + 1
        magic_dual_wielder = Character(
            TestData(
                fighting_style=Styles.TWO_WEAPON, shadow_blade=True, magic_weapon=True
            ).data()
        )
        assert magic_dual_wielder.second_weapon_damage() == 6.825
        assert round(magic_dual_wielder.damage_output(), 1) == 35.5


class FeatsTest(TestCase):
    def test_big_hit_abilities(self):
        sharpshooter = Character(
            TestData(
                weapon=Weapons.LONGBOW, fighting_style=Styles.ARCHERY, sharpshooter=True
            ).data()
        )
        great_weapon_master = Character(
            TestData(
                weapon=Weapons.GREATSWORD,
                fighting_style=Styles.TWO_HANDED,
                great_weapon_master=True,
                great_weapon_master_swing=True,
            ).data()
        )
        assert great_weapon_master.bonus_to_hit() == 4
        assert great_weapon_master.bonus_attack_damage() == 0.4875
        assert round(great_weapon_master.attack_damage(), 8) == round(70 / 3, 8)
        assert sharpshooter.bonus_to_hit() == 6
        assert sharpshooter.attack_damage() == 19.5

    def test_dual_wielding_bonus(self):
        double_swordsman = Character(
            TestData(fighting_style=Styles.TWO_WEAPON, dual_wielder=True).data()
        )
        assert double_swordsman.bonus_attack_damage() == 6.4

    def test_crossbow_expert(self):
        crossbowman = Character(
            TestData(
                weapon=Weapons.HEAVY_CROSSBOW,
                crossbow_expert=True,
                fighting_style=Styles.ARCHERY,
            ).data()
        )
        assert crossbowman.number_of_attacks() == 3
        assert crossbowman.damage_output() == 24.45


class UtilitiesTest(TestCase):
    def test_proficiency_bonus_calculation(self):
        assert proficiency_bonus_by_level(1) == 2
        assert proficiency_bonus_by_level(5) == 3
        assert proficiency_bonus_by_level(9) == 4
        assert proficiency_bonus_by_level(13) == 5
        assert proficiency_bonus_by_level(20) == 6

    def test_chance_to_hit_calculation(self):
        assert chance_to_hit(5, 1, advantage=False) == 0.95
        assert chance_to_hit(5, 1, advantage=True) == 0.9975
        assert chance_to_hit(5, 1, disadvantage=True) == 0.9025
        assert chance_to_hit(9, 17, advantage=False) == 0.65
        assert chance_to_hit(9, 17, True, True) == 0.65
        assert chance_to_hit(0, 30, advantage=False) == 0.05
        assert chance_to_hit(0, 30, advantage=True) == 0.0975
        assert chance_to_hit(0, 30, disadvantage=True) == 0.0025

    def test_chance_of_an_instance(self):
        assert chance_of_an_instance(0.5, 2) == 0.75

    def test_chance_to_critical(self):
        assert chance_to_critical(0.9, advantage=True) == 0.99
        assert chance_to_critical(0.9, disadvantage=True) == 0.81
        assert chance_to_critical(0.9, True, True) == 0.9


class ClassTest(TestCase):
    def test_fighter_attack_calculation(self):
        assert Champion(TestData().data()).number_of_attacks(1) == 1
        assert Champion(TestData().data()).number_of_attacks(5) == 2
        assert Champion(TestData().data()).number_of_attacks(11) == 3
        assert Champion(TestData().data()).number_of_attacks(20) == 4

    def test_ranger_attack_calculation(self):
        assert Hunter(TestData().data()).number_of_attacks(1) == 1
        assert Hunter(TestData().data()).number_of_attacks(5) == 2

    def test_battle_master_abilities(self):
        battle_master_data = TestData(
            subclass=Subclasses.BATTLE_MASTER, superiority=True
        ).data()
        assert BattleMaster(battle_master_data).damage_on_a_hit() == 5.5
        battle_master = Character(battle_master_data)
        assert battle_master.ability_damage() == 6.048625
        assert battle_master.damage_output() == 25.248625

    def test_ranger_abilities(self):
        hunter = Character(
            TestData(subclass=Subclasses.HUNTER, hunters_mark=True).data()
        )
        assert hunter.ability_damage() == 4.9
        assert hunter.damage_output() == 17.7
        hunter.subclass.colossus_slayer = True
        assert hunter.ability_damage() == 9.2875
        assert hunter.damage_output() == 22.0875

    def test_ranger_wolf_damage(self):
        wolf = Wolf(5, 0, False)
        bigger_wolf = Wolf(11, 0, False)
        assert wolf.bonus_to_hit == 7 and wolf.bite_damage == 10
        assert wolf.number_of_attacks == 1
        assert bigger_wolf.number_of_attacks == 2
        assert bigger_wolf.bonus_to_hit == 8 and bigger_wolf.bite_damage == 11
        beast_master_data = TestData(
            subclass=Subclasses.BEAST_MASTER, wolf_attack=True
        ).data()
        beast_master = Character(beast_master_data)
        assert beast_master.damage_output() == 20.1
        assert BeastMaster(beast_master_data).other_damage() == 13.7
        beast_master.advantage = True
        flanking_beast_master = Character(
            TestData(
                subclass=Subclasses.BEAST_MASTER, wolf_attack=True, advantage=True
            ).data()
        )
        assert flanking_beast_master.damage_output() == 28.23

    def test_shadow_blade_damage(self):
        for caster_level in range(3, 5):
            assert SMITH.conjure_shadow_blade(4).damage == 9
        for caster_level in range(5, 9):
            assert SMITH.conjure_shadow_blade(caster_level).damage == 13.5
        for caster_level in range(9, 13):
            assert SMITH.conjure_shadow_blade(caster_level).damage == 18
        for caster_level in range(13, 21):
            assert SMITH.conjure_shadow_blade(caster_level).damage == 22.5
        assert Character(TestData(shadow_blade=True).data()).damage_output() == 28.65
        two_hander = Character(
            TestData(
                fighting_style=Styles.TWO_WEAPON,
                weapon=Weapons.HANDAXE,
                shadow_blade=True,
            ).data()
        )
        assert two_hander.bonus_attack_damage() == 5.7
        assert two_hander.damage_output() == 34.35
        dual_wielder = Character(
            TestData(
                fighting_style=Styles.TWO_WEAPON,
                weapon=Weapons.HANDAXE,
                shadow_blade=True,
                dual_wielder=True,
            ).data()
        )
        assert round(dual_wielder.bonus_attack_damage(), 6) == 6.4
        assert dual_wielder.damage_output() == 35.05

    def test_booming_blade_damage(self):
        assert TEST_CHARACTER.subclass.booming_blade_damage() == 9
        assert (
            EldritchKnight(TestData(character_level=17).data()).booming_blade_damage()
            == 13.5
        )
        eldritch_knight = EldritchKnight(TestData(character_level=7).data())
        assert eldritch_knight.booming_blade_damage() == 4.5
        assert eldritch_knight.caster_level() == 3
        assert Character(TestData(war_magic=True).data()).damage_output() == 19.1

    def test_multiclass_slots(self):
        multiclasser = EldritchKnight(
            TestData(character_level=7, caster_multiclasses=4).data()
        )
        assert multiclasser.caster_level() == 6
        assert multiclasser.booming_blade_damage() == 9
