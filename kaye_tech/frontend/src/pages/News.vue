<template>
  <div>
    <v-card class="ma-6">
      <v-card-title class="primary headline">
        <span class="white--text">News search</span>
      </v-card-title>
      <v-row justify="start">
        <v-col>
          <v-row align="center" justify="start" md="auto">
            <v-card-title class="ml-4">Search Criteria:</v-card-title>
            <v-col v-for="(searchTerm, i) in searchCriteria" :key="searchTerm.text" class="shrink">
              <v-chip
                close
                @click:close="searchCriteria.splice(i, 1)"
              >{{searchTerm.type +": " +searchTerm.text }}</v-chip>
            </v-col>
          </v-row>
          <v-row class="ml-2" md="auto">
            <v-col cols="3">
              <v-text-field
                v-model="searchTerm"
                @keypress.enter="addSearch()"
                label="Keywords"
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
              <v-autocomplete
                v-model="section"
                :items="guardianSections"
                item-text="webTitle"
                item-value="id"
                label="Section Filters"
                attach
                :menu-props="{ transition: 'slide-y-transition' }"
              ></v-autocomplete>
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
          <v-card color="card" v-if="articles.length>0" class="ml-4" width="100%">
            <v-card-title class="headline">Results</v-card-title>
            <v-divider></v-divider>
            <v-list>
              <template v-for="(item, index) in articles">
                <v-list-item :key="index">
                  <v-list-item-content>
                    <v-row>
                      <v-col md="auto">
                        {{item.webTitle}}
                        <br />
                        <a :href="item.webUrl">{{item.id}}</a>
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
        </v-col>
        <v-col cols="3" class="ma-4" md="auto">
          <TwitterFeed />
        </v-col>
      </v-row>
      <br />
    </v-card>
    <v-btn
      color="primary"
      fixed
      bottom
      right
      fab
      large
      class="mb-10 ma-4"
      @click="$vuetify.goTo(0)"
    >
      <v-icon>mdi-arrow-up</v-icon>
    </v-btn>
  </div>
</template>
<script>
import NewsApi from "@/apis/NewsApi";
import TwitterFeed from "@/components/TwitterFeed.vue";
const newsApi = new NewsApi();

export default {
  components: {
    TwitterFeed
  },
  created() {
    this.fetchGuardianSections();
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
