from .classes import Fighter, Ranger, Wolf
import math


class Subclasses:
    BATTLE_MASTER = "Battle Master"
    BEAST_MASTER = "Beast Master"
    CHAMPION = "Champion"
    ELDRITCH_KNIGHT = "Eldritch Knight"
    HUNTER = "Hunter"


class Champion(Fighter):
    def critical_chance(self):
        if self.level >= 15:
            return 0.15
        elif self.level >= 3:
            return 0.1
        return 0.05


class EldritchKnight(Fighter):
    def caster_level(self):
        caster_level = math.ceil(self.level / 3) if self.level >= 3 else 0
        multiclass_level = math.floor(self.level / 3) + self.caster_multiclasses
        return max(caster_level, multiclass_level)

    def booming_blade_damage(self):
        character_level = self.level + self.caster_multiclasses
        if character_level >= 17:
            return 13.5
        elif character_level >= 11:
            return 9
        elif character_level >= 7:
            return 4.5
        return 0


class BattleMaster(Fighter):
    def damage_on_a_hit(self):
        if not self.superiority_bonus or self.level < 3:
            return 0
        if self.level >= 18:
            return 6.5
        elif self.level >= 10:
            return 5.5
        elif self.level >= 3:
            return 4.5


class BeastMaster(Ranger):
    def other_damage(self):
        if self.wolf_attack:
            companion = Wolf(self.level, self.enemy_armour, self.advantage)
            return companion.damage_output()
        return 0


class Hunter(Ranger):
    def damage_on_a_hit(self):
        return 4.5 if self.colossus_slayer else 0
