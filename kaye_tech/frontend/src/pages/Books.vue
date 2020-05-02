<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">New York Times Bestsellers</span>
    </v-card-title>
    <v-card class="ma-4" color="card">
      <v-data-table :headers="headers" :items="books">
        <template v-slot:item="row">
          <tr v-bind:style="{ cursor: 'pointer' }">
            <td>
              <p>{{ row.item.rank }}</p>
            </td>
            <td>
              <p>{{ toTitleCase(row.item.title) }}</p>
            </td>
            <td>
              <p>{{ row.item.author }}</p>
            </td>
            <td>
              <p>{{ row.item.weeks_on_list }}</p>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
    <br />
  </v-card>
</template>
<script>
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default {
  components: {},
  created() {
    this.fetchBooks();
  },
  data() {
    return {
      listUrl:
        "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json",
      reviewUrl: "https://api.nytimes.com/svc/books/v3/reviews.json",
      nytApiKey: "XF7JacilFFCdHR6kKTSESVYB220aKanS",
      searchTerm: "",
      books: []
    };
  },
  computed: {
    headers() {
      return [
        {
          text: "Rank",
          width: 1
        },
        {
          text: "Title",
          width: 2
        },
        {
          text: "Author",
          width: 2
        },
        {
          text: "Weeks on list",
          width: 2
        }
      ];
    }
  },
  methods: {
    fetchBooks() {
      var response = axios
        .get(this.listUrl, {
          params: {
            "api-key": this.nytApiKey
          },
          headers: { Accept: "application/json" }
        })
        .then(response => response.data)
        .catch(error => console.log(error));
      response.then(data => {
        this.books = data.results.books;
      });
    },
    toTitleCase(string) {
      return string.replace(/\w\S*/g, function(text) {
        return text.charAt(0).toUpperCase() + text.substr(1).toLowerCase();
      });
    }
  }
};
</script>
