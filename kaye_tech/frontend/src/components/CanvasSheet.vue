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
      render: false,
      scripts: []
    };
  },
  created() {
    this.removeScripts();
    var scripts = document.querySelectorAll("script");
    for (var i = 0; i < scripts.length; i++) {
      this.scripts.push(scripts[i].src);
    }
    this.scripts = this.scripts.length > 0 ? this.scripts : [];
    this.addScriptIfNotDuplicate("/static/canvas/dat.gui.min.js");
    this.addScriptIfNotDuplicate("/static/canvas/script.js");
  },
  mounted() {},
  computed: {},
  methods: {
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
      while (elem) {
        elem.parentNode.removeChild(elem);
        var elem = document.querySelector("script");
      }
      var elem = document.querySelector("script");
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