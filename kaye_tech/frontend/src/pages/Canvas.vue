<template>
  <div class="mb-4">
    <v-card class="ma-6" height="100%">
      <v-card-title class="primary headline">
        <span class="white--text">Canvas</span>
        <v-btn class="ml-12" primary @click="toggleGui">Toggle Controls</v-btn>
      </v-card-title>
      <div class="ma-10">
        <CanvasSheet class="canvasPlayground" ref="canvasSheet" :activateGui="true" />
        <v-divider />
        <br />
        <v-card md="auto" elevation="10" width="30%">
          <v-card-title class="primary headline white--text">Instructions</v-card-title>
          <v-divider />
          <v-card-text
            style="font-size:12pt"
            class="secondary--text"
          >Press 'p' to pause, and space bar to generate more swirls. Currently broken on Chrome v83.</v-card-text>
        </v-card>
        <br />
      </div>
    </v-card>
  </div>
</template>

<script>
import CanvasSheet from "@/components/CanvasSheet.vue";

export default {
  components: {
    CanvasSheet
  },
  data() {
    return {
      showGui: true,
      gui: {}
    };
  },
  mounted() {
    window.gui = this.$refs.canvasSheet.gui;
  },
  methods: {
    toggleGui() {
      if (this.showGui) {
        window.gui.close();
        this.showGui = false;
      } else {
        window.gui.open();
        this.showGui = true;
      }
    }
  }
};
</script>
<style module lang="scss">
.canvasPlayground {
  margin: 0;
  position: relative;
  width: 100%;
  height: 100%;
}
</style>