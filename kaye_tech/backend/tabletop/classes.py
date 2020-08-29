from abc import ABC, abstractmethod
import json


class Classes:
    RANGER = "Ranger"
    FIGHTER = "Fighter"


class Class(ABC):
    name: str
    fighting_style: str
    superiority_bonus: bool
    hunters_mark: bool
    colossus_slayer: bool

    def __init__(self, data):
        abilities = json.loads(data["abilities"])
        self.name = data["characterClass"]
        self.fighting_style = data["fightingStyle"]
        self.superiority_bonus = abilities["superiority"]
        self.hunters_mark = abilities["huntersMark"]
        self.colossus_slayer = abilities["colossusSlayer"]

    @abstractmethod
    def number_of_attacks(self, level):
        pass

    @abstractmethod
    def damage_per_hit(self, level):
        pass

    @abstractmethod
    def damage_on_a_hit(self, level):
        pass


class Ranger(Class):
    def number_of_attacks(self, level):
        return 2 if level >= 5 else 1

    def damage_per_hit(self, level):
        return 3.5 if self.hunters_mark else 0

    def damage_on_a_hit(self, level):
        return 4.5 if self.colossus_slayer else 0


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
