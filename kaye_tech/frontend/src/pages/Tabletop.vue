<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">Expected Damage Calculator</span>
    </v-card-title>
    <v-card-title>Character Options</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="1" sm="1">
          <v-select
            v-model="characterLevel"
            :rules="requiredField"
            :items="getNumberArray(1, 20)"
            required
            attach
            label="Character Level"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="2" sm="2">
          <v-select
            v-model="characterClass"
            :rules="requiredField"
            :items="classList"
            required
            attach
            label="Class"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="2" sm="2">
          <v-select
            v-model="subclass"
            :rules="requiredField"
            :items="subclasses[characterClass]"
            required
            attach
            label="Sublass"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="2" sm="2">
          <v-select
            v-model="fightingStyle"
            :rules="requiredField"
            :items="fightingStyleList"
            required
            attach
            label="Style"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="2" sm="2" v-if="subclass=='Battle Master'">
          <v-switch
            :disabled="characterLevel<3"
            v-model="bonuses.superiorityDie"
            class="ma-2"
            label="Superiority Dmg"
          ></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="subclass=='Eldritch Knight'">
          <v-switch
            :disabled="characterLevel<7"
            v-model="abilities.warMagic"
            class="ma-2"
            label="War Magic"
          ></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="characterClass==classes.ranger">
          <v-switch
            :disabled="characterLevel==1"
            v-model="abilities.huntersMark"
            class="ma-2"
            label="Hunter's Mark"
          ></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="subclass=='Hunter'">
          <v-switch
            :disabled="characterLevel<3"
            v-model="abilities.colossusSlayer"
            class="ma-2"
            label="Colossus Slayer"
          ></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="subclass=='Beast Master'">
          <v-switch
            :disabled="characterLevel<3"
            v-model="abilities.wolfAttack"
            class="ma-2"
            label="Wolf"
          ></v-switch>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-title>Stats</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="1" sm="1">
          <v-select
            v-model="proficiencyBonus"
            :items="getNumberArray(2, 6)"
            attach
            label="Proficiency"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="1" sm="1">
          <v-select
            v-model="attackStat"
            :items="getNumberArray(1, 5)"
            attach
            label="Attack Stat"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="1" sm="1">
          <v-text-field v-model="displayDice" label="Attack Dice" required></v-text-field>
        </v-col>
        <v-col cols="1" sm="1">
          <v-text-field v-model="averageAC" label="Enemy AC" required></v-text-field>
        </v-col>
        <v-col cols="1" sm="1">
          <v-select
            v-model="numberOfAttacks"
            :items="getNumberArray(1,5)"
            attach
            label="Attacks"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="2" sm="2">
          <v-switch v-model="bonuses.advantage" class="ma-2" label="Advantage"></v-switch>
        </v-col>
        <v-col cols="2" sm="2">
          <v-switch v-model="bonuses.magic" class="ma-2" label="+1 Weapon"></v-switch>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-title>{{"Expected Damage: " + totalDamage }}</v-card-title>
    <v-card-title
      v-if="abilities.warMagic"
    >{{"Expected Damage (Enemy Moves): " + boomingBladeDamage }}</v-card-title>
  </v-card>
</template>

<script>
export default {
  components: {},
  mounted() {},
  created() {
    this.calculateFields();
    this.classes = {
      fighter: "Fighter",
      ranger: "Ranger"
    };
    for (var value in this.classes) {
      this.classList.push(this.classes[value]);
    }
    this.subclasses[this.classes.fighter] = [
      "Battle Master",
      "Champion",
      "Eldritch Knight"
    ];
    this.subclasses[this.classes.ranger] = ["Beast Master", "Hunter"];
    this.fightingStyles = {
      archery: "Archery",
      defence: "Defence (Greatsword)",
      duelling: "Duelling",
      twoHanded: "Two-Handed",
      twoWeapon: "Two-Weapon",
      protection: "Protection"
    };
    this.weapons = {
      longbow: 4.5,
      longsword: 4.5,
      greatsword: 7,
      greataxe: 6.5,
      heavyCrossbow: 5.5,
      handaxe: 3.5
    };
    for (var value in this.fightingStyles) {
      this.fightingStyleList.push(this.fightingStyles[value]);
    }
    this.calculateFields();
  },
  data() {
    return {
      characterLevel: 1,
      characterClass: "Fighter",
      subclass: "Battle Master",
      fightingStyle: "Duelling",
      bonuses: {
        advantage: false,
        superiorityDie: false,
        magic: false
      },
      abilities: {
        warMagic: false,
        huntersMark: false,
        colossusSlayer: false,
        wolfAttack: false
      },
      requiredField: [v => !!v],
      classes: {},
      classList: [],
      subclasses: {},
      fightingStyles: {},
      fightingStyleList: [],
      bonusAttackDamage: 0,
      averageAC: 14,
      attackStat: 3,
      averageDamageDie: 6,
      proficiencyBonus: 2,
      numberOfAttacks: 1,
      displayDice: "",
      weapons: [],
      wolf: {
        bonusToHit: 4,
        averageDamageDie: 5,
        damagePerHit: 7
      }
    };
  },
  computed: {
    totalDamage() {
      var baseDamage =
        this.numberOfAttacks * this.attackDamage * this.chanceToHit;
      var critDamage =
        this.numberOfAttacks * this.chanceToCrit * this.averageDamageDie;
      return parseFloat(
        (baseDamage + critDamage + this.abilityDamage).toFixed(1)
      );
    },
    attackDamage() {
      var extraDamage =
        this.fightingStyle == this.fightingStyles.duelling ? 2 : 0;
      var attackDamage = this.bonuses.magic
        ? this.averageDamageDie + extraDamage + this.attackStat + 1
        : this.averageDamageDie + extraDamage + this.attackStat;
      return this.abilities.wolfAttack
        ? 7 + this.proficiencyBonus
        : attackDamage;
    },
    attackBonus() {
      var attackBonus = this.bonuses.magic
        ? this.attackStat + 1
        : this.attackStat;
      if (this.fightingStyle == this.fightingStyles.archery) {
        attackBonus = attackBonus + 2;
      }
      return attackBonus;
    },
    chanceToHit() {
      var toHit = this.proficiencyBonus + this.attackBonus;
      return this.getChanceToHitFromBonusToHit(toHit);
    },
    chanceToCrit() {
      var critChance = 0.05;
      if (this.subclass == "Champion") {
        if (this.characterLevel > 14) {
          critChance = 0.15;
        } else if (this.characterLevel > 2) {
          critChance = 0.1;
        }
      }
      return this.bonuses.advantage
        ? 1 - Math.pow(1 - critChance, 2)
        : critChance;
    },
    abilityDamage() {
      var chanceOfAHit =
        1 - Math.pow(1 - this.chanceToHit, this.numberOfAttacks);
      var chanceOfACrit =
        1 - Math.pow(1 - this.chanceToCrit, this.numberOfAttacks);
      var damageChance = this.chanceToHit + this.chanceToCrit;
      if (this.superiorityDieDamage > 0) {
        return (chanceOfAHit + chanceOfACrit) * this.superiorityDieDamage;
      } else if (this.warMagicDamage > 0) {
        return damageChance * this.warMagicDamage;
      }
      this.bonuses.superiorityDie = false;
      this.abilities.warMagic = false;
      if (this.characterClass == this.classes.ranger) {
        var huntersMarkDamage = this.abilities.huntersMark
          ? 3.5 * this.numberOfAttacks * damageChance
          : 0;
        var colossusSlayerDamage = this.abilities.colossusSlayer
          ? 4.5 * (chanceOfAHit + chanceOfACrit)
          : 0;
        return huntersMarkDamage + colossusSlayerDamage + this.wolfDamage;
      }
      return 0;
    },
    superiorityDieDamage() {
      if (this.subclass == "Battle Master" && this.bonuses.superiorityDie) {
        if (this.characterLevel > 17) {
          return 6.5;
        } else if (this.characterLevel > 9) {
          return 5.5;
        } else if (this.characterLevel > 2) {
          return 4.5;
        }
      }
      return 0;
    },
    warMagicDamage() {
      if (this.subclass == "Eldritch Knight" && this.abilities.warMagic) {
        if (this.characterLevel > 16) {
          return 13.5;
        } else if (this.characterLevel > 10) {
          return 9;
        } else if (this.characterLevel > 6) {
          return 4.5;
        }
      }
      return 0;
    },
    wolfDamage() {
      if (this.abilities.wolfAttack) {
        var companionBonusToHit = this.wolf.bonusToHit + this.proficiencyBonus;
        var wolfBiteDamage = this.wolf.damagePerHit + this.proficiencyBonus;
        var wolfChanceToHit = this.getChanceToHitFromBonusToHit(
          companionBonusToHit
        );
        return (
          this.wolfAttacks *
          (wolfChanceToHit * wolfBiteDamage +
            this.chanceToCrit * this.wolf.averageDamageDie)
        );
      }
      return 0;
    },
    wolfAttacks() {
      if (this.subclass == "Beast Master" && this.abilities.wolfAttack) {
        if (this.characterLevel > 10) {
          return 2;
        } else if (this.characterLevel > 2) {
          return 1;
        }
      }
      this.abilities.wolfAttack = false;
      return 0;
    },
    boomingBladeDamage() {
      var moveDamage = this.warMagicDamage + 4.5;
      return parseFloat(
        (this.totalDamage + this.chanceToHit * moveDamage).toFixed(1)
      );
    }
  },
  methods: {
    getNumberArray(start, end) {
      var levels = Array.from(Array(end + 1).keys());
      for (var x = 0; x < start; x++) {
        levels.shift();
      }
      return levels;
    },
    calculateFields() {
      this.calculateProficiencyBonus();
      this.calculateAttackStat();
      this.calculateAttackDice();
      this.calculateAverageAC();
      this.calculateNumberOfAttacks();
    },
    calculateProficiencyBonus() {
      this.proficiencyBonus = Math.ceil(this.characterLevel / 4) + 1;
    },
    calculateAttackStat() {
      var baseStat = Math.min(Math.floor(this.characterLevel / 4) + 3, 5);
      if (this.characterClass == this.classes.fighter) {
        this.attackStat = this.characterLevel > 5 ? 5 : baseStat;
      } else {
        this.attackStat = baseStat;
      }
    },
    calculateAttackDice() {
      switch (this.fightingStyle) {
        case this.fightingStyles.duelling:
          this.averageDamageDie = this.weapons.longsword;
          this.displayDice = "d8 + 2";
          break;
        case this.fightingStyles.twoHanded:
          this.averageDamageDie = this.weapons.greatsword + 4 / 3;
          this.displayDice = "2d6";
          break;
        case this.fightingStyles.archery:
          this.averageDamageDie = this.weapons.longbow;
          this.displayDice = "d8";
          break;
        case this.fightingStyles.twoWeapon:
          this.averageDamageDie = this.weapons.handaxe;
          this.displayDice = "d6";
          break;
        case this.fightingStyles.protection:
          this.averageDamageDie = this.weapons.longsword;
          this.displayDice = "d8";
          break;
        case this.fightingStyles.defence:
          this.averageDamageDie = this.weapons.greatsword;
          this.displayDice = "2d6";
      }
    },
    calculateAverageAC() {
      this.averageAC = Math.ceil(this.characterLevel / 3) + 13;
    },
    calculateNumberOfAttacks() {
      switch (this.characterClass) {
        case "Fighter":
          if (this.characterLevel == 20) {
            this.numberOfAttacks = this.abilities.warMagic ? 2 : 4;
          } else if (this.characterLevel > 10) {
            this.numberOfAttacks = this.abilities.warMagic ? 2 : 3;
          } else if (this.characterLevel > 4) {
            this.numberOfAttacks = 2;
          } else {
            this.numberOfAttacks = 1;
          }
          break;
        case "Ranger":
          if (this.characterLevel > 4) {
            this.numberOfAttacks = this.abilities.wolfAttack ? 1 : 2;
          } else {
            this.numberOfAttacks = 1;
          }
      }
      this.numberOfAttacks =
        this.fightingStyle == this.fightingStyles.twoWeapon
          ? this.numberOfAttacks + 1
          : this.numberOfAttacks;
    },
    disableImpossibleAbilities() {
      this.abilities.huntersMark =
        this.characterLevel > 1 ? this.abilities.huntersMark : false;
      this.abilities.colossusSlayer =
        this.characterLevel > 2 && this.subclass == "Hunter"
          ? this.abilities.colossusSlayer
          : false;
      this.abilities.wolfAttack =
        this.characterLevel > 2 && this.subclass == "Beast Master"
          ? this.abilities.wolfAttack
          : false;
    },
    getChanceToHitFromBonusToHit(bonusToHit) {
      var chanceToHit = Math.max(
        1 - (this.averageAC - 1 - bonusToHit) / 20,
        0.05
      );
      chanceToHit = Math.min(chanceToHit, 0.95);
      return this.bonuses.advantage
        ? 1 - Math.pow(1 - chanceToHit, 2)
        : chanceToHit;
    }
  },
  watch: {
    characterLevel: {
      deep: true,
      handler() {
        this.calculateFields();
        this.disableImpossibleAbilities();
      }
    },
    characterClass: {
      deep: true,
      handler() {
        this.calculateAttackStat();
        this.calculateNumberOfAttacks();
        this.disableImpossibleAbilities();
        this.subclass = this.subclasses[this.characterClass][0];
      }
    },
    fightingStyle: {
      deep: true,
      handler() {
        this.calculateAttackDice();
        this.calculateNumberOfAttacks();
      }
    },
    abilities: {
      deep: true,
      handler() {
        this.calculateNumberOfAttacks();
      }
    }
  }
};
</script>
