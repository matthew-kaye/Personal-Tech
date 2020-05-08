<template>
  <div>
    <canvas></canvas>
  </div>
</template>

<script>
export default {
  name: "CanvasSheet",
  data() {
    return {
      scripts: []
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

    const guiPlugin = document.createElement("script");
    guiPlugin.setAttribute("src", "/static/canvas/dat.gui.min.js");
    if (!this.scripts.includes(guiPlugin.src)) {
      document.head.appendChild(guiPlugin);
      guiPlugin.async = true;
      this.scripts.push(guiPlugin.src);
    }
    const scriptPlugin = document.createElement("script");
    scriptPlugin.setAttribute("src", "/static/canvas/script.js");
    if (!this.scripts.includes(scriptPlugin.src)) {
      document.head.appendChild(scriptPlugin);
      scriptPlugin.async = true;
      this.scripts.push(scriptPlugin.src);
    }
  },
  computed: {}
};
</script>
<style module lang="scss">
canvas {
  width: 100%;
  height: 100%;
}
</style>