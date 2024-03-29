<template>
  <v-card>
    <v-card-title class="primary headline">
      <v-row align="center" class="my-n3">
        <v-col cols="12" md="auto" align="center" class="ml-md-0 ml-n4">
          <v-icon large color="white" class="mr-2">mdi-earth</v-icon>
          <span class="white--text mr-4">{{
            `Guess the ${gameMode.headerText}!`
          }}</span>
        </v-col>
        <v-col cols="8" class="mb-n8" md="auto">
          <v-select
            color="white"
            dark
            round
            outlined
            v-model="gameMode"
            item-text="displayText"
            :items="modes"
            attach
            label="Game Mode"
            :menu-props="{ transition: 'slide-y-transition' }"
          ></v-select>
        </v-col>
        <v-col cols="auto">
          <v-btn icon large @click="resetScores" color="white">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-title>
    <v-row v-if="country" align="center" class="mt-2">
      <v-col cols="8" md="auto" v-if="gameMode.capitalGame">
        <v-card-text style="font-size: 1.4em">{{
          "Country: " + country.name.common
        }}</v-card-text>
      </v-col>
      <v-col cols="4" md="auto" v-if="!gameMode.capitalGame">
        <v-card-title>{{ "Flag: " }}</v-card-title>
      </v-col>
      <v-col cols="4" md="auto">
        <v-img
          class="elevation-5"
          contain
          max-width="60"
          :src="country.flags.png"
        ></v-img>
      </v-col>
    </v-row>
    <v-card-text>
      <v-row>
        <v-col cols="9" md="4">
          <v-text-field
            class="mt-1"
            outlined
            v-model="userGuess"
            @keyup.enter="validateGuess()"
            append-icon="mdi-magnify"
            :label="gameMode.instruction"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="3" md="auto">
          <v-fab-transition>
            <v-btn
              class="mr-2 ml-n1 mt-3"
              color="primary"
              v-if="userGuess"
              @click="validateGuess()"
              >{{ "Pass" }}</v-btn
            >
          </v-fab-transition>
        </v-col>
      </v-row>
    </v-card-text>
    <v-fab-transition>
      <v-row v-if="result" align="center">
        <v-col cols="2" md="auto" v-if="!gameMode.capitalGame">
          <v-img
            class="elevation-5 mb-1 ml-5 mr-n2"
            contain
            max-width="50"
            :src="previousCountry.flags.png"
          ></v-img>
        </v-col>
        <v-col cols="10" md="auto">
          <v-card-text style="font-size: 1.4em">{{
            result + " - score: " + score + "/" + guesses
          }}</v-card-text>
        </v-col>
      </v-row>
    </v-fab-transition>
  </v-card>
</template>

<script>
import axios from "axios";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default {
  components: {},
  created() {
    this.gameMode = this.modes[0].value;
    this.getCountryCapitals();
  },
  data() {
    return {
      country: null,
      previousCountry: null,
      userGuess: null,
      countryCapitalUrl: "https://restcountries.com/v3.1/all",
      fullCountrylist: [],
      unusedCountryList: [],
      result: null,
      guesses: 0,
      score: 0,
      modes: [
        {
          displayText: "Capitals",
          value: {
            capitalGame: true,
            headerText: "capital",
            instruction: "What's the country's capital?"
          }
        },
        {
          displayText: "Flags",
          value: { headerText: "country", instruction: "Whose flag is that?" }
        }
      ],
      gameMode: null
    };
  },
  computed: {
    capitalMatch() {
      if (this.country) {
        var capitals = this.country.capital.map((capital) =>
          this.getDeaccentedWord(capital).toLowerCase()
        );
        return capitals.includes(this.userGuess.toLowerCase().trim());
      }
      return false;
    },
    countryMatch() {
      for (var country of this.possibleCountrySpellings) {
        if (country.toLowerCase() == this.userGuess.toLowerCase().trim()) {
          return true;
        }
      }
      return false;
    },
    easiestCountryName() {
      var name = this.country.name.common;
      name = name
        .replace("n Arab Republic", "")
        .replace("City of ", "")
        .replace("Republic of ", "")
        .replace("Nation of ", "")
        .replace("Kingdom of ", "")
        .replace("n Federation", "")
        .replace("Darussalam", "")
        .replace("Viet Nam", "Vietnam");
      name =
        name.indexOf(",") != -1 ? name.substring(0, name.indexOf(",")) : name;
      return this.getDeaccentedWord(name.replace(/ *\([^)]*\) */g, ""));
    },
    possibleCountrySpellings() {
      var possibleSpellings = this.country.altSpellings;
      possibleSpellings.shift();
      if (this.easiestCountryName) {
        possibleSpellings.push(this.easiestCountryName);
      }
      possibleSpellings.push(this.country.name.common);
      return possibleSpellings;
    }
  },
  methods: {
    getDeaccentedWord(word) {
      return word.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    },
    async getCountryCapitals() {
      var countryApiResponse = await axios.get(this.countryCapitalUrl, {
        headers: { Accept: "application/json" }
      });
      this.fullCountrylist = countryApiResponse.data.filter(function (country) {
        return country.unMember;
      });
      this.unusedCountryList = this.fullCountrylist;
      this.country = this.pickNewCountry();
    },
    pickNewCountry() {
      this.userGuess = "";
      var country =
        this.unusedCountryList[
          Math.floor(Math.random() * this.unusedCountryList.length)
        ];
      this.unusedCountryList =
        this.unusedCountryList.length == 1
          ? this.fullCountrylist
          : this.unusedCountryList.filter((x) => x !== country);
      return country;
    },
    validateGuess() {
      this.guesses += 1;
      this.previousCountry = this.country;
      if (this.gameMode.capitalGame) {
        if (this.capitalMatch) {
          this.score += 1;
          this.result = "You guessed correctly!";
        } else {
          this.result =
            "Bad luck, the capital of " +
            this.country.name.common +
            " is: " +
            this.country.capital.join(", ");
        }
      } else {
        if (this.countryMatch) {
          this.score += 1;
          this.result = "You guessed correctly!";
        } else {
          this.result =
            "Bad luck, that flag belonged to " + this.country.name.common;
        }
      }
      this.country = this.pickNewCountry();
    },
    resetScores() {
      this.result = null;
      this.score = 0;
      this.guesses = 0;
      this.unusedCountryList = this.fullCountrylist;
      this.country = this.pickNewCountry();
    }
  },
  watch: {
    userGuess: function () {
      if (this.gameMode.capitalGame ? this.capitalMatch : this.countryMatch) {
        this.validateGuess();
      }
    },
    gameMode: function () {
      this.resetScores();
    }
  }
};
</script>
