<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">Expected Damage Calculator</span>
    </v-card-title>
    <v-card-title>Required fields</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="1" sm="1">
          <v-select
            v-model="character.level"
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
            v-model="character.class"
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
            v-model="character.subclass"
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
            v-model="character.fightingStyle"
            :rules="requiredField"
            :items="fightingStyleList"
            required
            attach
            label="Style"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="2" sm="2">
          <v-switch v-model="character.advantage" class="ma-2" label="Advantage"></v-switch>
        </v-col>
        <v-col cols="2" sm="2">
          <v-switch v-model="character.magic" class="ma-2" label="+1 Weapon"></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="character.subclass=='Battle Master'">
          <v-switch
            :disabled="character.level<3"
            v-model="character.superiorityDie"
            class="ma-2"
            label="Superiority Dmg"
          ></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="character.subclass=='Eldritch Knight'">
          <v-switch
            :disabled="character.level<7"
            v-model="character.warMagic"
            class="ma-2"
            label="War Magic"
          ></v-switch>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-title>Calculated Fields</v-card-title>
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
    <v-card-title>{{"Expected Damage: " + damage }}</v-card-title>
    <v-card-title
      v-if="character.warMagic"
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
      character: {
        level: 1,
        class: "Fighter",
        subclass: "Battle Master",
        fightingStyle: "Duelling",
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
      attackDamage: 0,
      bonusAttackDamage: 0,
      averageAC: 14,
      attackStat: 3,
      attackBonus: 3,
      averageDamageDie: 6,
      proficiencyBonus: 2,
      numberOfAttacks: 1,
      extraDamage: 0,
      critChance: 0.05,
      displayDice: ""
    };
  },
  computed: {
    superiorityDieDamage() {
      if (
        this.character.subclass == "Battle Master" &&
        this.character.superiorityDie
      ) {
        if (this.character.level > 17) {
          return 6.5;
        } else if (this.character.level > 9) {
          return 5.5;
        } else if (this.character.level > 2) {
          return 4.5;
        }
      }
      this.character.superiorityDie = false;
      return 0;
    },
    warMagicDamage() {
      if (
        this.character.subclass == "Eldritch Knight" &&
        this.character.warMagic
      ) {
        this.numberOfAttacks = 2;
        if (this.character.level > 16) {
          return 13.5;
        } else if (this.character.level > 10) {
          return 9;
        } else if (this.character.level > 4) {
          return 4.5;
        }
      }
      this.character.warMagic = false;
      return 0;
    },
    boomingBladeDamage() {
      return this.damage + this.warMagicDamage + 4.5;
    },
    damage() {
      this.attackBonus = this.character.magic
        ? this.attackStat + 1
        : this.attackStat;
      if (this.character.fightingStyle == this.fightingStyles.archery) {
        this.attackBonus = this.attackBonus + 2;
      }
      var toHit = this.proficiencyBonus + this.attackBonus;
      var baseDamage = this.numberOfAttacks * this.attackDamage;
      if (this.averageAC <= toHit) {
        var chanceToHit = 1;
      } else {
        var chanceToHit = Math.max(1 - (this.averageAC - 1 - toHit) / 20, 0.05);
      }
      chanceToHit = this.character.advantage
        ? 1 - Math.pow(1 - chanceToHit, 2)
        : chanceToHit;
      var critChance = this.character.advantage
        ? 1 - Math.pow(1 - this.critChance, 2)
        : this.critChance;
      var critDamage =
        this.numberOfAttacks * critChance * this.averageDamageDie;
      if (this.superiorityDieDamage > 0) {
        var chanceOfAHit = 1 - Math.pow(1 - chanceToHit, this.numberOfAttacks);
        var chanceOfACrit =
          1 - Math.pow(1 - this.critChance, this.numberOfAttacks);
        var extraDamage =
          chanceOfAHit * this.superiorityDieDamage +
          chanceOfACrit * this.superiorityDieDamage;
      } else if (this.warMagicDamage > 0) {
        var extraDamage =
          chanceToHit * this.warMagicDamage +
          this.critChance * this.warMagicDamage;
      } else {
        var extraDamage = 0;
      }
      return parseFloat(
        (chanceToHit * baseDamage + critDamage + extraDamage).toFixed(1)
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
      this.proficiencyBonus = this.calculateProficiencyBonus();
      this.attackStat = this.calculateAttackStat();
      this.calculateAttackDice();
      this.averageAC = this.calculateAverageAC();
      this.numberOfAttacks = this.calculateNumberOfAttacks();
      this.critChance = this.calculateCritChance();
    },
    calculateProficiencyBonus() {
      return Math.ceil(this.character.level / 4) + 1;
    },
    calculateAttackStat() {
      var baseStat = Math.min(Math.floor(this.character.level / 4) + 3, 5);
      if (this.character.class == "Fighter") {
        return this.character.level > 5 ? 5 : baseStat;
      }
      return baseStat;
    },
    calculateAttackDice() {
      this.extraDamage = 0;
      switch (this.character.fightingStyle) {
        case this.fightingStyles.duelling:
          this.averageDamageDie = 4.5;
          this.extraDamage = 2;
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
          this.displayDice = "d6 + d6";
          break;
        case this.fightingStyles.protection:
          this.averageDamageDie = 4.5;
          this.displayDice = "d8";
          break;
      }
      this.attackDamage = this.character.magic
        ? this.averageDamageDie + this.extraDamage + this.attackStat + 1
        : this.averageDamageDie + this.extraDamage + this.attackStat;
    },
    calculateAverageAC() {
      return Math.ceil(this.character.level / 3) + 13;
    },
    calculateNumberOfAttacks() {
      var bonusAttacks =
        this.character.fightingStyle == this.fightingStyles.twoWeapon ? 1 : 0;
      switch (this.character.class) {
        case "Fighter":
          if (this.character.level == 20) {
            return 4 + bonusAttacks;
          } else if (this.character.level > 10) {
            return 3 + bonusAttacks;
          }
          break;
      }
      if (this.character.level > 4) {
        return 2 + bonusAttacks;
      }
      return 1 + bonusAttacks;
    },
    calculateCritChance() {
      if (this.character.subclass == "Champion") {
        if (this.character.level > 14) {
          return 0.15;
        } else if (this.character.level > 2) {
          return 0.1;
        }
      }
      return 0.05;
    }
  },
  watch: {
    character: {
      deep: true,
      handler() {
        this.calculateFields();
      }
    }
  }
};
</script>
