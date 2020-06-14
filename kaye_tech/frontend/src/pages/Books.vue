<template>
  <div>
    <v-card class="ma-4" v-if="books.length>0">
      <v-card-title class="primary headline">
        <span class="white--text">{{"New York Times Bestsellers - updated " + time +"s ago"}}</span>
      </v-card-title>
      <v-data-table :headers="headers" :items="books">
        <template v-slot:item="row">
          <tr v-bind:style="{ cursor: 'pointer' }" @click="viewBook(row.item)">
            <td>{{ row.item.rank }}</td>
            <td>
              <v-row justify="start" align="center" class="ma-n1">
                <v-col md="auto">
                  <v-img contain height="40" max-width="25" :src="row.item.book_image">
                    <template v-slot:placeholder>
                      <v-row class="fill-height ma-0" align="center" justify="center">
                        <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                      </v-row>
                    </template>
                  </v-img>
                </v-col>
                <v-col md="auto">{{ toTitleCase(row.item.title) }}</v-col>
              </v-row>
            </td>
            <td>{{ row.item.author }}</td>
            <td>{{ row.item.weeks_on_list }}</td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
    <BookDialog ref="bookDialog" />
  </div>
</template>
<script>
import BookApi from "@/apis/BookApi";
import BookDialog from "@/components/BookDialog";
const bookApi = new BookApi();

export default {
  components: {
    BookDialog
  },
  created() {
    bookApi.fetchBooks().then(data => {
      this.books = data.results.books;
    });
    var interval = setInterval(this.incrementTime, 1000);
  },
  data() {
    return {
      searchTerm: "",
      books: [],
      time: 0
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
      this.$refs.bookDialog.book = item;
      this.$refs.bookDialog.dialog = true;
    },
    incrementTime() {
      this.time = parseInt(this.time) + 1;
    }
  }
};
</script>
