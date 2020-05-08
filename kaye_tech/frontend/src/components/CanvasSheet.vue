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
      var scriptObject = scripts[i];
      this.scripts.push(scripts[i].src);
    }
  },
  mounted() {
    window.ga =
      window.ga ||
      function() {
        (ga.q = ga.q || []).push(arguments);
      };
    ga.l = +new Date();
    ga("create", "UA-105392568-1", "auto");
    ga("send", "pageview");
    this.addScriptIfNotDuplicate("/static/canvas/dat.gui.min.js");
    this.addScriptIfNotDuplicate("/static/canvas/script.js");
  },
  methods: {
    addScriptIfNotDuplicate(source) {
      const plugin = document.createElement("script");
      if (!this.scripts.includes(source)) {
        plugin.setAttribute("src", source);
        document.head.appendChild(plugin);
        plugin.async = true;
        this.scripts.push(source);
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