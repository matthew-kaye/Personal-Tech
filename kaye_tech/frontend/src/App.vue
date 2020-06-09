<template>
  <v-app :style="{ background: $vuetify.theme.themes[theme].background }">
    <v-expand-transition>
      <NavigationBar />
    </v-expand-transition>
    <v-content>
      <v-slide-y-reverse-transition :hide-on-leave="true">
        <router-view />
      </v-slide-y-reverse-transition>
      <v-btn absolute bottom left v-if="!footer" @click="footer=true" icon>
        <v-icon>mdi-chevron-up</v-icon>
      </v-btn>
    </v-content>
    <v-footer padless height="52" v-show="footer" class="text-right">
      <v-card width="100%" height="52">
        <div class="mt-2" color="card">
          <v-btn @click="footer=false" icon bottom left absolute>
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
          <span class="secondary--text">
            <strong>
              Matthew Kaye
              - {{ new Date().getFullYear() }}
            </strong>
          </span>
          <v-btn class="mb-2 ml-2" icon href="https://www.linkedin.com/in/matthew-kaye-20332016a/">
            <v-icon>mdi-linkedin</v-icon>
          </v-btn>
          <v-btn
            class="mb-1 ml-1 mr-2"
            icon
            href="mailto:matt-website-queries@outlook.com?subject=Website Feedback"
          >
            <v-icon>mdi-email</v-icon>
          </v-btn>
          <v-btn class="mb-2 mr-4" @click="$refs.aboutDialog.dialog=true">About</v-btn>
          <AboutDialog ref="aboutDialog" />
        </div>
      </v-card>
    </v-footer>
  </v-app>
</template>
<script>
import NavigationBar from "./components/NavigationBar.vue";
import AboutDialog from "@/components/AboutDialog";

export default {
  name: "app",
  components: {
    NavigationBar,
    AboutDialog
  },
  created() {
    if (window.location.href.includes("dark")) {
      this.$vuetify.theme.dark = location.search.includes("dark=true");
    } else {
      this.$vuetify.theme.dark = true;
    }
    window.activeTab = true;
    window.onfocus = function() {
      window.activeTab = true;
    };
    window.onblur = function() {
      window.activeTab = false;
    };
  },
  mounted() {
    this.$root.$on("toggleFooter", () => {
      this.footer = !this.footer;
    });
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
a {
  text-decoration: none;
}
html,
body {
  max-width: 100% !important;
  overflow-x: hidden !important;
}
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
