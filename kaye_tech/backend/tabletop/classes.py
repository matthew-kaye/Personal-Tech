from abc import ABC, abstractmethod


class Classes:
    RANGER = "Ranger"
    FIGHTER = "Fighter"


class Class(ABC):
    name: str
    fighting_style: str

    def __init__(self, data):
        self.name = data["characterClass"]
        self.fighting_style = data["fightingStyle"]

    @abstractmethod
    def number_of_attacks(self, level):
        pass


class Ranger(Class):
    def number_of_attacks(self, level):
        return 2 if level >= 5 else 1


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
