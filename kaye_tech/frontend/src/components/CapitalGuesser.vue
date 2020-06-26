<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">Guess the capital!</span>
      <v-btn icon @click="resetScores" class="ml-4">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </v-card-title>
    <v-row v-if="country" class="mt-2">
      <v-col md="auto">
        <v-card-title>{{"Country: " + country.name}}</v-card-title>
      </v-col>
      <v-col class="mt-4">
        <v-img contain max-width="50" :src="country.flag"></v-img>
      </v-col>
    </v-row>
    <v-card-text>
      <v-row>
        <v-col cols="4" sm="4">
          <v-text-field
            class="mt-1"
            outlined
            v-model="capitalGuess"
            @keypress.enter="checkGuess(capitalGuess)"
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
              @click="checkGuess(capitalGuess)"
            >{{"Guess" }}</v-btn>
          </v-fab-transition>
        </v-col>
      </v-row>
    </v-card-text>
    <v-fab-transition>
      <v-card-title v-if="result">{{result + " - score: " + score + "/" + guesses}}</v-card-title>
      <v-card-title v-if="!result">Error: Failed to retrieve data - max api calls likely reached</v-card-title>
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
      countryCapitalList: [],
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
        this.countryCapitalList = data.filter(function(country) {
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
            "GF",
            "PF",
            "TF",
            "GI",
            "GL",
            "GP",
            "GU",
            "GG",
            "HM",
            "VA",
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
            "EH"
          ];
          return !alpha2CodesToExclude.includes(country.alpha2Code);
        });
        this.country = this.pickNewCountry();
      });
    },
    pickNewCountry() {
      this.capitalGuess = null;
      var country = this.countryCapitalList[
        Math.floor(Math.random() * this.countryCapitalList.length)
      ];
      return country.capital && !this.country == country
        ? country
        : this.pickNewCountry();
    },
    checkGuess(capitalGuess) {
      if (capitalGuess) {
        this.guesses += 1;
        if (
          [
            this.country.capital.toLowerCase(),
            this.deaccentedCapital.toLowerCase()
          ].includes(capitalGuess.toLowerCase().trim())
        ) {
          this.score += 1;
          this.result = "You guessed correctly!";
        } else {
          this.result =
            "Incorrect, the capital of " +
            this.country.name +
            " is: " +
            this.country.capital;
        }
        this.country = this.pickNewCountry();
      }
    },
    resetScores() {
      this.result = null;
      this.score = 0;
      this.guesses = 0;
      this.country = this.pickNewCountry();
    }
  }
};
</script>
