<template>
  <v-fab-transition>
    <div @click="overlay = false" class="text-center">
      <FluidsSheet :homePage="true" class="homeCanvas"></FluidsSheet>
      <v-overlay width="100%" height="100%" :value="overlay" style="cursor: pointer;">
        <span style="font-size:64pt">{{welcomeMessage}}</span>
        <br />
        <span>Click me.</span>
      </v-overlay>
    </div>
  </v-fab-transition>
</template>
<script>
import FluidsSheet from "@/components/FluidsSheet.vue";
import AccountsApi from "@/apis/AccountsApi";
const accountsApi = new AccountsApi();
export default {
  components: {
    FluidsSheet
  },
  created() {
    accountsApi.getCurrentUser().then(data => {
      this.currentUser = data;
      this.overlay = true;
    });
    window.activeGui = false;
  },
  data() {
    return {
      overlay: false,
      currentUser: ""
    };
  },
  computed: {
    dark() {
      return this.$vuetify.theme.dark ? "dark" : "light";
    },
    welcomeMessage() {
      return this.currentUser.first_name
        ? `Hello ${this.currentUser.first_name}!`
        : `Hello!`;
    }
  }
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