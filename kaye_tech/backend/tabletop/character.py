from dataclasses import dataclass
from .weapon import Weapon, Blacksmith
import json


@dataclass
class Character:
    weapon: Weapon
    character_class: str
    attack_stat: int
    advantage: bool
    level: int

    def __init__(self, data):
        blacksmith = Blacksmith()
        self.weapon = blacksmith.draw_weapon(data["weapon"])
        self.level = int(data["characterLevel"])
        self.advantage = json.loads(data["bonuses"])["advantage"]
        self.attack_stat = int(data["attackStat"])
        self.character_class = data["characterClass"]
