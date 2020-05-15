<template>
  <v-dialog v-model="visible" persistent max-width="350px" @click:outside="emitNo">
    <v-card>
      <v-card-title class="primary headline">Warning!</v-card-title>
      <br />
      <v-card-text class="white--text">Are you sure you want to delete this vendor?</v-card-text>
      <v-card-actions>
        <v-btn color="primary" text @click="emitNo">No</v-btn>
        <v-btn color="primary" text @click="emitYes">Yes</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  computed: {
    visible() {
      return this.dialog;
    }
  },
  data() {
    return {};
  },
  props: {
    dialog: Boolean
  },
  methods: {
    emitYes() {
      this.$emit("yes");
    },
    emitNo() {
      this.$emit("no");
    }
  }
};
</script>
