<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">Guess the capital!</span>
      <v-btn icon @click="resetScores" color="white" class="ml-4">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </v-card-title>
    <v-row v-if="country" align="center" class="mt-2">
      <v-col md="auto">
        <v-card-title>{{"Country: " + country.name}}</v-card-title>
      </v-col>
      <v-col md="auto">
        <v-img class="elevation-5" contain max-height="50" max-width="60" :src="country.flag"></v-img>
      </v-col>
    </v-row>
    <v-card-text>
      <v-row>
        <v-col cols="4" sm="4">
          <v-text-field
            class="mt-1"
            outlined
            v-model="capitalGuess"
            @keyup.enter="guessCapital()"
            append-icon="mdi-magnify"
            label="Enter the country capital (no accents needed)"
            required
          ></v-text-field>
        </v-col>
        <v-col md="auto">
          <v-fab-transition>
            <v-btn
              class="mr-2 mt-3"
              color="primary"
              v-if="capitalGuess"
              @click="guessCapital()"
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
    this.getCountryCapitals();
  },
  data() {
    return {
      country: null,
      capitalGuess: null,
      countryCapitalUrl: "https://restcountries.eu/rest/v2/all",
      fullCountrylist: [],
      unusedCountryList: [],
      result: null,
      guesses: 0,
      score: 0
    };
  },
  computed: {
    deaccentedCapital() {
      return this.country.capital
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
    },
    capitalMatch() {
      return [
        this.country.capital.toLowerCase(),
        this.deaccentedCapital.toLowerCase()
      ].includes(this.capitalGuess.toLowerCase().trim());
    }
  },
  methods: {
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
      this.capitalGuess = "";
      var country = this.unusedCountryList[
        Math.floor(Math.random() * this.unusedCountryList.length)
      ];
      this.unusedCountryList =
        this.unusedCountryList.length == 1
          ? this.fullCountrylist
          : this.unusedCountryList.filter(x => x !== country);
      return country;
    },
    guessCapital() {
      this.guesses += 1;
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
    capitalGuess: function() {
      if (this.capitalMatch) {
        this.guessCapital();
      }
    }
  }
};
</script>
