<template>
  <v-card>
    <v-card-title class="mb-2">Character Options</v-card-title>
    <v-row class="mx-0">
      <v-col cols="6" md="1">
        <v-select
          outlined
          v-model="characterLevel"
          :rules="requiredField"
          :items="getNumberArray(1, 20)"
          required
          attach
          label="Level"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="6" md="2">
        <v-select
          outlined
          v-model="characterClass"
          :rules="requiredField"
          :items="classList"
          required
          attach
          label="Class"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="12" md="2">
        <v-select
          outlined
          v-model="subclass"
          :rules="requiredField"
          :items="subclasses[characterClass]"
          required
          attach
          label="Sublass"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="12" md="2">
        <v-select
          outlined
          v-model="fightingStyle"
          :rules="requiredField"
          :items="fightingStyleList"
          required
          attach
          label="Style"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
    </v-row>
    <v-card-title>Stats</v-card-title>
    <v-row class="mx-2">
      <v-col cols="6" md="1">
        <v-select
          outlined
          v-model="proficiencyBonus"
          :items="getNumberArray(2, 6)"
          attach
          label="Proficiency"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="6" md="1">
        <v-select
          outlined
          v-model="attackStat"
          :items="getNumberArray(1, 5)"
          attach
          label="Attack Stat"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="6" md="2">
        <v-select
          outlined
          v-model="weapon"
          :items="weaponList"
          item-text="name"
          attach
          label="Weapons"
          return-object
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="6" md="1">
        <v-text-field outlined v-model="averageAC" label="Enemy AC" required></v-text-field>
      </v-col>
      <v-col cols="6" md="1">
        <v-select
          outlined
          v-model="numberOfAttacks"
          :items="getNumberArray(1,5)"
          attach
          label="Attacks"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col md="auto">
        <v-switch v-model="bonuses.advantage" class="ma-2" label="Advantage"></v-switch>
      </v-col>
      <v-col md="auto">
        <v-switch v-model="bonuses.magic" class="ma-2" label="+1 Weapon"></v-switch>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card-title>Feats/Abilities</v-card-title>
        <v-row class="ml-2">
          <v-col md="auto" v-if="subclass=='Battle Master'">
            <v-switch
              :disabled="characterLevel<3"
              v-model="bonuses.superiorityDie"
              class="ma-2"
              label="Superiority Dmg"
            ></v-switch>
          </v-col>
          <v-col md="auto" v-if="subclass=='Eldritch Knight'">
            <v-switch
              :disabled="characterLevel<7"
              v-model="abilities.warMagic"
              class="ma-2"
              label="War Magic"
            ></v-switch>
          </v-col>
          <v-col
            md="auto"
            v-if="subclass=='Eldritch Knight' && fightingStyle!=fightingStyles.archery"
          >
            <v-switch
              :disabled="characterLevel<7"
              v-model="abilities.shadowBlade"
              class="ma-2"
              label="Shadow Blade"
            ></v-switch>
          </v-col>
          <v-col md="auto" v-if="characterClass==classes.ranger">
            <v-switch
              :disabled="characterLevel==1"
              v-model="abilities.huntersMark"
              class="ma-2"
              label="Hunter's Mark"
            ></v-switch>
          </v-col>
          <v-col md="auto" v-if="subclass=='Hunter'">
            <v-switch
              :disabled="characterLevel<3"
              v-model="abilities.colossusSlayer"
              class="ma-2"
              label="Colossus Slayer"
            ></v-switch>
          </v-col>
          <v-col md="auto" v-if="subclass=='Beast Master'">
            <v-switch
              :disabled="characterLevel<3"
              v-model="abilities.wolfAttack"
              class="ma-2"
              label="Wolf"
            ></v-switch>
          </v-col>
          <v-col md="auto" v-if="fightingStyle==fightingStyles.archery">
            <v-switch v-model="abilities.crossbowExpert" class="ma-2" label="Crossbow Expert"></v-switch>
          </v-col>
          <v-col md="auto" v-if="fightingStyle==fightingStyles.archery">
            <v-switch v-model="abilities.sharpshooter" class="ma-2" label="Sharpshooter"></v-switch>
          </v-col>
          <v-col
            md="auto"
            v-if="fightingStyle==fightingStyles.twoHanded || fightingStyle==fightingStyles.defence"
          >
            <v-switch v-model="abilities.greatWeaponMaster" class="ma-2" label="GW Master"></v-switch>
          </v-col>
          <v-col md="auto" v-if="fightingStyle==fightingStyles.twoWeapon">
            <v-switch v-model="abilities.dualWielder" class="ma-2" label="Dual Wielder"></v-switch>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="11" md="auto" class="ml-4">
        <v-card elevation="10" v-if="!abilities.warMagic">
          <v-card-title class="primary headline">
            <span class="white--text">{{"Damage: " + totalDamage }}</span>
          </v-card-title>
        </v-card>
        <v-card elevation="10" v-if="abilities.warMagic">
          <v-card-title class="primary headline">
            <span class="white--text">{{`Damage (moves): ${totalDamage} (${boomingBladeDamage}) `}}</span>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import CalculatorApi from "@/apis/CalculatorApi";
const calculatorApi = new CalculatorApi();
export default {
  components: {},
  mounted() {},
  created() {
    this.calculateFields();
    this.playerData = this.classes;
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
      defence: "Defence",
      duelling: "Duelling",
      twoHanded: "Two-Handed",
      twoWeapon: "Two-Weapon",
      protection: "Protection"
    };
    for (var value in this.fightingStyles) {
      this.fightingStyleList.push(this.fightingStyles[value]);
    }
    this.weapons = {
      greataxe: { damage: 6.5, name: "Greataxe", heavy: true },
      greatsword: { damage: 7, name: "Greatsword", heavy: true },
      handaxe: {
        damage: 3.5,
        name: "Handaxe",
        ranged: true,
        light: true
      },
      heavyCrossbow: {
        damage: 5.5,
        name: "Heavy Crossbow",
        ranged: true,
        loading: true,
        heavy: true
      },
      longbow: { damage: 4.5, name: "Longbow", ranged: true, heavy: true },
      longsword: { damage: 4.5, name: "Longsword", versatile: true }
    };
    for (var value in this.weapons) {
      this.weaponList.push(this.weapons[value]);
    }
    this.weapons.shadowBlade = { damage: 9, name: "Shadow Blade", light: true };
    this.calculateFields();
  },
  data() {
    return {
      playerData: {},
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
        crossbowExpert: false,
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
      weapons: {},
      weaponList: [],
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
        this.fightingStyle == this.fightingStyles.duelling && !this.weapon.heavy
          ? 2
          : 0;
      var attackDamage =
        this.averageDamageDie + extraDamage + this.attackStat + this.magicBonus;
      return (this.abilities.sharpshooter && this.weapon.ranged) ||
        (this.abilities.greatWeaponMaster &&
          (this.weapon.heavy || this.weapon.versatile))
        ? attackDamage + 10
        : attackDamage;
    },
    bonusAttackDamage() {
      if (this.allowedToDualWield) {
        var magicBonus = this.bonuses.magic ? 1 : 0;
        var toHit = this.proficiencyBonus + this.attackBonus + magicBonus;
        var chanceToHit = this.getChanceToHitFromBonusToHit(toHit);
        return (
          (this.bonusWeapon.damage + this.attackStat + magicBonus) *
            chanceToHit +
          this.chanceToCrit * this.bonusWeapon.damage
        );
      }
      return 0;
    },
    allowedToDualWield() {
      if (this.fightingStyle == this.fightingStyles.twoWeapon) {
        return this.abilities.dualWielder
          ? !this.weapon.heavy
          : this.weapon.light;
      }
      return false;
    },
    attackBonus() {
      var attackBonus = this.attackStat + this.magicBonus;
      if (
        this.fightingStyle == this.fightingStyles.archery &&
        this.weapon.ranged
      ) {
        attackBonus =
          this.abilities.sharpshooter && this.weapon.ranged
            ? attackBonus - 3
            : attackBonus + 2;
      }
      return this.abilities.greatWeaponMaster &&
        (this.weapon.heavy || this.weapon.versatile)
        ? attackBonus - 5
        : attackBonus;
    },
    magicBonus() {
      return !this.abilities.shadowBlade && this.bonuses.magic ? 1 : 0;
    },
    chanceToHit() {
      var toHit = this.proficiencyBonus + this.attackBonus;
      return this.getChanceToHitFromBonusToHit(toHit);
    },
    chanceOfAHit() {
      return 1 - Math.pow(1 - this.chanceToHit, this.numberOfAttacks);
    },
    chanceToCrit() {
      var critChance = 0.05;
      if (this.subclass == "Champion") {
        if (this.characterLevel >= 15) {
          critChance = 0.15;
        } else if (this.characterLevel >= 3) {
          critChance = 0.1;
        }
      }
      return this.bonuses.advantage
        ? 1 - Math.pow(1 - critChance, 2)
        : critChance;
    },
    chanceOfACrit() {
      return 1 - Math.pow(1 - this.chanceToCrit, this.numberOfAttacks);
    },
    averageDamageDie() {
      if (
        this.fightingStyle == this.fightingStyles.twoHanded &&
        (this.weapon.heavy || this.weapon.versatile)
      ) {
        return this.greatWeaponFightingBonus;
      }
      return this.weapon.damage;
    },
    abilityDamage() {
      var damageChance = this.chanceToHit + this.chanceToCrit;
      if (this.superiorityDieDamage > 0) {
        return (
          (this.chanceOfAHit + this.chanceOfACrit) * this.superiorityDieDamage
        );
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
          ? 4.5 * (this.chanceOfAHit + this.chanceOfACrit)
          : 0;
        return huntersMarkDamage + colossusSlayerDamage + this.wolfDamage;
      }
      return 0;
    },
    superiorityDieDamage() {
      if (this.subclass == "Battle Master" && this.bonuses.superiorityDie) {
        if (this.characterLevel >= 18) {
          return 6.5;
        } else if (this.characterLevel >= 10) {
          return 5.5;
        } else if (this.characterLevel >= 3) {
          return 4.5;
        }
      }
      return 0;
    },
    warMagicDamage() {
      if (this.subclass == "Eldritch Knight" && this.abilities.warMagic) {
        if (this.characterLevel >= 17) {
          return 13.5;
        } else if (this.characterLevel >= 11) {
          return 9;
        } else if (this.characterLevel >= 7) {
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
        if (this.characterLevel >= 11) {
          return 2;
        } else if (this.characterLevel >= 3) {
          return 1;
        }
      }
      this.abilities.wolfAttack = false;
      return 0;
    },
    boomingBladeDamage() {
      var moveDamage = this.warMagicDamage + 4.5;
      return (
        parseFloat(this.totalDamage) +
        this.chanceToHit * moveDamage
      ).toFixed(1);
    },
    greatWeaponFightingBonus() {
      if (this.weapon == this.weapons.greatsword) {
        return this.weapon.damage + 4 / 3;
      }
      var weaponDamage = this.weapon.versatile
        ? this.weapon.damage + 1
        : this.weapon.damage;
      var diceMax = weaponDamage * 2 - 1;
      var rerollChance = 2 / diceMax;
      return (
        rerollChance * weaponDamage + (1 - rerollChance) * (weaponDamage + 1)
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
        this.attackStat = this.characterLevel >= 6 ? 5 : baseStat;
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
          this.weapon =
            this.characterLevel < 5 || this.abilities.crossbowExpert
              ? this.weapons.heavyCrossbow
              : this.weapons.longbow;
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
      if (this.weapon.loading && !this.abilities.crossbowExpert) {
        this.numberOfAttacks = 1;
      }
    },
    disableImpossibleAbilities() {
      if (this.fightingStyle != this.fightingStyles.archery) {
        this.abilities.sharpshooter = false;
        this.abilities.crossbowExpert = false;
      }
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
      this.abilities.greatWeaponMaster =
        this.weapon.heavy || this.weapon.versatile
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
    playerData: function() {
      calculatorApi.getDamage(this.playerData).then(data => {
        console.log(data);
      });
    },
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
    weapon: {
      deep: true,
      handler() {
        this.calculateNumberOfAttacks();
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
      }
    }
  }
};
</script>
