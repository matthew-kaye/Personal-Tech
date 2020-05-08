<template>
  <div @click="overlay = false">
    <CanvasSheet></CanvasSheet>
    <v-overlay width="100%" height="100%" :value="overlay">
      <v-lazy transition="slide-x-transition">
        <span style="font-size:64pt">{{welcomeMessage}}</span>
      </v-lazy>
      <v-btn top right absolute fab icon class="mr-n12 mx-auto" @click="overlay = false">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-overlay>
  </div>
</template>

<script>
import CanvasSheet from "@/components/CanvasSheet.vue";
import AccountsApi from "@/apis/AccountsApi";
const accountsApi = new AccountsApi();
export default {
  components: {
    CanvasSheet
  },
  created() {
    accountsApi.getCurrentUser().then(data => {
      this.currentUser = data;
    });
  },
  data() {
    return {
      overlay: true,
      currentUser: ""
    };
  },
  computed: {
    welcomeMessage() {
      return this.currentUser.first_name
        ? `Hello ${this.currentUser.first_name}!`
        : `Hello!`;
    }
  },
  methods: {}
};
</script>
