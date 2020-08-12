<template>
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
</template>
<script>
import NewsApi from "@/apis/NewsApi";
import TwitterFeed from "@/components/TwitterFeed.vue";
import ScrollButton from "@/components/ScrollButton.vue";
const newsApi = new NewsApi();

export default {
  created() {
    window.addEventListener("scroll", this.onScroll);
  },
  destroyed() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  data() {
    return {
      offsetTop: 0
    };
  },
  methods: {
    onScroll(e) {
      this.offsetTop = e.target.scrollingElement.scrollTop;
    }
  }
};
</script>

