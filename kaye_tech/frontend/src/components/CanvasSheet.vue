<template>
  <div>
    <canvas></canvas>
  </div>
</template>

<script>
export default {
  name: "CanvasSheet",
  data() {
    var background = this.$vuetify.theme.dark ? 0 : 255;
    return {
      canvasConfig: {
        SIM_RESOLUTION: 128,
        DYE_RESOLUTION: 1024,
        CAPTURE_RESOLUTION: 512,
        DENSITY_DISSIPATION: 1,
        VELOCITY_DISSIPATION: 0.2,
        PRESSURE: 0.8,
        PRESSURE_ITERATIONS: 20,
        CURL: 30,
        SPLAT_RADIUS: 0.25,
        SPLAT_FORCE: 6000,
        SHADING: true,
        COLORFUL: true,
        COLOR_UPDATE_SPEED: 10,
        PAUSED: false,
        BACK_COLOR: { r: background, g: background, b: background },
        TRANSPARENT: false,
        BLOOM: true,
        BLOOM_ITERATIONS: 8,
        BLOOM_RESOLUTION: 256,
        BLOOM_INTENSITY: 0.8,
        BLOOM_THRESHOLD: 0.6,
        BLOOM_SOFT_KNEE: 0.7,
        SUNRAYS: true,
        SUNRAYS_RESOLUTION: 196,
        SUNRAYS_WEIGHT: 1.0
      }
    };
  },
  created() {
    this.refreshScripts();
    window.canvasConfig = this.canvasConfig;
  },
  mounted() {},
  computed: {
    scripts() {
      var scripts = [];
      for (var script of document.querySelectorAll("script")) {
        scripts.push(script.src);
      }
      return scripts;
    }
  },
  methods: {
    refreshScripts() {
      this.removeScripts();
      this.addScriptIfNotDuplicate("/static/canvas/dat.gui.min.js");
      this.addScriptIfNotDuplicate("/static/canvas/script.js");
    },
    addScriptIfNotDuplicate(source) {
      const plugin = document.createElement("script");
      plugin.setAttribute("src", source);
      if (!this.scripts.includes(plugin.src)) {
        document.head.appendChild(plugin);
        plugin.async = true;
        this.scripts.push(plugin.src);
      }
    },
    removeScripts() {
      var elem = document.querySelector("script");
      for (var script of document.querySelectorAll("script")) {
        if (script.src.includes("/static/canvas/script.js")) {
          script.parentNode.removeChild(script);
        }
      }
    }
  }
};
</script>
<style module lang="scss">
canvas {
  width: 100%;
  height: 100%;
}
</style>