<template>
  <div @click="overlay = false">
    <CanvasSheet class="homeCanvas"></CanvasSheet>
    <v-overlay width="100%" height="100%" :value="overlay">
      <span style="font-size:64pt">{{welcomeMessage}}</span>
      <br />
      <span>*Click and drag to generate animations</span>
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
    window.activeGui = false;
  },
  data() {
    return {
      overlay: true,
      currentUser: ""
    };
  },
  computed: {
    dark() {
      return this.$vuetify.theme.dark ? "dark" : "light";
    },
    welcomeMessage() {
      return this.currentUser.first_name
        ? `Hello ${this.currentUser.first_name}!*`
        : `Hello!*`;
    }
  },
  methods: {}
};
</script>
<style module lang="scss">
canvas {
  margin: 0;
  width: 100%;
  height: 100%;
}
.homeCanvas {
  position: absolute;
  width: 100%;
  height: 100%;
}
</style>