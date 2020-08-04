from dataclasses import dataclass
from .weapon import Weapon


@dataclass
class Character:
    weapon: Weapon
    characterClass: CharacterClass
    level: int = 1


@dataclass
class CharacterClass:
    name: str
