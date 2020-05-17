<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">Joke search</span>
    </v-card-title>
    <v-card-title>Search term - search for a joke by typing in a keyword:</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="3" sm="3">
          <v-text-field
            v-model="jokeSearch"
            @keypress.enter="findJoke(jokeSearch)"
            append-icon="mdi-magnify"
            label="Enter a search term for the joke, e.g. cat"
            required
          ></v-text-field>
        </v-col>
        <v-col md="auto">
          <v-fab-transition>
            <v-btn
              v-if="jokeSearch.length > 0"
              class="mb-2 mr-2"
              color="primary"
              @click="findJoke(jokeSearch)"
            >{{ "Search" }}</v-btn>
          </v-fab-transition>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card class="my-4" color="card">
      <v-fab-transition>
        <v-card-title v-if="joke">{{"Your Joke: " + joke}}</v-card-title>
      </v-fab-transition>
    </v-card>
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
    this.findJoke("a");
  },
  data() {
    return {
      jokeSearch: "",
      baseUrl: "https://icanhazdadjoke.com/search",
      joke: null
    };
  },
  computed: {},
  methods: {
    findJoke(searchTerm) {
      this.joke = null;
      if (searchTerm.length > 0) {
        var jokeResponse = axios
          .get(this.baseUrl, {
            params: { term: searchTerm },
            headers: { Accept: "application/json" }
          })
          .then(response => response.data)
          .catch(error => console.log(error));
        jokeResponse.then(data => {
          if (data.total_jokes > 0) {
            var max = Math.min(MAX_JOKES_RETURNED_BY_SITE, data.total_jokes);
            this.joke = data.results[Math.floor(Math.random() * max)].joke;
          } else {
            this.joke = `Apparently ${searchTerm} is not a funny word`;
          }
        });
      }
    }
  }
};
</script>
