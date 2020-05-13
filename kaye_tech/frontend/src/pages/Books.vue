<template>
  <v-card class="ma-6">
    <v-card-title class="primary headline">
      <span class="white--text">New York Times Bestsellers</span>
    </v-card-title>
    <v-card class="ma-4" color="card">
      <v-data-table :headers="headers" :items="books">
        <template v-slot:item="row">
          <tr v-bind:style="{ cursor: 'pointer' }" @click="viewBook(row.item)">
            <td>
              <p>{{ row.item.rank }}</p>
            </td>
            <td>
              <v-row justify="start" align="center">
                <v-col md="auto">
                  <v-img max-height="40" max-width="25" :src="row.item.book_image" />
                </v-col>
                <v-col md="auto">
                  <p>{{ toTitleCase(row.item.title) }}</p>
                </v-col>
              </v-row>
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
import BookApi from "@/apis/BookApi";
const bookApi = new BookApi();

export default {
  components: {},
  created() {
    bookApi.fetchBooks().then(data => {
      this.books = data.results.books;
    });
  },
  data() {
    return {
      searchTerm: "",
      books: []
    };
  },
  computed: {
    headers() {
      return [
        {
          text: "Rank",
          value: "rank",
          width: 1
        },
        {
          text: "Title",
          value: "title",
          width: 2
        },
        {
          text: "Author",
          value: "author",
          width: 2
        },
        {
          text: "Weeks on list",
          value: "weeks_on_list",
          width: 2
        }
      ];
    }
  },
  methods: {
    toTitleCase(string) {
      return string.replace(/\w\S*/g, function(text) {
        return text.charAt(0).toUpperCase() + text.substr(1).toLowerCase();
      });
    },
    viewBook(item) {
      this.$router.push("/book/" + item.rank);
    }
  }
};
</script>
