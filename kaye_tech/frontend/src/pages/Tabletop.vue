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
        <v-col
          cols="2"
          sm="2"
          v-if="subclass=='Eldritch Knight' && fightingStyle!=fightingStyles.archery"
        >
          <v-switch
            :disabled="characterLevel<7"
            v-model="abilities.shadowBlade"
            class="ma-2"
            label="Shadow Blade"
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
        <v-col cols="1" sm="1" v-if="subclass=='Beast Master'">
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
        <v-col cols="2" sm="2" v-if="fightingStyle==fightingStyles.archery">
          <v-switch v-model="abilities.sharpshooter" class="ma-2" label="Sharpshooter"></v-switch>
        </v-col>
        <v-col
          cols="2"
          sm="2"
          v-if="fightingStyle==fightingStyles.twoHanded || fightingStyle==fightingStyles.defence"
        >
          <v-switch v-model="abilities.greatWeaponMaster" class="ma-2" label="GW Master"></v-switch>
        </v-col>
        <v-col cols="2" sm="2" v-if="fightingStyle==fightingStyles.twoWeapon">
          <v-switch v-model="abilities.dualWielder" class="ma-2" label="Dual Wielder"></v-switch>
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
      longbow: { damage: 4.5, dice: "d8" },
      longsword: { damage: 4.5, dice: "d8" },
      greatsword: { damage: 7, dice: "2d6" },
      greataxe: { damage: 6.5, dice: "d12" },
      heavyCrossbow: { damage: 5.5, dice: "d10" },
      handaxe: { damage: 3.5, dice: "d6" },
      shadowBlade: { damage: 9, dice: "2d8" }
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
        wolfAttack: false,
        sharpshooter: false,
        greatWeaponMaster: false,
        dualWielder: false,
        shadowBlade: false
      },
      requiredField: [v => !!v],
      classes: {},
      classList: [],
      subclasses: {},
      fightingStyles: {},
      fightingStyleList: [],
      averageAC: 14,
      attackStat: 3,
      proficiencyBonus: 2,
      numberOfAttacks: 1,
      weapons: [],
      weapon: {},
      bonusWeapon: {},
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
      var extraDamage = this.abilityDamage + this.bonusAttackDamage;
      return parseFloat(baseDamage + critDamage + extraDamage).toFixed(1);
    },
    attackDamage() {
      var extraDamage =
        this.fightingStyle == this.fightingStyles.duelling ? 2 : 0;
      var magicBonus =
        !this.abilities.shadowBlade && this.bonuses.magic ? 1 : 0;
      var attackDamage =
        this.averageDamageDie + extraDamage + this.attackStat + magicBonus;
      var attackDamage =
        this.abilities.sharpshooter || this.abilities.greatWeaponMaster
          ? attackDamage + 10
          : attackDamage;
      return attackDamage;
    },
    bonusAttackDamage() {
      var magicBonus = this.bonuses.magic ? 1 : 0;
      var toHit = this.proficiencyBonus + this.attackBonus + magicBonus;
      var chanceToHit = this.getChanceToHitFromBonusToHit(toHit);
      return this.fightingStyle == this.fightingStyles.twoWeapon
        ? (this.bonusWeapon.damage + this.attackStat + magicBonus) *
            chanceToHit +
            this.chanceToCrit * this.bonusWeapon.damage
        : 0;
    },
    attackBonus() {
      var magicBonus =
        !this.abilities.shadowBlade && this.bonuses.magic ? 1 : 0;
      var attackBonus = this.attackStat + magicBonus;
      if (this.fightingStyle == this.fightingStyles.archery) {
        attackBonus = this.abilities.sharpshooter
          ? attackBonus - 3
          : attackBonus + 2;
      }
      return this.abilities.greatWeaponMaster ? attackBonus - 5 : attackBonus;
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
    displayDice() {
      if (this.fightingStyle == this.fightingStyles.duelling) {
        return "d8 + 2";
      } else {
        return this.weapon.dice;
      }
    },
    averageDamageDie() {
      if (
        this.fightingStyle == this.fightingStyles.twoHanded &&
        this.weapon == this.weapons.greatsword
      ) {
        return this.weapon.damage + 4 / 3;
      } else {
        return this.weapon.damage;
      }
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
      this.chooseWeaponFromStyle();
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
    chooseWeaponFromStyle() {
      switch (this.fightingStyle) {
        case this.fightingStyles.duelling:
          this.weapon = this.weapons.longsword;
          break;
        case this.fightingStyles.twoHanded:
          this.weapon = this.weapons.greatsword;
          break;
        case this.fightingStyles.archery:
          this.weapon = this.weapons.longbow;
          break;
        case this.fightingStyles.twoWeapon:
          this.weapon = this.abilities.dualWielder
            ? this.weapons.longsword
            : this.weapons.handaxe;
          this.bonusWeapon = this.weapon;
          break;
        case this.fightingStyles.protection:
          this.weapon = this.weapons.longsword;
          break;
        case this.fightingStyles.defence:
          this.weapon = this.weapons.greatsword;
      }
      this.weapon = this.abilities.shadowBlade
        ? this.weapons.shadowBlade
        : this.weapon;
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
      this.abilities.sharpshooter =
        this.fightingStyle == this.fightingStyles.archery
          ? this.abilities.sharpshooter
          : false;
      this.abilities.greatWeaponMaster =
        this.fightingStyle == this.fightingStyles.twoWeapon
          ? this.abilities.greatWeaponMaster
          : false;
      this.abilities.dualWielder =
        this.fightingStyle == this.fightingStyles.twoWeapon
          ? this.abilities.dualWielder
          : false;
      this.abilities.shadowBlade =
        this.subclass == "Eldritch Knight" &&
        this.characterLevel > 6 &&
        this.fightingStyle != this.fightingStyles.archery
          ? this.abilities.shadowBlade
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
        this.chooseWeaponFromStyle();
        this.calculateNumberOfAttacks();
        this.disableImpossibleAbilities();
      }
    },
    abilities: {
      deep: true,
      handler() {
        this.disableImpossibleAbilities();
        this.calculateNumberOfAttacks();
        this.chooseWeaponFromStyle();
      }
    }
  }
};
</script>
