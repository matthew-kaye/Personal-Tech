<template>
  <div>
    <v-card-title class="headline">
      <span>
        <b>Options:</b>
      </span>
      <v-tooltip v-model="showToggleGuiHint" bottom>
        <template v-slot:activator="{ on }">
          <v-btn large v-on="on" icon class="ml-6" primary @click="toggleGui">
            <v-icon v-if="showGui">mdi-eye-off</v-icon>
            <v-icon v-if="!showGui">mdi-eye</v-icon>
          </v-btn>
        </template>
        Toggle Controls
      </v-tooltip>
      <v-tooltip v-model="showFullscreenHint" bottom>
        <template v-slot:activator="{ on }">
          <v-btn label="Fullscreen" v-on="on" icon class="ml-6" primary @click="goFullscreen">
            <v-icon large>mdi-fullscreen</v-icon>
          </v-btn>
        </template>
        Fullscreen
      </v-tooltip>
      <v-tooltip v-model="showToggleWidescreenHint" bottom>
        <template v-slot:activator="{ on }">
          <v-btn large icon v-on="on" class="ml-6" primary @click="toggleWidescreen">
            <v-icon v-if="fullscreen">mdi-arrow-collapse-all</v-icon>
            <v-icon v-if="!fullscreen">mdi-arrow-expand-all</v-icon>
          </v-btn>
        </template>
        Toggle Widescreen
      </v-tooltip>
      <v-tooltip v-model="showRefreshHint" bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" large icon class="ml-6" primary @click="refreshPage">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </template>
        Refresh (reset defaults)
      </v-tooltip>
      <v-tooltip v-model="showPauseHint" bottom>
        <template v-slot:activator="{ on }">
          <v-btn
            large
            v-on="on"
            icon
            class="ml-6"
            primary
            @click="$refs.canvasSheet.config.PAUSED=!$refs.canvasSheet.config.PAUSED"
          >
            <v-icon>mdi-play-pause</v-icon>
          </v-btn>
        </template>
        Pause/Resume (also 'p')
      </v-tooltip>
      <v-tooltip v-model="showSplatHint" bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" large icon class="ml-6" primary @click="$root.$emit('randomSplat')">
            <v-icon>mdi-flower-poppy</v-icon>
          </v-btn>
        </template>
        Splat
      </v-tooltip>
      <v-tooltip max-width="350" v-model="showInfoTooltip" bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon class="ml-6" v-on="on">
            <v-icon>mdi-information</v-icon>
          </v-btn>
        </template>
        <span>
          Click and drag to generate animations, and space bar to generate more splats.
          When satisfied, pause, and click 'Create Photo/Download Photo' to download, or right click to copy and paste.
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
      showInfoTooltip: false,
      showFullscreenHint: false,
      showToggleGuiHint: false,
      showToggleWidescreenHint: false,
      showRefreshHint: false,
      showSplatHint: false,
      showPauseHint: false,
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
    goFullscreen() {
      const canvas = document.getElementById("fluids");
      canvas.requestFullscreen();
    },
    toggleWidescreen() {
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
    },
    refreshPage() {
      location.reload();
    }
  },
  computed: {
    computedMargin() {
      return `ma-${this.fullscreen ? 0 : 8}`;
    }
  },
  watch: {
    // quality: function() {
    // }
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