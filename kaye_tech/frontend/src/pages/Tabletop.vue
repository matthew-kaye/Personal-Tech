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
        <v-col cols="1" sm="1">
          <v-select
            v-model="characterClass"
            :rules="requiredField"
            :items="classes"
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
            :items="subclasses"
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
        <v-col cols="2" sm="2">
          <v-switch v-model="bonuses.advantage" class="ma-2" label="Advantage"></v-switch>
        </v-col>
        <v-col cols="2" sm="2">
          <v-switch v-model="bonuses.magic" class="ma-2" label="+1 Weapon"></v-switch>
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
            v-model="bonuses.warMagic"
            class="ma-2"
            label="War Magic"
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
      </v-row>
    </v-card-text>
    <v-card-title>{{"Expected Damage: " + totalDamage }}</v-card-title>
    <v-card-title
      v-if="bonuses.warMagic"
    >{{"Expected Damage (Enemy Moves): " + boomingBladeDamage }}</v-card-title>
  </v-card>
</template>

<script>
export default {
  components: {},
  mounted() {},
  created() {
    this.calculateFields();
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
        magic: false,
        warMagic: false
      },
      requiredField: [v => !!v],
      classes: ["Fighter"],
      subclasses: ["Battle Master", "Champion", "Eldritch Knight"],
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
      var baseDamage =
        this.numberOfAttacks * this.attackDamage * this.chanceToHit;
      var critDamage =
        this.numberOfAttacks * this.chanceToCrit * this.averageDamageDie;
      return parseFloat(
        (baseDamage + critDamage + this.abiltyDamage).toFixed(1)
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
    abiltyDamage() {
      if (this.superiorityDieDamage > 0) {
        var chanceOfAHit =
          1 - Math.pow(1 - this.chanceToHit, this.numberOfAttacks);
        var chanceOfACrit =
          1 - Math.pow(1 - this.chanceToCrit, this.numberOfAttacks);
        return (
          chanceOfAHit * this.superiorityDieDamage +
          chanceOfACrit * this.superiorityDieDamage
        );
      } else if (this.warMagicDamage > 0) {
        return (
          this.chanceToHit * this.warMagicDamage +
          this.chanceToCrit * this.warMagicDamage
        );
      } else {
        return 0;
      }
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
      this.bonuses.superiorityDie = false;
      return 0;
    },
    warMagicDamage() {
      if (this.subclass == "Eldritch Knight" && this.bonuses.warMagic) {
        this.numberOfAttacks = 2;
        if (this.characterLevel > 16) {
          return 13.5;
        } else if (this.characterLevel > 10) {
          return 9;
        } else if (this.characterLevel > 4) {
          return 4.5;
        }
      }
      this.bonuses.warMagic = false;
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
      if (this.characterClass == "Fighter") {
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
      }
    },
    fightingStyle: {
      deep: true,
      handler() {
        this.calculateAttackDice();
        this.calculateNumberOfAttacks();
      }
    }
  }
};
</script>
