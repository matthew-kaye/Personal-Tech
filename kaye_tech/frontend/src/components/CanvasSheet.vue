<template>
  <div>
    <canvas></canvas>
  </div>
</template>

<script>
import Vue from "vue";
export default {
  name: "CanvasSheet",
  data() {
    return {
      scripts: [],
      render: false
    };
  },
  created() {
    var scripts = document.querySelectorAll("script");
    for (var i = 0; i < scripts.length; i++) {
      this.scripts.push(scripts[i].src);
    }

    this.addScriptIfNotDuplicate("/static/canvas/dat.gui.min.js");
    this.addScriptIfNotDuplicate("/static/canvas/script.js");
  },
  mounted() {},
  methods: {
    addScriptIfNotDuplicate(source) {
      const plugin = document.createElement("script");
      plugin.setAttribute("src", source);
      if (!this.scripts.includes(plugin.src)) {
        document.head.appendChild(plugin);
        plugin.async = true;
        this.scripts.push(plugin.src);
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