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
                @click:close="searchCriteria.splice(i, 1);fetchArticles()"
              >{{searchTerm.type +": " +searchTerm.text }}</v-chip>
            </v-col>
          </v-row>
          <v-row class="ml-2" justify="start">
            <v-col cols="3">
              <v-autocomplete
                v-model="section"
                :items="guardianSections"
                class="mr-4"
                item-text="webTitle"
                item-value="id"
                label="Section Filters"
                attach
                :menu-props="{ transition: 'slide-y-transition' }"
              ></v-autocomplete>
            </v-col>
            <v-col cols="1">
              <v-select
                v-model="pageSize"
                :items="[10,25,50]"
                class="mr-4"
                attach
                label="Results"
                :menu-props="{ transition: 'slide-y-transition' }"
              ></v-select>
            </v-col>
            <v-col md="auto">
              <v-btn
                :disabled="searchCriteria.includes(abcFilter)"
                color="primary"
                @click="anythingButCovid()"
                icon
                x-large
                append-icon="mdi-cancel"
              >
                <v-icon large>mdi-thermometer-minus</v-icon>
              </v-btn>
            </v-col>
            <v-col cols="3">
              <v-text-field
                v-model="searchTerm"
                @keypress.enter="addSearch()"
                label="Keywords"
                append-icon="mdi-magnify"
                required
              ></v-text-field>
            </v-col>
            <v-col md="auto">
              <v-fab-transition>
                <v-btn
                  v-show="searchTerm && !keywords.includes(searchTerm)"
                  class="mt-2"
                  color="primary"
                  @click="addSearch()"
                >{{ "Add" }}</v-btn>
              </v-fab-transition>
            </v-col>
          </v-row>
          <br />
          <v-card color="card" class="ml-4" width="100%">
            <v-card-title class="headline">Results</v-card-title>
            <v-slide-x-transition>
              <div v-if="articles.length>0">
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
              </div>
            </v-slide-x-transition>
          </v-card>
        </v-col>
        <v-col cols="3" class="ma-4" md="auto">
          <TwitterFeed />
        </v-col>
      </v-row>
      <br />
    </v-card>
    <v-scale-transition>
      <v-btn
        color="primary"
        v-show="offsetTop!=0"
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
    </v-scale-transition>
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
    window.addEventListener("scroll", this.onScroll);
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
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
      sectionParams: [],
      abcFilter: {
        type: "ABC",
        text: "Anything But Coronavirus"
      },
      offsetTop: 0
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
    },
    anythingButCoronavirus() {
      for (var item of this.searchCriteria) {
        if (item.type == "ABC") {
          return true;
        }
      }
      return false;
    }
  },
  methods: {
    fetchArticles() {
      this.articles = [];
      if (this.searchTerm) {
        this.addSearch();
      }
      if (this.section && this.section.webTitle != "None") {
        this.addSection();
      }
      this.keywordParams = this.keywords.join(" OR ");
      var orderBy = this.keywordParams.length > 0 ? "relevance" : "newest";
      var covidString = this.anythingButCoronavirus
        ? "NOT ('coronavirus' OR 'covid' OR 'quarantine' OR 'lockdown' OR 'COV-SARS-2')"
        : "";
      this.keywordParams =
        this.keywordParams.length > 0
          ? this.keywordParams + " AND ".concat(covidString)
          : this.keywordParams.concat(covidString);
      this.sectionParams = this.sections.join(" OR ");
      var params = {
        q: this.keywordParams ? this.keywordParams : null,
        section: this.sectionParams ? this.sectionParams : null,
        "order-by": orderBy,
        "page-size": this.pageSize
      };
      newsApi.fetchArticles(params).then(data => {
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
    fetchGuardianSections() {
      newsApi.fetchSections().then(data => {
        this.guardianSections = data.response.results;
        this.guardianSections.push({ id: null, webTitle: "None" });
      });
    },
    anythingButCovid() {
      this.searchCriteria.push(this.abcFilter);
    },
    onScroll(e) {
      this.offsetTop = e.target.scrollingElement.scrollTop;
    }
  },
  watch: {
    searchCriteria: function() {
      this.fetchArticles();
    },
    pageSize: function() {
      this.fetchArticles();
    },
    section: function() {
      if (this.section) {
        this.searchCriteria.push({ text: this.section, type: "Section" });
        this.section = "";
      }
    }
  }
};
</script>
