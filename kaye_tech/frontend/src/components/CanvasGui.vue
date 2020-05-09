<template></template>

<script>
export default {
  name: "CanvasGui",
  data() {
    return {
      show: false
    };
  },
  created() {},
  mounted() {},
  computed: {},
  methods: {
    startGUI() {
      console.log("Start GUi");
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