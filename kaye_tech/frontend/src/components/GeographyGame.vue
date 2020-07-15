<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <v-icon large class="mr-2">mdi-earth</v-icon>
      <span class="white--text">{{`Guess the ${gameMode.headerText}!`}}</span>
      <v-btn icon @click="resetScores" color="white" class="ml-4">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
      <div>
        <v-select
          class="mx-4 mb-n7"
          md="auto"
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
      </div>
    </v-card-title>
    <v-row v-if="country" align="center" class="mt-2">
      <v-col md="auto" v-if="gameMode.capitalGame">
        <v-card-title>{{"Country: " + country.name}}</v-card-title>
      </v-col>
      <v-col md="auto" v-if="!gameMode.capitalGame">
        <v-card-title>{{"Flag: "}}</v-card-title>
      </v-col>
      <v-col md="auto">
        <v-img class="elevation-5" contain max-width="60" :src="country.flag"></v-img>
      </v-col>
    </v-row>
    <v-card-text>
      <v-row>
        <v-col cols="4" sm="4">
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
        <v-col md="auto">
          <v-fab-transition>
            <v-btn
              class="mr-2 mt-3"
              color="primary"
              v-if="userGuess"
              @click="validateGuess()"
            >{{"Pass" }}</v-btn>
          </v-fab-transition>
        </v-col>
      </v-row>
    </v-card-text>
    <v-fab-transition>
      <v-card-title v-if="result">{{result + " - score: " + score + "/" + guesses}}</v-card-title>
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
      userGuess: null,
      countryCapitalUrl: "https://restcountries.eu/rest/v2/all",
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
      return this.country
        ? [
            this.country.capital.toLowerCase(),
            this.getDeaccentedWord(this.country.capital).toLowerCase()
          ].includes(this.userGuess.toLowerCase().trim())
        : false;
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
      var name = this.country.name;
      name = name
        .replace("n Arab Republic", "")
        .replace("Republic of ", "")
        .replace("Nation of ", "")
        .replace("Kingdom of ", "")
        .replace("n Federation", "")
        .replace("Darussalam", "")
        .replace("Viet Nam", "Vietnam");
      name =
        name.indexOf(",") != -1 ? name.substring(0, name.indexOf(",")) : name;
      return name.replace(/ *\([^)]*\) */g, "");
    },
    possibleCountrySpellings() {
      var possibleSpellings = this.country.altSpellings;
      possibleSpellings.shift();
      if (this.easiestCountryName) {
        possibleSpellings.push(this.easiestCountryName);
      }
      return possibleSpellings;
    }
  },
  methods: {
    getDeaccentedWord(word) {
      return word.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    },
    getCountryCapitals() {
      var countryApiResponse = axios
        .get(this.countryCapitalUrl, {
          headers: { Accept: "application/json" }
        })
        .then(response => response.data)
        .catch(error => console.log(error));
      countryApiResponse.then(data => {
        this.fullCountrylist = data.filter(function(country) {
          var alpha2CodesToExclude = [
            "AX",
            "AS",
            "AI",
            "AQ",
            "AW",
            "BM",
            "BQ",
            "BV",
            "IO",
            "UM",
            "VG",
            "VI",
            "KY",
            "CX",
            "CC",
            "CK",
            "CW",
            "FK",
            "FA",
            "FO",
            "GF",
            "PF",
            "TF",
            "GI",
            "GL",
            "GP",
            "GU",
            "GG",
            "HM",
            "HK",
            "IM",
            "JE",
            "MO",
            "MQ",
            "YT",
            "MS",
            "NC",
            "NU",
            "NF",
            "MP",
            "PN",
            "PR",
            "BL",
            "SH",
            "MF",
            "PM",
            "SX",
            "GS",
            "SJ",
            "TK",
            "TC",
            "WF",
            "EH",
            "RE"
          ];
          return !alpha2CodesToExclude.includes(country.alpha2Code);
        });
        this.unusedCountryList = this.fullCountrylist;
        this.country = this.pickNewCountry();
      });
    },
    pickNewCountry() {
      this.userGuess = "";
      var country = this.unusedCountryList[
        Math.floor(Math.random() * this.unusedCountryList.length)
      ];
      this.unusedCountryList =
        this.unusedCountryList.length == 1
          ? this.fullCountrylist
          : this.unusedCountryList.filter(x => x !== country);
      return country;
    },
    validateGuess() {
      this.guesses += 1;
      if (this.gameMode.capitalGame) {
        if (this.capitalMatch) {
          this.score += 1;
          this.result = "You guessed correctly!";
        } else {
          this.result =
            "Bad luck, the capital of " +
            this.country.name +
            " is: " +
            this.country.capital;
        }
      } else {
        if (this.countryMatch) {
          this.score += 1;
          this.result = "You guessed correctly!";
        } else {
          this.result = "Bad luck, that flag belonged to " + this.country.name;
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
    userGuess: function() {
      if (this.gameMode.capitalGame ? this.capitalMatch : this.countryMatch) {
        this.validateGuess();
      }
    },
    gameMode: function() {
      this.resetScores();
    }
  }
};
</script>
