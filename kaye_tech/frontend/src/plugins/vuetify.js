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
        primary: colors.pink.darken4,
        secondary: colors.shades.black,
        offset: colors.grey.darken1,
        card: colors.shades.white,
        background: colors.shades.white
      },
      dark: {
        primary: colors.pink.darken4,
        secondary: colors.shades.white,
        offset: colors.grey.darken4,
        card: colors.grey.darken4,
        background: colors.shades.black
      }
    }
  }
});
