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
          :append-icon="icons[characterClass]"
          v-model="characterClass"
          :items="Object.values(classes)"
          attach
          label="Class"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="12" md="2">
        <v-select
          outlined
          v-model="subclass"
          :items="subclassOptions"
          attach
          :append-icon="icons[subclass]"
          label="Subclass"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="12" md="2">
        <v-select
          outlined
          v-model="fightingStyle"
          :items="Object.values(fightingStyles)"
          attach
          label="Style"
          :append-icon="icons[fightingStyle]"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
    </v-row>
    <v-card-title>Stats</v-card-title>
    <v-row class="mx-2">
      <v-col cols="6" md="1">
        <v-text-field
          outlined
          v-model="proficiencyBonus"
          readonly
          label="Proficiency"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-text-field>
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
          :append-icon="icons[weapon.name]"
          v-model="weapon"
          :items="weapons"
          item-text="name"
          attach
          label="Weapons"
          return-object
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col cols="6" md="auto">
        <v-text-field
          append-icon="mdi-shield"
          type="number"
          outlined
          v-model="averageAC"
          label="Enemy AC"
          required
        ></v-text-field>
      </v-col>
      <v-col cols="6" md="1">
        <v-text-field
          outlined
          append-icon="fas fa-crosshairs"
          v-model="numberOfAttacks"
          readonly
          label="Attacks"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-text-field>
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
  created() {
    this.weapon = this.weapon.name ? this.weapon : { name: "Longsword" };
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
      subclasses: [],
      fightingStyles: {},
      averageAC: 14,
      attackStat: 3,
      proficiencyBonus: 2,
      numberOfAttacks: 1,
      weapons: [],
      weapon: {},
      bonusWeapon: {},
      damageOutput: 0,
      boomingBladeDamage: 0,
      casterMulticlasses: 0,
      icons: {
        Fighter: "mdi-sword-cross",
        Ranger: "mdi-grass",
        "Beast Master": "fab fa-wolf-pack-battalion",
        Hunter: "mdi-paw",
        "Eldritch Knight": "mdi-wizard-hat",
        "Battle Master": "mdi-chess-queen",
        Champion: "mdi-trophy",
        Archery: "mdi-bullseye-arrow",
        Duelling: "mdi-sword",
        Defence: "mdi-chess-rook",
        "Two-Handed": "fas fa-handshake",
        "Two-Weapon": "fas fa-hands",
        Protection: "mdi-shield",
        Greatsword: "mdi-sword",
        Longbow: "mdi-bullseye-arrow",
        Handaxe: "mdi-axe",
        Greataxe: "mdi-axe",
        "Heavy Crossbow": "mdi-arrow-decision",
        Longsword: "mdi-sword"
      }
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
    },
    subclassOptions() {
      for (var classKey of Object.keys(this.classes)) {
        if (this.characterClass == this.classes[classKey]) {
          return Object.values(this.subclasses[classKey]);
        }
      }
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
    getWeaponByName(name) {
      var filteredList = this.weapons.filter(function (weapon) {
        return weapon.name == name;
      });
      return filteredList.length > 0 ? filteredList[0] : {};
    },
    calculateFields() {
      this.calculateAttackStat();
      this.chooseWeaponFromStyle();
      this.calculateAverageAC();
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
        case this.fightingStyles.DUELLING:
          this.weapon = this.getWeaponByName("Longsword");
          break;
        case this.fightingStyles.TWO_HANDED:
          this.weapon = this.getWeaponByName("Greatsword");
          break;
        case this.fightingStyles.ARCHERY:
          this.weapon =
            this.characterLevel < 5 || this.feats.crossbowExpert
              ? this.getWeaponByName("Heavy Crossbow")
              : this.getWeaponByName("Longbow");
          break;
        case this.fightingStyles.TWO_WEAPON:
          this.weapon = this.feats.dualWielder
            ? this.getWeaponByName("Longsword")
            : this.getWeaponByName("Handaxe");
          this.bonusWeapon = this.weapon;
          break;
        case this.fightingStyles.PROTECTION:
          this.weapon = this.getWeaponByName("Longsword");
          break;
        case this.fightingStyles.DEFENCE:
          this.weapon = this.getWeaponByName("Greatsword");
      }
    },
    calculateAverageAC() {
      this.averageAC = Math.ceil(this.characterLevel / 3) + 13;
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
          this.fightingStyles = data.fightingStyles;
          if (this.weapons.length == 0) {
            this.weapons = data.weapons;
            this.weapon = this.weapons[0];
          }
          this.numberOfAttacks = data.numberOfAttacks;
          this.proficiencyBonus = data.proficiencyBonus;
          this.classes = data.classes;
          this.subclasses = data.subclasses;
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
        this.disableImpossibleAbilities();
        this.resetAbilities();
        this.subclass = this.subclassOptions[0];
      }
    },
    subclass: {
      deep: true,
      handler() {
        this.resetAbilities();
      }
    },
    fightingStyle: {
      deep: true,
      handler() {
        this.chooseWeaponFromStyle();
        this.disableImpossibleAbilities();
      }
    },
    abilities: {
      deep: true,
      handler() {
        this.chooseWeaponFromStyle();
        this.disableImpossibleAbilities();
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
