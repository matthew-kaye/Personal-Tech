<template>
  <v-card class="ma-6" height="100%">
    <v-card-title class="primary headline">
      <span class="white--text">Canvas</span>
    </v-card-title>
    <v-btn @click="toggleGui">Toggle Controls</v-btn>
    <div width="100%" height="100%" class="ma-10">
      <CanvasSheet ref="canvasSheet" :activateGui="true" />
      <v-divider />
      <br />
      <v-card md="auto" elevation="10" width="30%">
        <v-card-title class="primary headline white--text">Instructions</v-card-title>
        <v-divider />
        <v-card-text
          style="font-size:12pt"
          class="secondary--text"
        >Press 'p' to pause, and space bar to generate more swirls</v-card-text>
      </v-card>
    </div>
  </v-card>
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
    this.gui = this.$refs.canvasSheet.gui;
  },
  methods: {
    toggleGui() {
      if (this.showGui) {
        this.gui.close();
        this.gui.end();
        this.showGui = false;
      } else {
        this.gui.open();
        this.showGui = true;
      }
    }
  }
};
</script>