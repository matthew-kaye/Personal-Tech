from dataclasses import dataclass


@dataclass
class Styles:
    ARCHERY: str = "Archery"
    DEFENCE: str = "Defence"
    DUELLING: str = "Duelling"
    TWO_HANDED: str = "Two-Handed"
    TWO_WEAPON: str = "Two-Weapon"
    PROTECTION: str = "Protection"


class Classes:
    RANGER = "Ranger"
    FIGHTER = "Fighter"


class Subclasses:
    BATTLE_MASTER = "Battle Master"
    BEAST_MASTER = "Beast Master"
    CHAMPION = "Champion"
    ELDRITCH_KNIGHT = "Eldritch Knight"
    HUNTER = "Hunter"


class Weapons:
    HANDAXE = "Handaxe"
    HEAVY_CROSSBOW = "Heavy Crossbow"
    LONGBOW = "Longbow"
    LONGSWORD = "Longsword"
    GREATAXE = "Greataxe"
    GREATSWORD = "Greatsword"
    SHADOW_BLADE = "Shadow Blade"
