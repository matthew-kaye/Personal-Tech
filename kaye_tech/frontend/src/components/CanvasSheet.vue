<template>
  <div>
    <canvas></canvas>
  </div>
</template>

<script>
export default {
  name: "CanvasSheet",
  created() {
    window.ga =
      window.ga ||
      function() {
        (ga.q = ga.q || []).push(arguments);
      };
    ga.l = +new Date();
    ga("create", "UA-105392568-1", "auto");
    ga("send", "pageview");
  },
  mounted() {
    const guiPlugin = document.createElement("script");
    guiPlugin.setAttribute("src", "/static/dat.gui.min.js");
    guiPlugin.async = true;
    document.head.appendChild(guiPlugin);

    const scriptPlugin = document.createElement("script");
    scriptPlugin.setAttribute("src", "/static/script.js");
    scriptPlugin.async = true;
    document.head.appendChild(scriptPlugin);
  }
};
</script>
<style module lang="scss">
canvas {
  width: 100%;
  height: 100%;
}
</style>