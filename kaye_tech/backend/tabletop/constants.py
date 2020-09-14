from dataclasses import dataclass


@dataclass
class Styles:
    ARCHERY: str = "Archery"
    DEFENCE: str = "Defence"
    DUELLING: str = "Duelling"
    TWO_HANDED: str = "Two-Handed"
    TWO_WEAPON: str = "Two-Weapon"
    PROTECTION: str = "Protection"


@dataclass
class Classes:
    RANGER: str = "Ranger"
    FIGHTER: str = "Fighter"


@dataclass
class FighterSubclasses:
    BATTLE_MASTER: str = "Battle Master"
    CHAMPION: str = "Champion"
    ELDRITCH_KNIGHT: str = "Eldritch Knight"


@dataclass
class RangerSubclasses:
    BEAST_MASTER: str = "Beast Master"
    HUNTER: str = "Hunter"


@dataclass
class Subclasses:
    FIGHTER: FighterSubclasses = FighterSubclasses()
    RANGER: RangerSubclasses = RangerSubclasses()


class Weapons:
    HANDAXE = "Handaxe"
    HEAVY_CROSSBOW = "Heavy Crossbow"
    LONGBOW = "Longbow"
    LONGSWORD = "Longsword"
    GREATAXE = "Greataxe"
    GREATSWORD = "Greatsword"
    SHADOW_BLADE = "Shadow Blade"
