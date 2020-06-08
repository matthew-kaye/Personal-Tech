<template>
  <v-dialog v-model="dialog" content-class="card" max-width="700px">
    <v-card color="card">
      <v-card-title class>
        <b>About</b>
      </v-card-title>
      <v-divider />
      <v-row justify="space-around">
        <v-col md="auto">
          <v-avatar left size="100" class="mt-5 ml-6">
            <img src="/static/frontend/matt.jpg" />
          </v-avatar>
        </v-col>
        <v-col class="ml-n4 mr-4">
          <v-card-text style="text-align:justify;">
            Hello! If we haven't already met, my name's Matt, and I work as a Software Engineer at Brainlabs.
            I've generally been more comfortable with backend programming, and was keen to make the most of this "unprecedented" time on furlough and improve my web skills, so built this website!
            If you have any ideas for cool things to add to the site (or find a bug!), then
            <a
              href="mailto:matt-website-queries@outlook.com?subject=Website Feedback"
            >
              <b>let me know!</b>
            </a>
          </v-card-text>
        </v-col>
      </v-row>
      <v-row class="ml-1">
        <v-col style="text-align: center;">
          <v-card-text>
            <span class="headline">
              <b>Details</b>
            </span>
            <br />
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
        <v-col>
          <div>
            <v-img
              class="ml-12 mt-2 logo"
              max-height="200"
              max-width="200"
              src="/static/frontend/k-logo.jpg"
            />
          </div>
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
<style>
.logo:hover {
  animation: shake 0.5s;
  animation-iteration-count: infinite;
}
@keyframes shake {
  0% {
    transform: translate(1px, 1px) rotate(0deg);
  }
  10% {
    transform: translate(-1px, -2px) rotate(-1deg);
  }
  20% {
    transform: translate(-3px, 0px) rotate(1deg);
  }
  30% {
    transform: translate(3px, 2px) rotate(0deg);
  }
  40% {
    transform: translate(1px, -1px) rotate(1deg);
  }
  50% {
    transform: translate(-1px, 2px) rotate(-1deg);
  }
  60% {
    transform: translate(-3px, 1px) rotate(0deg);
  }
  70% {
    transform: translate(3px, 1px) rotate(-1deg);
  }
  80% {
    transform: translate(-1px, -1px) rotate(1deg);
  }
  90% {
    transform: translate(1px, 2px) rotate(0deg);
  }
  100% {
    transform: translate(1px, -2px) rotate(-1deg);
  }
}
</style>