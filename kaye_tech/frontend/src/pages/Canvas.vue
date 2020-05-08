<template>
  <v-card class="ma-6" height="100%">
    <v-card-title class="primary headline">
      <span class="white--text">Canvas</span>

      <v-btn color="primary" class="ml-8 mr-1" @click="refresh()">Refresh</v-btn>
    </v-card-title>
    <div width="100%" height="100%" class="ma-10">
      <CanvasSheet />
      <v-divider />
      <br />
      <v-card md="auto" elevation="10" width="20%">
        <v-card-title class="primary headline">Instructions</v-card-title>
        <v-divider />
        <v-card-text style="font-size:12pt">Press 'p' to pause</v-card-text>
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
  data() {
    return {};
  },
  computed: {},
  mounted() {},
  methods: {
    refresh() {
      window.location.reload();
    }
  }
};
</script>