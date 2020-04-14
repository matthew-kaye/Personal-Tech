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
            :items="getNumberArray(1,4)"
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
      duelling: "Duelling",
      twoHanded: "Two-Handed",
      twoWeapon: "Two-Weapon",
      archery: "Archery",
      protection: "Protection"
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
        colossusSlayer: false
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
      displayDice: ""
    };
  },
  computed: {
    totalDamage() {
      console.log(this.numberOfAttacks);
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
      return this.bonuses.magic
        ? this.averageDamageDie + extraDamage + this.attackStat + 1
        : this.averageDamageDie + extraDamage + this.attackStat;
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
      if (this.averageAC <= toHit) {
        var chanceToHit = 1;
      } else {
        var chanceToHit = Math.max(1 - (this.averageAC - 1 - toHit) / 20, 0.05);
      }
      return this.bonuses.advantage
        ? 1 - Math.pow(1 - chanceToHit, 2)
        : chanceToHit;
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
      this.abilities.huntersMark =
        this.characterLevel > 1 ? this.abilities.huntersMark : false;
      this.abilities.colossusSlayer =
        this.characterLevel > 2 ? this.abilities.colossusSlayer : false;
      if (this.characterClass == this.classes.ranger) {
        var huntersMarkDamage = this.abilities.huntersMark
          ? 3.5 * this.numberOfAttacks * damageChance
          : 0;
        var colossusSlayerDamage = this.abilities.colossusSlayer
          ? 4.5 * (chanceOfAHit + chanceOfACrit)
          : 0;
        return huntersMarkDamage + colossusSlayerDamage;
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
        this.numberOfAttacks = 2;
        if (this.characterLevel > 16) {
          return 13.5;
        } else if (this.characterLevel > 10) {
          return 9;
        } else if (this.characterLevel > 4) {
          return 4.5;
        }
      }
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
          this.averageDamageDie = 4.5;
          this.displayDice = "d8 + 2";
          break;
        case this.fightingStyles.twoHanded:
          this.averageDamageDie = 4.5 + 3.5;
          this.displayDice = "2d6";
          break;
        case this.fightingStyles.archery:
          this.averageDamageDie = 4.5;
          this.displayDice = "d8";
          break;
        case this.fightingStyles.twoWeapon:
          this.averageDamageDie = 3.5;
          this.displayDice = "d6";
          break;
        case this.fightingStyles.protection:
          this.averageDamageDie = 4.5;
          this.displayDice = "d8";
          break;
      }
    },
    calculateAverageAC() {
      this.averageAC = Math.ceil(this.characterLevel / 3) + 13;
    },
    calculateNumberOfAttacks() {
      switch (this.characterClass) {
        case "Fighter":
          if (this.characterLevel == 20) {
            this.numberOfAttacks = 4;
          } else if (this.characterLevel > 10) {
            this.numberOfAttacks = 3;
          } else if (this.characterLevel > 4) {
            this.numberOfAttacks = 2;
          } else {
            this.numberOfAttacks = 1;
          }
          break;
        case "Ranger":
          if (this.characterLevel > 4) {
            this.numberOfAttacks = 2;
          } else {
            this.numberOfAttacks = 1;
          }
      }
      this.numberOfAttacks =
        this.fightingStyle == this.fightingStyles.twoWeapon
          ? this.numberOfAttacks + 1
          : this.numberOfAttacks;
    }
  },
  watch: {
    characterLevel: {
      deep: true,
      handler() {
        this.calculateFields();
      }
    },
    characterClass: {
      deep: true,
      handler() {
        this.calculateAttackStat();
        this.calculateNumberOfAttacks();
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
        if (this.abilities.warMagic) {
          this.numberOfAttacks = 2;
        } else {
          this.calculateNumberOfAttacks();
        }
      }
    }
  }
};
</script>
