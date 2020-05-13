<template>
  <v-app :style="{ background: $vuetify.theme.themes[theme].background }">
    <NavigationBar />
    <v-content>
      <router-view />
      <v-btn absolute bottom left v-if="!footer" @click="footer=true" icon>
        <v-icon>mdi-arrow-up</v-icon>
      </v-btn>
    </v-content>
    <v-footer padless height="52" v-show="footer" class="text-right">
      <v-card width="100%" height="52" v-if="footer">
        <div class="mt-2" color="card">
          <v-btn @click="footer=false" icon bottom left absolute>
            <v-icon>mdi-arrow-down</v-icon>
          </v-btn>
          <span class="secondary--text">
            <strong>
              Matthew Kaye
              - {{ new Date().getFullYear() }}
            </strong>
          </span>
          <v-btn
            class="mb-2 ml-2 mr-4"
            icon
            href="https://www.linkedin.com/in/matthew-kaye-20332016a/"
          >
            <v-icon>mdi-linkedin</v-icon>
          </v-btn>
        </div>
      </v-card>
    </v-footer>
  </v-app>
</template>
<script>
import NavigationBar from "./components/NavigationBar.vue";

export default {
  name: "app",
  components: {
    NavigationBar
  },
  created() {
    if (window.location.href.includes("dark")) {
      this.$vuetify.theme.dark =
        window.location.href.split("dark=").pop() == "true";
    } else {
      this.$vuetify.theme.dark = true;
    }
  },
  data() {
    return {
      footer: true
    };
  },
  computed: {
    theme() {
      return this.$vuetify.theme.dark ? "dark" : "light";
    }
  }
};
</script>

<style module lang="scss">
.container {
  align-items: stretch;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.content {
  flex-grow: 1;
  margin: 0 0 spacing-vertical() 0;
}
.footer {
  background: background-color(content);
  border-top: border-width() solid border-color();
  padding: spacing-vertical(compact) 0;
  text-align: right;
  width: 100%;
  p {
    color: color(text, muted);
    font-size: 11;
  }
}
.header,
.footer {
  flex-shrink: 0;
}
</style>
