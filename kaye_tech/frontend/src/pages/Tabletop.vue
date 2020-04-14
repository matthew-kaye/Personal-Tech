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
          <v-switch v-model="bonuses.advantage" class="ma-2" label="Advantage"></v-switch>
        </v-col>
        <v-col cols="2" sm="2">
          <v-switch v-model="bonuses.magic" class="ma-2" label="+1 Weapon"></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="character.subclass=='Battle Master'">
          <v-switch
            :disabled="character.level<3"
            v-model="bonuses.superiorityDie"
            class="ma-2"
            label="Superiority Dmg"
          ></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="character.subclass=='Eldritch Knight'">
          <v-switch
            :disabled="character.level<7"
            v-model="bonuses.warMagic"
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
      character: {
        level: 1,
        class: "Fighter",
        subclass: "Battle Master",
        fightingStyle: "Duelling"
      },
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
      attackDamage: 0,
      bonusAttackDamage: 0,
      averageAC: 14,
      attackStat: 3,
      averageDamageDie: 6,
      proficiencyBonus: 2,
      numberOfAttacks: 1,
      extraDamage: 0,
      critChance: 0.05,
      displayDice: ""
    };
  },
  computed: {
    damage() {
      var baseDamage =
        this.numberOfAttacks * this.attackDamage * this.chanceToHit;
      var critDamage =
        this.numberOfAttacks * this.chanceToCrit * this.averageDamageDie;
      var extraDamage = this.calculateExtraDamage();
      return parseFloat((baseDamage + critDamage + extraDamage).toFixed(1));
    },
    attackBonus() {
      var attackBonus = this.bonuses.magic
        ? this.attackStat + 1
        : this.attackStat;
      if (this.character.fightingStyle == this.fightingStyles.archery) {
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
      if (this.character.subclass == "Champion") {
        if (this.character.level > 14) {
          var baseChance = 0.15;
        } else if (this.character.level > 2) {
          var baseChance = 0.1;
        }
      } else {
        var baseChance = 0.05;
      }
      return this.bonuses.advantage
        ? 1 - Math.pow(1 - baseChance, 2)
        : baseChance;
    },
    superiorityDieDamage() {
      if (
        this.character.subclass == "Battle Master" &&
        this.bonuses.superiorityDie
      ) {
        if (this.character.level > 17) {
          return 6.5;
        } else if (this.character.level > 9) {
          return 5.5;
        } else if (this.character.level > 2) {
          return 4.5;
        }
      }
      this.bonuses.superiorityDie = false;
      return 0;
    },
    warMagicDamage() {
      if (
        this.character.subclass == "Eldritch Knight" &&
        this.bonuses.warMagic
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
      this.bonuses.warMagic = false;
      return 0;
    },
    boomingBladeDamage() {
      var moveDamage = this.warMagicDamage + 4.5;
      return parseFloat(
        (this.damage + this.chanceToHit * moveDamage).toFixed(1)
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
      this.proficiencyBonus = Math.ceil(this.character.level / 4) + 1;
    },
    calculateAttackStat() {
      var baseStat = Math.min(Math.floor(this.character.level / 4) + 3, 5);
      if (this.character.class == "Fighter") {
        this.attackStat = this.character.level > 5 ? 5 : baseStat;
      } else {
        this.attackStat = baseStat;
      }
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
      this.attackDamage = this.bonuses.magic
        ? this.averageDamageDie + this.extraDamage + this.attackStat + 1
        : this.averageDamageDie + this.extraDamage + this.attackStat;
    },
    calculateAverageAC() {
      this.averageAC = Math.ceil(this.character.level / 3) + 13;
    },
    calculateNumberOfAttacks() {
      var bonusAttacks =
        this.character.fightingStyle == this.fightingStyles.twoWeapon ? 1 : 0;
      switch (this.character.class) {
        case "Fighter":
          if (this.character.level == 20) {
            this.numberOfAttacks = 4 + bonusAttacks;
          } else if (this.character.level > 10) {
            this.numberOfAttacks = 3 + bonusAttacks;
          } else if (this.character.level > 4) {
            this.numberOfAttacks = 2 + bonusAttacks;
          } else {
            this.numberOfAttacks = 1 + bonusAttacks;
          }
          break;
      }
    },
    calculateExtraDamage() {
      if (this.superiorityDieDamage > 0) {
        var chanceOfAHit =
          1 - Math.pow(1 - this.chanceToHit, this.numberOfAttacks);
        var chanceOfACrit =
          1 - Math.pow(1 - this.critChance, this.numberOfAttacks);
        return (
          chanceOfAHit * this.superiorityDieDamage +
          chanceOfACrit * this.superiorityDieDamage
        );
      } else if (this.warMagicDamage > 0) {
        return (
          this.chanceToHit * this.warMagicDamage +
          this.critChance * this.warMagicDamage
        );
      } else {
        return 0;
      }
    }
  },
  watch: {
    character: {
      deep: true,
      handler() {
        this.calculateFields();
      }
    },
    level: {
      deep: true,
      handler() {
        this.calculateFields();
      }
    },
    bonuses: {
      deep: true,
      handler() {
        this.calculateFields();
      }
    }
  }
};
</script>
