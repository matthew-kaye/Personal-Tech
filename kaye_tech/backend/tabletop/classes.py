from abc import ABC, abstractmethod
from .utilities import proficiency_bonus_by_level, chance_to_hit, chance_if_advantage
import json
import math


class Classes:
    RANGER = "Ranger"
    FIGHTER = "Fighter"


class Subclasses:
    BATTLE_MASTER = "Battle Master"
    BEAST_MASTER = "Beast Master"
    CHAMPION = "Champion"
    ELDRITCH_KNIGHT = "Eldritch Knight"
    HUNTER = "Hunter"


class Wolf:
    bonus_to_hit: int
    average_damage_die: int = 5
    bite_damage: int
    attacks: int
    chance_to_hit: float
    chance_to_crit: float

    def __init__(self, ranger_level: int, enemy_armour: int, advantage: bool):
        self.bonus_to_hit = 4 + proficiency_bonus_by_level(ranger_level)
        self.bite_damage = 7 + proficiency_bonus_by_level(ranger_level)
        self.number_of_attacks = 2 if ranger_level >= 11 else 1
        self.chance_to_hit = chance_to_hit(
            self.bonus_to_hit, enemy_armour, advantage)
        self.chance_to_crit = chance_if_advantage(0.05, advantage)

    def damage_output(self):
        base_damage = self.bite_damage * self.chance_to_hit
        crit_damage = self.average_damage_die * self.chance_to_crit
        return self.number_of_attacks*(base_damage+crit_damage)


class Class(ABC):
    name: str
    level: int
    fighting_style: str
    superiority_bonus: bool
    hunters_mark: bool
    colossus_slayer: bool
    advantage: bool
    war_magic: bool
    shadow_blade: bool
    subclass: str

    def __init__(self, data):
        abilities = json.loads(data["abilities"])
        bonuses = json.loads(data["bonuses"])
        self.name = data["characterClass"]
        self.level = int(data["characterLevel"])
        self.advantage = bonuses["advantage"]
        self.enemy_armour = int(
            data["averageAC"]) if data["averageAC"] else 0
        self.fighting_style = data["fightingStyle"]
        self.superiority_bonus = abilities["superiority"]
        self.hunters_mark = abilities["huntersMark"]
        self.colossus_slayer = abilities["colossusSlayer"]
        self.wolf_attack = abilities["wolfAttack"]
        self.war_magic = abilities["warMagic"]
        self.shadow_blade = abilities["shadowBlade"]
        self.subclass = data["subclass"]

    @abstractmethod
    def number_of_attacks(self, level):
        pass

    @abstractmethod
    def damage_per_hit(self, level):
        pass

    @abstractmethod
    def damage_on_a_hit(self, level):
        pass

    @abstractmethod
    def other_damage(self, level):
        pass

    @abstractmethod
    def caster_level(self):
        pass


class Ranger(Class):
    def number_of_attacks(self, level):
        return 2 if level >= 5 and not self.wolf_attack else 1

    def damage_per_hit(self, level):
        return 3.5 if self.hunters_mark else 0

    def damage_on_a_hit(self, level):
        return 4.5 if self.colossus_slayer else 0

    def other_damage(self, level):
        if self.wolf_attack:
            companion = Wolf(level, self.enemy_armour, self.advantage)
            return companion.damage_output()
        return 0

    def caster_level(self):
        return 0 if self.level == 1 else math.ceil((self.level)/2)


class Fighter(Class):
    def number_of_attacks(self, level):
        if level == 20:
            return 4
        elif level >= 11:
            return 3
        elif level >= 5:
            return 2
        else:
            return 1

    def damage_per_hit(self, level):
        return 0

    def damage_on_a_hit(self, level):
        if not self.superiority_bonus or level < 3:
            return 0
        if level >= 18:
            return 6.5
        elif level >= 10:
            return 5.5
        elif level >= 3:
            return 4.5

    def other_damage(self, level):
        return 0

    def caster_level(self):
        if self.subclass == Subclasses.ELDRITCH_KNIGHT and self.level >= 3:
            return math.ceil((self.level)/3)
        return 0
