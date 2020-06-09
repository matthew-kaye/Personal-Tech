<template>
  <div>
    <v-card-title class="headline">
      <span>
        <b>Controls:</b>
      </span>
      <v-btn icon class="ml-6" primary @click="toggleGui">
        <v-icon v-if="showGui">mdi-eye-off</v-icon>
        <v-icon v-if="!showGui">mdi-eye</v-icon>
      </v-btn>
      <v-btn icon class="ml-6" primary @click="toggleFullscreen">
        <v-icon v-if="fullscreen">mdi-fullscreen-exit</v-icon>
        <v-icon v-if="!fullscreen">mdi-fullscreen</v-icon>
      </v-btn>
      <v-tooltip max-width="350" v-model="showTooltip" right>
        <template v-slot:activator="{ on }">
          <v-btn icon class="ml-4" v-on="on">
            <v-icon>mdi-information</v-icon>
          </v-btn>
        </template>
        <span>
          Click and drag to generate animations, and space bar to generate more swirls.
          When satisfied, press 'p' to pause, and click 'Create Photo'. It will download as fluid.png.
        </span>
      </v-tooltip>
    </v-card-title>
    <v-divider />
    <div :class="[computedMargin]" @mousedown="closeGui()" @mouseup="openGui()">
      <CanvasSheet class="canvasPlayground" ref="canvasSheet" :activateGui="true" />
    </div>
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
      showTooltip: false,
      fullscreen: false
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
    toggleFullscreen() {
      this.fullscreen = !this.fullscreen;
      this.$root.$emit("toggleFooter", this.fullscreen);
      if (this.fullscreen) {
        window.scrollTo(0, document.body.scrollHeight);
      }
    },
    closeGui() {
      window.gui.close();
    },
    openGui() {
      if (this.showGui) {
        window.gui.open();
      }
    }
  },
  computed: {
    computedMargin() {
      return `ma-${this.fullscreen ? 0 : 8}`;
    }
  }
};
</script>
<style module lang="scss">
.canvasPlayground {
  margin: 0;
  position: relative;
  width: 100%;
  height: 100vh;
}
::-webkit-scrollbar {
  width: 0px;
}
</style>