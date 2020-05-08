<template>
  <div>
    <v-card class="ma-6" v-if="burrito">
      <v-btn class="ma-6" color="primary" href="/burritos">{{ "Go Back" }}</v-btn>
    </v-card>
    <v-speed-dial
      v-model="fab"
      bottom
      right
      direction="top"
      transition="slide-y-reverse-transition"
      fixed
      class="mb-12 mr-4"
    >
      <template v-slot:activator>
        <v-btn v-model="fab" fab color="primary">
          <v-icon v-if="fab">mdi-close</v-icon>
          <v-icon v-else>mdi-chevron-up</v-icon>
        </v-btn>
      </template>
      <v-btn fab dark small color="primary" @click="console.log('add')">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
      <v-btn fab dark small color="green" @click="console.log('edit')">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn fab dark small color="red" @click="console.log('delete')">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-speed-dial>
  </div>
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
      fab: true,
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
