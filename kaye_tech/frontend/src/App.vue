<template>
  <v-app :style="{ background: $vuetify.theme.themes[theme].background }">
    <NavigationBar />
    <v-content>
      <router-view />
    </v-content>
    <br />
    <br />
    <v-footer padless>
      <v-card width="100%" class="text-right">
        <v-card-text>
          <span>
            <strong>Matthew Kaye</strong>
            - {{ new Date().getFullYear() }}
          </span>
        </v-card-text>
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
  data() {
    return {};
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
    font-size: font-size(caption);
  }
}

.header,
.footer {
  flex-shrink: 0;
}
</style>
