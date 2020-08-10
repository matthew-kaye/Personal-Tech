<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">Joke search</span>
    </v-card-title>
    <v-card-title>Search term - search for a joke by typing in a keyword:</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12" md="3">
          <v-text-field
            class="mt-1"
            outlined
            v-model="jokeSearch"
            @keypress.enter="findJoke(jokeSearch)"
            append-icon="mdi-magnify"
            label="Enter a search term for the joke, e.g. cat"
            required
          ></v-text-field>
        </v-col>
        <v-col md="auto">
          <v-checkbox v-model="programming" label="Programming"></v-checkbox>
        </v-col>
        <v-col md="auto">
          <v-fab-transition>
            <v-btn
              class="mr-2 mt-3"
              color="primary"
              @click="findJoke(jokeSearch)"
            >{{ jokeSearch.length>0?"Search":"Get Random" }}</v-btn>
          </v-fab-transition>
        </v-col>
      </v-row>
      <v-fab-transition class="my-4">
        <div class="white--text" style="font-size:1.4em" v-if="joke">{{"Your Joke: " + joke}}</div>
      </v-fab-transition>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
var MAX_JOKES_RETURNED_BY_SITE = 20;

export default {
  components: {},
  created() {
    this.findJoke("");
  },
  data() {
    return {
      jokeSearch: "",
      dadJoke: true,
      programming: false,
      clean: true,
      dadJokeUrl: "https://icanhazdadjoke.com/search",
      jokeApiUrl: "https://sv443.net/jokeapi/v2/joke/",
      joke: null
    };
  },
  computed: {
    jokeType() {
      return this.programming ? "Programming" : "Miscellaneous";
    }
  },
  methods: {
    findJoke(searchTerm) {
      this.joke = null;
      this.programming
        ? this.findJokeApiJoke(searchTerm)
        : this.findDadJoke(searchTerm);
    },
    findDadJoke(searchTerm) {
      var jokeResponse = axios
        .get(this.dadJokeUrl, {
          params: { term: searchTerm },
          headers: { Accept: "application/json" }
        })
        .then((response) => response.data)
        .catch((error) => console.log(error));
      jokeResponse.then((data) => {
        if (data.total_jokes > 0) {
          var max = Math.min(MAX_JOKES_RETURNED_BY_SITE, data.total_jokes);
          this.joke = data.results[Math.floor(Math.random() * max)].joke;
        } else {
          this.findJokeApiJoke(searchTerm);
        }
      });
    },
    findJokeApiJoke(searchTerm) {
      var params = {
        blacklistFlags: "nsfw,racist,sexist,religious"
      };
      if (searchTerm.length > 0) {
        params.contains = searchTerm;
      }
      var jokeResponse = axios
        .get(this.jokeApiUrl + this.jokeType, {
          params: params,
          headers: { Accept: "application/json" }
        })
        .then((response) => response.data)
        .catch((error) => console.log(error));
      jokeResponse.then((data) => {
        try {
          if (data.type == "single") {
            this.joke = data.joke;
          } else if (data.type == "twopart") {
            this.joke = data.setup + " - " + data.delivery;
          } else {
            this.joke = `Apparently ${searchTerm} is not a funny word`;
          }
          if (data.id == 144 || data.id == 73) {
            this.joke = null;
          }
        } catch (error) {
          this.joke = "Api call rate exceeded - try again later.";
        }
      });
    }
  }
};
</script>
