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
            v-model="characterLevel"
            :rules="requiredField"
            :items="getLevels()"
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
            :items="classes"
            required
            attach
            label="Class"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="2" sm="2">
          <v-select
            v-model="fightingStyle"
            :rules="requiredField"
            :items="fightingStyles"
            required
            attach
            label="Style"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="1" sm="1">
          <v-switch v-model="advantage" class="ma-2" label="Advantage"></v-switch>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-title>Calculated Fields (not over-writeable)</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="1" sm="1">
          <v-text-field v-model="proficiencyBonus" label="Proficiency" required></v-text-field>
        </v-col>
        <v-col cols="2" sm="2">
          <v-text-field v-model="attackStat" label="Attack Stat" required></v-text-field>
        </v-col>
        <v-col cols="2" sm="2">
          <v-text-field v-model="attackDice" label="Attack Dice (base)" required></v-text-field>
        </v-col>
        <v-col cols="1" sm="1">
          <v-text-field v-model="averageAC" label="Est. AC" required></v-text-field>
        </v-col>
        <v-col cols="1" sm="1">
          <v-text-field v-model="numberOfAttacks" label="Attacks" required></v-text-field>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-title>{{"Expected Damage: " + damage }}</v-card-title>
  </v-card>
</template>

<script>
export default {
  components: {},
  created() {},
  data() {
    return {
      characterLevel: 1,
      requiredField: [v => !!v],
      characterClass: "",
      classes: ["Fighter"],
      fightingStyles: ["Duelling", "Two-Handed", "Two-Weapon", "Archery"],
      fightingStyle: "",
      advantage: false,
      ACOverride: false,
      attackDamage: 0,
      bonusAttackDamage: 0
    };
  },
  computed: {
    proficiencyBonus: {
      get() {
        return Math.ceil(this.characterLevel / 4) + 1;
      },
      set(value) {
        return parseInt(value);
      }
    },
    attackStat: {
      get() {
        var baseStat = Math.min(Math.floor(this.characterLevel / 4) + 3, 5);
        if (this.characterClass == "Fighter") {
          baseStat = this.characterLevel > 5 ? 5 : baseStat;
        }
        return this.fightingStyle == "Archery" ? baseStat + 2 : baseStat;
      },
      set(value) {
        return parseInt(value);
      }
    },
    attackDice: {
      get() {
        switch (this.fightingStyle) {
          case "Duelling":
            this.attackDamage = 6.5 + this.attackStat;
            return "d8 + 2";
          case "Two-Handed":
            this.attackDamage = 3.5 + this.attackStat;
            this.bonusAttackDamage = this.attackDamage;
            return "d6 + d6";
          case "Archery":
            this.attackDamage = 4.5 + this.attackStat;
            return "d8";
          case "Two-Weapon":
            this.attackDamage = 7 + this.attackStat;
            return "2d6";
        }
      },
      set(value) {
        return value;
      }
    },
    averageAC: {
      get() {
        if (!this.ACOverride) {
          return Math.ceil(this.characterLevel / 3) + 13;
        }
      },
      set(value) {
        return value;
      }
    },
    numberOfAttacks: {
      get() {
        if (this.characterLevel == 20) {
          return 4;
        } else if (this.characterLevel > 10) {
          return 3;
        } else if (this.characterLevel > 4) {
          return 2;
        }
        return 1;
      },
      set(value) {
        return parseInt(value);
      }
    },
    damage() {
      var toHit = this.proficiencyBonus + this.attackStat;
      var averageDamage =
        this.numberOfAttacks * this.attackDamage + this.bonusAttackDamage;
      var chanceToHit = 1 - (this.averageAC - 1 - toHit) / 20;
      chanceToHit = this.advantage
        ? 1 - Math.pow(1 - chanceToHit, 2)
        : chanceToHit;
      return (chanceToHit * averageDamage).toFixed(1);
    }
  },
  methods: {
    getLevels() {
      var levels = Array.from(Array(21).keys());
      levels.shift();
      return levels;
    },
    getProficiencyFromLevel(level) {
      return Math.ceil(level / 4) + 1;
    }
  }
};
</script>
