<template>
  <v-card class="ma-6" height="100%">
    <v-card-title class="primary headline">
      <span class="white--text">Canvas</span>
    </v-card-title>
    <div width="100%" height="100%" class="ma-10">
      <CanvasSheet ref="canvasSheet" />
      <v-divider />
      <br />
      <v-card md="auto" elevation="10" width="30%">
        <v-card-title class="primary headline white--text">Instructions</v-card-title>
        <v-divider />
        <v-card-text
          style="font-size:12pt"
          class="secondary--text"
        >Press 'p' to pause, and space bar to generate more swirls</v-card-text>
      </v-card>
    </div>
  </v-card>
</template>

<script>
import CanvasSheet from "@/components/CanvasSheet.vue";

export default {
  components: {
    CanvasSheet
  },
  created() {},
  computed: {},
  mounted() {},
  methods: {}
};
</script>