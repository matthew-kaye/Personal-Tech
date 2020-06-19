<template>
  <v-dialog v-model="dialog" width="1000" content-class="card" @click:outside="book=null">
    <v-scale-transition>
      <v-card flat v-if="book" color="card">
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
          <v-col cols="6">
            <v-card class="ma-4">
              <v-card-title class="primary headline">
                <span class="white--text ml-2">Description</span>
              </v-card-title>
              <div class="text--primary ml-6 mb-4 mr-4 mt-4">{{book.description}}</div>
              <v-row justify="start">
                <v-col md="auto">
                  <v-btn
                    class="ml-6 mb-4"
                    color="primary"
                    :href="book.amazon_product_url"
                  >{{ "Amazon (US)" }}</v-btn>
                </v-col>
                <v-col>
                  <v-btn class="ml-4" color="primary" :href="ukAmazonLink">{{ "Amazon (UK)" }}</v-btn>
                </v-col>
              </v-row>
            </v-card>
            <v-slide-x-transition>
              <v-card class="ma-4" v-if="reviews">
                <v-card-title class="primary headline">
                  <span class="white--text">Reviews</span>
                </v-card-title>
                <v-list>
                  <template v-for="(item, index) in reviews">
                    <v-list-item :key="index">
                      <v-list-item-content>
                        {{item.summary}}
                        <v-list-item-subtitle>
                          <a :href="item.url">See Full Review</a>
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                </v-list>
              </v-card>
            </v-slide-x-transition>
          </v-col>
        </v-row>
      </v-card>
    </v-scale-transition>
  </v-dialog>
</template>

<script>
import BookApi from "@/apis/BookApi";
const bookApi = new BookApi();
export default {
  data() {
    return {
      dialog: false,
      book: null,
      reviews: null
    };
  },
  created() {},
  computed: {
    ukAmazonLink() {
      return this.book.amazon_product_url.replace("com", "co.uk");
    }
  },
  methods: {
    toTitleCase(string) {
      return string.replace(/\w\S*/g, function(text) {
        return text.charAt(0).toUpperCase() + text.substr(1).toLowerCase();
      });
    }
  },
  watch: {
    book: {
      deep: true,
      handler() {
        if (this.book) {
          bookApi.fetchReviews(this.book.isbns[0].isbn13).then(data => {
            this.reviews = data.num_results > 0 ? data.results : null;
          });
        } else {
          this.reviews = null;
        }
      }
    }
  }
};
</script>
