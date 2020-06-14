<template>
  <div>
    <v-card-title class="headline" align="start">
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
            @click="$refs.fluidsSheet.config.PAUSED=!$refs.fluidsSheet.config.PAUSED"
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
      <v-menu bottom :close-on-content-click="false">
        <template v-slot:activator="{ on: menu, attrs }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn large class="ml-6" icon v-bind="attrs" v-on="{ ...tooltip, ...menu }">
                <v-icon class="mt-1" large>mdi-format-color-fill</v-icon>
              </v-btn>
            </template>
            <span>Adjust Background Colour</span>
          </v-tooltip>
        </template>
        <v-color-picker
          swatches-max-height="10"
          width="300"
          canvas-height="180"
          hide-mode-switch
          v-model="backgroundColour"
        ></v-color-picker>
      </v-menu>
      <v-menu bottom :close-on-content-click="false">
        <template v-slot:activator="{ on: menu, attrs }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn large class="ml-6" icon v-bind="attrs" v-on="{ ...tooltip, ...menu }">
                <v-icon large>mdi-brush</v-icon>
              </v-btn>
            </template>
            <span>Override Splat Colour</span>
          </v-tooltip>
        </template>
        <v-color-picker
          swatches-max-height="10"
          canvas-height="180"
          width="300"
          hide-mode-switch
          v-model="splatColour"
        ></v-color-picker>
        <v-btn width="300" large @click="splatRgb={ r: 0, g: 0, b: 0 }">Reset</v-btn>
      </v-menu>
      <v-tooltip v-model="toggleDragButtonhint" bottom>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" large icon class="ml-6" @click="toggleContinuous">
            <v-icon v-if="continuous">mdi-cursor-default-click</v-icon>
            <v-icon v-if="!continuous">mdi-cursor-default-click-outline</v-icon>
          </v-btn>
        </template>
        Toggle Animating on Mouse Hover
        <span></span>
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
      <FluidsSheet class="canvasPlayground" ref="fluidsSheet" :activateGui="true" />
    </div>
  </div>
</template>

<script>
import FluidsSheet from "@/components/FluidsSheet.vue";

export default {
  components: {
    FluidsSheet
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
      rgb: { r: 0, g: 0, b: 0 },
      splatRgb: { r: 0, g: 0, b: 0 },
      colourPicker: false,
      backgroundColourHint: false,
      splatColourHint: false,
      toggleDragButtonhint: false,
      fullscreen: false,
      continuous: false
    };
  },
  mounted() {
    window.gui = this.$refs.fluidsSheet.gui;
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
    toggleContinuous() {
      this.continuous = !this.continuous;
      this.$refs.fluidsSheet.config.CONTINUOUS = this.continuous;
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
    },
    backgroundColour: {
      get() {
        return this.rgb;
      },
      set(v) {
        this.rgb = v;
      }
    },
    splatColour: {
      get() {
        return this.splatRgb;
      },
      set(v) {
        this.splatRgb = v;
      }
    }
  },
  watch: {
    rgb: function() {
      this.$root.$emit("changeBackground", this.rgb);
    },
    splatRgb: function() {
      this.$root.$emit("overrideSplatColour", this.splatRgb);
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