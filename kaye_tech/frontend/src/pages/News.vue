<template>
  <div>
    <v-card class="ma-md-6 ma-2">
      <v-card-title class="primary headline">
        <span class="white--text">News search</span>
        <v-btn class="ml-8" color="primary" @click="tldrTech=!tldrTech">
          <v-icon>mdi-laptop</v-icon>
          <span class="ml-2 hidden-sm-and-down">Tech Summary</span>
        </v-btn>
      </v-card-title>
      <v-dialog v-model="tldrTech" width="900">
        <v-card>
          <v-card-title class="mb-6 primary">
            <span class="headline white--text">Daily Tech Summary</span>
          </v-card-title>
          <v-card-text style="font-size:1.063em" v-html="techNews"></v-card-text>
          <v-row v-if="!techNews" class="fill-height ma-0" align="center" justify="center">
            <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
          </v-row>
          <v-card-subtitle>
            Source:
            <a :href="tldrUrl">TLDR News</a>
          </v-card-subtitle>
        </v-card>
      </v-dialog>
      <v-row justify="start">
        <v-col cols="12" md="auto">
          <v-row align="center" justify="start" md="auto">
            <v-card-title class="ml-4">Search Criteria:</v-card-title>
            <v-col
              cols="12"
              md="auto"
              v-for="(searchTerm, i) in searchCriteria"
              :key="searchTerm.text"
              class="shrink ml-4"
            >
              <v-chip
                close
                @click:close="searchCriteria.splice(i, 1);fetchArticles()"
              >{{searchTerm.type +": " +searchTerm.text }}</v-chip>
            </v-col>
          </v-row>
          <v-row class="mx-2" justify="start">
            <v-col lg="auto" md="6" cols="12">
              <v-autocomplete
                v-model="section"
                :items="guardianSections"
                item-text="webTitle"
                item-value="id"
                label="Section Filters"
                round
                outlined
                hint
                attach
                placeholder="Section"
                :menu-props="{ transition: 'slide-y-transition' }"
              ></v-autocomplete>
            </v-col>
            <v-col cols="9" lg="auto" md="6">
              <v-select
                round
                outlined
                v-model="pageSize"
                :items="[10,25,50]"
                attach
                label="Results"
                :menu-props="{ transition: 'slide-y-transition' }"
              ></v-select>
            </v-col>
            <v-col cols="3" md="auto">
              <v-tooltip v-model="showABCHint" bottom>
                <template v-slot:activator="{ on }">
                  <v-btn
                    :disabled="searchCriteria.includes(abcFilter)"
                    class="mr-2"
                    color="primary"
                    @click="anythingButCovid()"
                    outlined
                    icon
                    x-large
                    v-on="on"
                  >
                    <v-icon>fas fa-user-md</v-icon>
                  </v-btn>
                </template>
                Anything But Coronavirus
              </v-tooltip>
            </v-col>
            <v-col cols="12" md="6" lg="auto">
              <v-text-field
                round
                outlined
                hint="Allows single keyword as well as AND, OR, NOT operators"
                v-model="searchTerm"
                @keypress.enter="addSearch()"
                label="Keywords"
                append-icon="mdi-magnify"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="auto">
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
          <v-card color="card" class="ml-sm-4" width="100%">
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
        <v-col class="ma-md-4" cols="auto">
          <TwitterFeed class="ml-md-4" />
        </v-col>
      </v-row>
      <br />
    </v-card>
    <ScrollButton />
  </div>
</template>
<script>
import NewsApi from "@/apis/NewsApi";
import TwitterFeed from "@/components/TwitterFeed.vue";
import ScrollButton from "@/components/ScrollButton.vue";
const newsApi = new NewsApi();

export default {
  components: {
    TwitterFeed,
    ScrollButton
  },
  created() {
    this.fetchGuardianSections();
    this.fetchArticles();
    this.fetchTldrTechNews();
  },
  data() {
    return {
      tldrUrl: "https://www.tldrnewsletter.com/latest",
      tldrTech: false,
      techNews: "",
      searchTerm: null,
      guardianSections: [{ webTitle: "" }],
      articles: [],
      currentUser: "",
      section: null,
      pageSize: 25,
      searchCriteria: [],
      searchParameter: "",
      keywordParams: [],
      sectionParams: [],
      abcFilter: {
        type: "ABC",
        text: "Anything But Coronavirus"
      },
      showABCHint: false
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
        this.guardianSections = data.response.results.filter(function(section) {
          var excludedSections = [
            "About",
            "Extra",
            "Help",
            "Info",
            "Katine",
            "Membership",
            "Search",
            "From the Observer",
            "Local",
            "Leeds",
            "Edinburgh",
            "Cardiff",
            "Better Business"
          ];
          return (
            !excludedSections.includes(section.webTitle) &&
            !section.webTitle.toLowerCase().includes("network") &&
            !section.webTitle.includes("Guardian")
          );
        });
      });
    },
    anythingButCovid() {
      this.searchCriteria.push(this.abcFilter);
    },
    fetchTldrTechNews() {
      newsApi.scrapeHTML(this.tldrUrl).then(data => {
        var span = document.createElement("span");
        span.innerHTML = data.split("Daily Update").pop();
        this.techNews = span.innerText
          .split("           ")
          .join("<br><br>")
          .split(" sponsorship page!​​​​")
          .pop()
          .split("Give feedback by ")[0]
          .split(/[(][-+]?[0-9]+ minute read[)]/g)
          .join(" - ")
          .split(")")
          .join(") - ");
      });
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
