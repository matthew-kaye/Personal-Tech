<template>
  <v-dialog v-model="dialog" content-class="card" max-width="700px">
    <v-card color="card">
      <v-card-title class>
        <b>About</b>
      </v-card-title>
      <v-divider />
      <v-row>
        <v-col md="auto">
          <v-avatar size="100" class="mt-5 ml-4">
            <img src="/static/frontend/matt.jpg" />
          </v-avatar>
        </v-col>
        <v-col>
          <v-card-text>
            Hello! If we haven't already met, my name's Matt, and I work as a Software Engineer at Brainlabs.
            I've generally been more comfortable with backend programming, and was keen to make the most of this "unprecedented" time on furlough and improve my web skills, so built this website!
            If you have any ideas for cool things to add to the site (or bugs you've found), then
            <a
              href="mailto:m.kaye@outlook.com"
            >let me know!</a>
          </v-card-text>
          <v-card-title>
            <b>Techy Stuff</b>
          </v-card-title>
          <v-card-text>
            <b>Web Frameworks:</b> Vue.js, Django
            <br />
            <b>Frontend Libraries:</b> Vuetify
            <br />
            <b>Internal APIs:</b> Django Rest Framework
            <br />
            <b>Package Management:</b> Node.js, Webpack
            <br />
            <b>Container:</b> Docker
            <br />
            <b>Hosting:</b> DigitalOcean
            <br />
            <b>Domain routing:</b> GoDaddy, Nginx
            <br />
          </v-card-text>
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false
    };
  }
};
</script>
