<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">{{ "Joke search" }}</span>
    </v-card-title>
    <v-card-title>Search term</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="6" sm="6">
          <v-text-field
            v-model="jokeSearch"
            @keypress.enter="findJoke(jokeSearch)"
            hint="The search term for the joke, e.g. cat"
            required
          ></v-text-field>
        </v-col>
        <v-col>
          <v-btn
            :disabled="jokeSearch.length == 0"
            class="mb-2 mr-2"
            color="primary"
            @click="findJoke(jokeSearch)"
          >{{ "Search" }}</v-btn>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card class="my-4" color="card">
      <v-card-title>{{"Your Joke: " + joke}}</v-card-title>
    </v-card>
  </v-card>
</template>

<script>
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default {
  components: {},
  created() {},
  data() {
    return {
      jokeSearch: "",
      baseUrl: "https://icanhazdadjoke.com/search",
      joke: ""
    };
  },
  computed: {},
  methods: {
    findJoke(searchTerm) {
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
            var max = data.total_jokes > 20 ? 19 : data.total_jokes;
            this.joke = data.results[Math.floor(Math.random() * max)].joke;
          } else {
            this.joke = "Apparently that's not a funny word";
          }
        });
      }
    }
  }
};
</script>
