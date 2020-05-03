<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">News search</span>
    </v-card-title>
    <v-card-title>Search term</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="6" sm="6">
          <v-text-field
            v-model="searchTerm"
            @keypress.enter="fetchArticles()"
            hint="The news search term"
            required
          ></v-text-field>
        </v-col>
        <v-col>
          <v-btn
            :disabled="searchTerm.length == 0"
            class="mb-2 mr-2"
            color="primary"
            @click="fetchArticles()"
          >{{ "Search" }}</v-btn>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card color="card" v-if="articles.length>0" class="ma-4">
      <v-card-title class="headline">Results</v-card-title>
      <v-divider></v-divider>
      <v-list>
        <template v-for="(item, index) in articles">
          <v-list-item :key="index">
            <v-list-item-content>
              <v-list-item-title v-html="item.webTitle"></v-list-item-title>
              <v-list-item-subtitle>
                <a :href="item.webUrl">{{item.id}}</a>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-list>
    </v-card>
    <br />
  </v-card>
</template>
<script>
import AccountsApi from "@/apis/AccountsApi";
import NewsApi from "@/apis/NewsApi";

const accountsApi = new AccountsApi();
const newsApi = new NewsApi();

export default {
  components: {},
  created() {
    accountsApi.getCurrentUser().then(data => {
      this.currentUser = data.username;
      console.log(this.currentUser);
      this.fetchSections();
    });
  },
  data() {
    return {
      searchTerm: "",
      articles: [],
      currentUser: ""
    };
  },
  computed: {},
  methods: {
    fetchArticles() {
      if (this.searchTerm.length > 0) {
        newsApi.fetchArticles().then(data => {
          this.articles = data.response.results;
        });
      }
    },

    fetchSections() {
      newsApi.fetchSections().then(data => {
        console.log(data);
      });
    }
  }
};
</script>
