<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">News search</span>
    </v-card-title>
    <v-row align="center" justify="start" class="ma-2">
      <v-card-title>Search Criteria:</v-card-title>
      <v-col v-for="(searchTerm, i) in searchCriteria" :key="searchTerm.text" class="shrink">
        <v-chip
          close
          @click:close="searchCriteria.splice(i, 1)"
        >{{searchTerm.type +": " +searchTerm.text }}</v-chip>
      </v-col>
    </v-row>
    <v-row class="ml-2">
      <v-col cols="3">
        <v-text-field
          v-model="searchTerm"
          @keypress.enter="addSearch()"
          hint="The news search term"
          required
        ></v-text-field>
        <v-btn
          :disabled="(!searchTerm) || keywords.includes(searchTerm)"
          class="mb-2 mr-2"
          color="primary"
          @click="addSearch()"
        >{{ "Add" }}</v-btn>
      </v-col>
      <v-col cols="3">
        <v-select
          v-model="section"
          :items="guardianSections"
          item-text="webTitle"
          item-value="id"
          label="Section (Optional)"
          attach
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
        <v-btn
          :disabled="(!section) || sections.includes(section)"
          class="mb-2 mr-2"
          color="primary"
          @click="addSection()"
        >{{ "Add" }}</v-btn>
      </v-col>
      <v-col cols="1">
        <v-select
          v-model="pageSize"
          :items="[10,25,50]"
          attach
          label="Results"
          :menu-props="{ transition: 'slide-y-transition' }"
        ></v-select>
      </v-col>
      <v-col>
        <v-btn class="mb-2 mr-2" color="primary" @click="fetchArticles()">{{ "Search" }}</v-btn>
      </v-col>
    </v-row>
    <v-card color="card" v-if="articles.length>0" class="ma-4">
      <v-card-title class="headline">Results</v-card-title>
      <v-divider></v-divider>
      <v-list>
        <template v-for="(item, index) in articles">
          <v-list-item :key="index">
            <v-list-item-content>
              <v-row justify="start">
                <v-col md="auto">
                  <v-list-item-title v-html="item.webTitle"></v-list-item-title>
                  <v-list-item-subtitle>
                    <a :href="item.webUrl">{{item.id}}</a>
                  </v-list-item-subtitle>
                </v-col>
                <v-col md="auto">
                  <v-btn icon :href="item.webUrl">
                    <v-icon color="primary" large>mdi-arrow-right-circle-outline</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
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
    this.fetchGuardianSections();
    accountsApi.getCurrentUser().then(data => {
      this.currentUser = data.username;
      console.log(this.currentUser);
    });
    this.fetchArticles();
  },
  data() {
    return {
      searchTerm: null,
      guardianSections: [{ webTitle: "" }],
      articles: [],
      currentUser: "",
      section: null,
      pageSize: 10,
      searchCriteria: [],
      searchParameter: "",
      keywordParams: [],
      sectionParams: []
    };
  },
  computed: {
    keywords() {
      return this.searchCriteria
        .filter(function(searchTerm) {
          return searchTerm.type == "Keyword";
        })
        .map(a => a.text);
    },
    sections() {
      return this.searchCriteria
        .filter(function(searchTerm) {
          return searchTerm.type == "Section";
        })
        .map(a => a.text);
    }
  },
  methods: {
    fetchArticles() {
      if (this.searchTerm) {
        this.addSearch();
      }
      if (this.section && this.section.webTitle != "None") {
        this.addSection();
      }
      this.keywordParams = this.keywords.join(" OR ");
      this.sectionParams = this.sections.join(" OR ");
      var params = {
        q: this.keywordParams ? this.keywordParams : null,
        section: this.sectionParams ? this.sectionParams : null,
        "page-size": this.pageSize
      };
      newsApi.fetchArticles(params).then(data => {
        console.log(data);
        this.articles = data.response.results;
      });
    },

    addSearch() {
      this.searchCriteria.push({
        text: this.searchTerm,
        type: "Keyword"
      });
      this.searchTerm = "";
    },

    addSection() {
      this.searchCriteria.push({ text: this.section, type: "Section" });
      this.section = "";
    },

    removeSearch(item) {
      this.searchCriteria.splice(this.searchCriteria.indexOf(item), 1);
      this.searchCriteria = [...this.searchCriteria];
    },

    fetchGuardianSections() {
      newsApi.fetchSections().then(data => {
        this.guardianSections = data.response.results;
        this.guardianSections.push({ id: null, webTitle: "None" });
      });
    }
  }
};
</script>
