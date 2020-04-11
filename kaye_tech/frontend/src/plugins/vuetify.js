import Vue from "vue";
import Vuetify from "vuetify";
import "vuetify/dist/vuetify.min.css";

import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: window.matchMedia("(prefers-color-scheme: dark)").matches,
    themes: {
      light: {
        // primary: "",
        // secondary: "",
        // accent: "",
        // card: colors.grey.lighten5,
        // background: ""
      },
      dark: {
        // primary: "",
        // secondary: "",
        // accent: "",
        // card: colors.grey.darken4,
        // background: ""
      }
    }
  }
});
