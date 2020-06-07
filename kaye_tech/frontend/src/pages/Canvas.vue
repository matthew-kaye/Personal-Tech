<template>
  <div class="mb-4">
    <v-card class="ma-6" height="100%">
      <v-card-title class="primary headline">
        <span class="white--text">Canvas</span>
        <v-btn icon color="white" class="ml-6" primary @click="toggleGui">
          <v-icon v-if="showGui">mdi-eye-off</v-icon>
          <v-icon v-if="!showGui">mdi-eye</v-icon>
        </v-btn>
        <v-tooltip max-width="350" v-model="showTooltip" right>
          <template v-slot:activator="{ on }">
            <v-btn icon color="white" class="ml-4" v-on="on">
              <v-icon>mdi-information-outline</v-icon>
            </v-btn>
          </template>
          <span>
            Click and drag to generate animations, and space bar to generate more swirls.
            When satisfied, press 'p' to pause, and click 'Create Photo'. It will download as fluid.png.
          </span>
        </v-tooltip>
      </v-card-title>
      <div class="ma-10" @mousedown="closeGui()" @mouseup="openGui()">
        <CanvasSheet class="canvasPlayground" ref="canvasSheet" :activateGui="true" />
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
      showTooltip: false
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
}
</style>