<template>
  <v-card class="ma-6" v-if="book">
    <v-card-title class="primary headline">
      <span class="white--text">{{toTitleCase(book.title) + ", " + book.contributor}}</span>
    </v-card-title>
    <v-row class="ma-4" justify="start">
      <v-col md="auto">
        <v-img
          class="ma-4"
          :max-height="book.book_image_height*0.9"
          :max-width="book.book_image_width*0.9"
          :src="book.book_image"
        />
      </v-col>
      <v-col md="auto">
        <v-card class="ma-4">
          <v-card-title class="primary headline">
            <span class="white--text">Description</span>
          </v-card-title>
          <div class="text--primary ma-4">{{book.description}}</div>
          <v-row>
            <v-col>
              <v-btn
                class="ma-6"
                color="primary"
                :href="book.amazon_product_url"
              >{{ "Buy on Amazon (US)" }}</v-btn>
            </v-col>
            <v-col>
              <v-btn class="ma-6" color="primary" :href="ukAmazonLink">{{ "Buy on Amazon (UK)" }}</v-btn>
            </v-col>
          </v-row>
        </v-card>
        <v-card class="ma-4" v-if="reviews">
          <v-card-title class="primary headline">
            <span class="white--text">Reviews</span>
          </v-card-title>
          <v-list>
            <template v-for="(item, index) in reviews">
              <v-list-item :key="index">
                <v-list-item-content>
                  <v-list-item-title v-html="item.summary"></v-list-item-title>
                  <v-list-item-subtitle>
                    <a :href="item.url">See Full Review</a>
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </template>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
    <v-btn class="ma-6" color="primary" href="/books">{{ "Go Back" }}</v-btn>
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
      this.getBookFromRank();
      console.log(this.book);
      bookApi.fetchReviews(this.book.isbns[0].isbn13).then(data => {
        this.reviews = data.num_results > 0 ? data.results : null;
      });
    });
  },
  data() {
    return {
      book: null,
      books: [],
      rank: parseInt(this.$route.path.split("/").pop()),
      reviews: null
    };
  },
  computed: {
    ukAmazonLink() {
      return this.book.amazon_product_url.replace("com", "co.uk");
    }
  },
  methods: {
    getBookFromRank() {
      this.book = this.books.find(({ rank }) => rank === this.rank);
    },
    toTitleCase(string) {
      return string.replace(/\w\S*/g, function(text) {
        return text.charAt(0).toUpperCase() + text.substr(1).toLowerCase();
      });
    }
  }
};
</script>
