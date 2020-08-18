<template>
  <v-dialog v-model="dialog" content-class="card" max-width="700px">
    <v-card color="card">
      <v-card-title class>
        <b>About</b>
        <v-btn class="ma-5 hidden-md-and-up" fixed top right icon @click="dialog=false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-divider />
      <v-row justify="space-around">
        <v-col cols="12" md="auto" align="center">
          <v-avatar left size="100" class="mt-5 ml-sm-6">
            <img src="/static/frontend/matt.jpg" />
          </v-avatar>
        </v-col>
        <v-col class="ml-md-n4 ml-4 mr-4">
          <v-card-text>
            Hello! My name's Matt, and I work as a Software Engineer at Brainlabs.
            During the Covid-19 lockdown I was keen to improve my web skills, so built this as a place to showcase them with a variety of interesting content (to me anyway!),
            with everything from news to fluid simulations, games, and even my highly-debated burrito rankings.
            If you have any ideas for cool things to add to the site (or find a bug!), then
            <a
              href="mailto:matt-website-queries@outlook.com?subject=Website Feedback"
            >
              <b>let me know!</b>
            </a>
          </v-card-text>
        </v-col>
      </v-row>
      <v-row class="ml-1 mt-n6" align="center" justify="center">
        <v-col cols="12" md="auto" style="text-align: center;">
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
        <v-col cols="12" md="auto" align="center">
          <div>
            <v-img
              class="ml-md-12 mt-2 logo"
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
  cursor: grab;
}
.logo:active {
  animation: shake 0.1s;
  animation-iteration-count: infinite;
  cursor: grabbing;
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
