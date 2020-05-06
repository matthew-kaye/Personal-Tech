<template>
  <v-card class="ma-6" v-if="burrito">
    <v-btn class="ma-6" color="primary" href="/burritos">{{ "Go Back" }}</v-btn>
  </v-card>
</template>

<script>
import burritoApi from "@/apis/burritoApi";
const burritoApi = new BurritoApi();

export default {
  components: {},
  created() {
    burritoApi.fetchburritos().then(data => {
      console.log(data);
    });
  },
  data() {
    return {
      burrito: null,
      burritos: [],
      id: parseInt(this.$route.path.split("/").pop()),
      reviews: null
    };
  },
  computed: {},
  methods: {
    getBurritoFromId() {
      return;
    }
  }
};
</script>
