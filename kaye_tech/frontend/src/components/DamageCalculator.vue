<template>
  <v-card>
    <v-card-title class="mb-2">Character Options</v-card-title>
    <v-row class="mx-0">
      <v-col cols="6" md="1">
        <v-select
          outlined
          v-model="characterLevel"
          :items="getNumberArray(1, 20)"
          attach
          label="Level"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="6" md="2">
        <v-select
          outlined
          v-model="characterClass"
          :items="classList"
          attach
          label="Class"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="12" md="2">
        <v-select
          outlined
          v-model="subclass"
          :items="subclasses[characterClass]"
          attach
          label="Sublass"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="12" md="2">
        <v-select
          outlined
          v-model="fightingStyle"
          :items="fightingStyleList"
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
          readonly
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
        <v-text-field type="number" outlined v-model="averageAC" label="Enemy AC" required></v-text-field>
      </v-col>
      <v-col cols="6" md="1">
        <v-select
          outlined
          v-model="numberOfAttacks"
          readonly
          :items="getNumberArray(1,5)"
          attach
          label="Attacks"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="6" md="1" v-if="subclass=='Eldritch Knight'">
        <v-select
          outlined
          v-model="casterMulticlasses"
          :items="getNumberArray(0, 10)"
          attach
          label="Caster Multiclasses"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col md="auto">
        <v-switch v-model="bonuses.advantage" class="ma-2" label="Advantage"></v-switch>
      </v-col>
      <v-col md="auto">
        <v-switch v-model="bonuses.magicWeapon" class="ma-2" label="+1 Weapon"></v-switch>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card-title>Feats/Abilities</v-card-title>
        <v-row class="ml-2">
          <v-col md="auto" v-if="subclass=='Battle Master'">
            <v-switch
              :disabled="characterLevel<3"
              v-model="abilities.superiority"
              class="ma-2"
              label="Superiority Damage"
            ></v-switch>
          </v-col>
          <v-col md="auto" v-if="subclass=='Eldritch Knight'">
            <v-switch
              :disabled="characterLevel<7"
              v-model="abilities.warMagic"
              class="ma-2"
              label="War Magic (Booming Blade)"
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
            <v-switch v-model="feats.crossbowExpert" class="ma-2" label="Crossbow Expert"></v-switch>
          </v-col>
          <v-col md="auto" v-if="fightingStyle==fightingStyles.archery">
            <v-switch v-model="feats.sharpshooter" class="ma-2" label="Sharpshooter"></v-switch>
          </v-col>
          <v-col md="auto" v-if="(weapon.versatile ||weapon.heavy) && !weapon.ranged">
            <v-switch v-model="feats.greatWeaponMaster" class="ma-2" label="GW Master"></v-switch>
          </v-col>
          <v-col md="auto" v-if="feats.greatWeaponMaster">
            <v-switch v-model="feats.greatWeaponMasterSwing" class="ma-2" label="GW Swing"></v-switch>
          </v-col>
          <v-col md="auto" v-if="fightingStyle==fightingStyles.twoWeapon">
            <v-switch v-model="feats.dualWielder" class="ma-2" label="Dual Wielder"></v-switch>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="11" md="auto" class="ml-4">
        <v-card elevation="10">
          <v-card-title class="primary headline">
            <span
              v-if="abilities.warMagic"
              class="white--text"
            >{{`Damage (moves): ${damageOutput} (${boomingBladeDamage}) `}}</span>
            <span v-else class="white--text">{{"Damage: " + damageOutput }}</span>
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
      greataxe: { name: "Greataxe", heavy: true },
      greatsword: { name: "Greatsword", heavy: true },
      handaxe: {
        name: "Handaxe",
        ranged: true,
        light: true
      },
      heavyCrossbow: {
        name: "Heavy Crossbow",
        ranged: true,
        loading: true,
        heavy: true
      },
      longbow: { name: "Longbow", ranged: true, heavy: true },
      longsword: { name: "Longsword", versatile: true }
    };
    for (var value in this.weapons) {
      this.weaponList.push(this.weapons[value]);
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
        magicWeapon: false
      },
      feats: {
        sharpshooter: false,
        crossbowExpert: false,
        greatWeaponMaster: false,
        greatWeaponMasterSwing: false,
        dualWielder: false
      },
      abilities: {
        warMagic: false,
        huntersMark: false,
        colossusSlayer: false,
        wolfAttack: false,
        shadowBlade: false,
        superiority: false
      },
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
      damageOutput: 0,
      boomingBladeDamage: 0,
      casterMulticlasses: 0
    };
  },
  computed: {
    playerDataToProcess() {
      return {
        characterLevel: this.characterLevel,
        characterClass: this.characterClass,
        subclass: this.subclass,
        fightingStyle: this.fightingStyle,
        weapon: this.weapon.name,
        averageAC: this.averageAC,
        attackStat: this.attackStat,
        abilities: this.abilities,
        bonuses: this.bonuses,
        feats: this.feats,
        casterMulticlasses: this.casterMulticlasses
      };
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
            this.characterLevel < 5 || this.feats.crossbowExpert
              ? this.weapons.heavyCrossbow
              : this.weapons.longbow;
          break;
        case this.fightingStyles.twoWeapon:
          this.weapon = this.feats.dualWielder
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
      if (this.weapon.loading && !this.feats.crossbowExpert) {
        this.numberOfAttacks = 1;
      }
    },
    disableImpossibleAbilities() {
      if (this.fightingStyle != this.fightingStyles.archery) {
        this.feats.sharpshooter = false;
        this.feats.crossbowExpert = false;
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
      this.feats.greatWeaponMaster = !this.weapon.ranged
        ? this.feats.greatWeaponMaster
        : false;
      this.feats.greatWeaponMasterSwing =
        (this.weapon.heavy || this.weapon.versatile) &&
        this.feats.greatWeaponMaster
          ? this.feats.greatWeaponMasterSwing
          : false;
      this.feats.dualWielder =
        this.fightingStyle == this.fightingStyles.twoWeapon
          ? this.feats.dualWielder
          : false;
      this.abilities.shadowBlade =
        this.subclass == "Eldritch Knight" &&
        this.characterLevel > 6 &&
        this.fightingStyle != this.fightingStyles.archery
          ? this.abilities.shadowBlade
          : false;
      this.bonuses.magicWeapon = this.abilities.shadowBlade
        ? false
        : this.bonuses.magicWeapon;
    },
    resetAbilities() {
      for (var key in this.abilities) {
        this.abilities[key] = false;
      }
      for (var key in this.feats) {
        this.feats[key] = false;
      }
      this.casterMulticlasses = 0;
    }
  },
  watch: {
    playerDataToProcess: {
      deep: true,
      handler() {
        calculatorApi.getDamage(this.playerDataToProcess).then((data) => {
          console.log("Calculator Estimate: " + data.damage);
          this.damageOutput = Math.round(data.damage * 100) / 100;
          this.boomingBladeDamage = Math.round(data.damageIfMoves * 100) / 100;
        });
      }
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
        this.resetAbilities();
        this.subclass = this.subclasses[this.characterClass][0];
      }
    },
    subclass: {
      deep: true,
      handler() {
        this.resetAbilities();
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
        this.chooseWeaponFromStyle();
        this.disableImpossibleAbilities();
        this.calculateNumberOfAttacks();
      }
    },
    feats: {
      deep: true,
      handler() {
        this.disableImpossibleAbilities();
      }
    }
  }
};
</script>
