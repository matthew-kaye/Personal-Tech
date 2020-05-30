<template>
  <v-dialog v-model="dialog" max-width="700px">
    <v-card color="card">
      <v-card-title class="mb-2">About</v-card-title>
      <v-divider />
      <v-card-text>
        <v-row>
          <v-col md="auto">
            <v-avatar size="100" class="mt-1">
              <img src="/static/frontend/matt.jpg" />
            </v-avatar>
          </v-col>
          <v-col>
            Hello! If we haven't already met, my name's Matt, and I'm currently working as a Software Engineer at Brainlabs.
            Having generally been more comfortable with backend-focused tools, I was keen to make the most of this "unprecedented" time on furlough and improve on my frontend, so built this website!
            It uses Vue.js/Vuetify for the frontend, and a Python/Django backend, hosted on a DigitalOcean server using Docker and Nginx.
            If you have any suggestions for cool things to add to the site (or bugs you've found), then drop me a line!
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: true
    };
  },
  computed: {},
  props: {
    dialogMode: String
  },
  methods: {
    open() {
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    }
  }
};
</script>
