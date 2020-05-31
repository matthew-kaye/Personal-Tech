<template>
  <div class="mb-4">
    <v-card class="ma-6" height="100%">
      <v-card-title class="primary headline">
        <span class="white--text">Canvas</span>
        <v-btn class="ml-12" primary @click="toggleGui">{{showGui?"Hide Controls":"Show Controls"}}</v-btn>
      </v-card-title>
      <div class="ma-10" @mousedown="closeGui()" @mouseup="openGui()">
        <CanvasSheet class="canvasPlayground" ref="canvasSheet" :activateGui="true" />
        <v-divider />
        <br />
        <v-card md="auto" elevation="10" width="30%">
          <v-card-title class="primary headline white--text">Instructions</v-card-title>
          <v-divider />
          <v-card-text
            style="font-size:12pt"
            class="secondary--text"
          >Click and drag to generate animations, press 'p' to pause, and space bar to generate more swirls</v-card-text>
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
      showGui: true
    };
  },
  mounted() {
    window.gui = this.$refs.canvasSheet.gui;
  },
  methods: {
    toggleGui() {
      this.showGui = !this.showGui;
      this.showGui ? window.gui.open() : this.closeGui();
    },
    closeGui() {
      window.gui.close();
    },
    openGui() {
      if (this.showGui) {
        window.gui.open();
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
::-webkit-scrollbar {
  width: 0px;
  background: transparent; /* make scrollbar transparent */
}
</style>