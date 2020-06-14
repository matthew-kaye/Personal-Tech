<template>
  <div v-if="currentUser" @click="closeGui()">
    <v-navigation-drawer v-model="drawer" absolute temporary app>
      <v-list>
        <v-list-item
          v-for="item in navigationItems"
          :key="item.label"
          :to="item.link +'?dark='+ $vuetify.theme.dark"
          link
        >
          <v-list-item-icon>
            <v-icon color="secondary">{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ item.label }}</v-list-item-title>
        </v-list-item>
        <v-list-item :href="'/accounts/logout/?next='+$route.path">
          <v-list-item-icon>
            <v-icon color="secondary">mdi-logout</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Log Out</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar dark color="primary">
      <v-app-bar-nav-icon class="hidden-lg-and-up" @click="drawer = !drawer"></v-app-bar-nav-icon>
      <span @click="goHome()" tag="span" style="cursor: pointer; display: flex;">
        <v-img class="ml-2 mt-1" max-height="46" max-width="50" src="/static/frontend/k-logo.jpg" />
        <v-toolbar-title class="ma-3">
          <b class="headline font-weight-bold">Matt's Tech</b>
        </v-toolbar-title>
      </span>
      <v-spacer></v-spacer>
      <v-tooltip bottom color="tooltip">
        <template v-slot:activator="{ on }">
          <v-btn class="mr-1" icon text @click="toggleDark" v-on="on">
            <v-icon>mdi-brightness-6</v-icon>
          </v-btn>
        </template>
        Toggle dark mode
      </v-tooltip>
      <v-tooltip bottom color="tooltip">
        <template v-slot:activator="{ on }">
          <v-btn icon text @click="$refs.aboutDialog.dialog=true" v-on="on">
            <v-icon>mdi-information-outline</v-icon>
          </v-btn>
        </template>
        About the website
      </v-tooltip>
      <AboutDialog ref="aboutDialog" />
      <v-toolbar-items class="hidden-md-and-down">
        <v-chip class="ma-4 pa-0" outlined color="white">
          <v-btn
            text
            v-for="item in navigationItems"
            :key="item.label"
            :to="item.link +'?dark=' +$vuetify.theme.dark"
          >
            <v-icon left dark>{{ item.icon }}</v-icon>
            {{ item.label }}
          </v-btn>
        </v-chip>
      </v-toolbar-items>
      <v-avatar class="ml-2" size="40" v-if="currentUser.profile.avatar">
        <img :src="currentUser.profile.avatar" />
      </v-avatar>
      <v-btn
        class="ml-2 mr-1"
        icon
        text
        :href="'/accounts/logout/?next='+$route.path"
        v-if="currentUser.id"
      >
        <v-icon dark>mdi-logout</v-icon>
      </v-btn>
      <v-btn
        class="ml-2 mr-1"
        text
        :href="'/accounts/splash/?next='+$route.path"
        v-if="!currentUser.id"
      >Sign In</v-btn>
    </v-app-bar>
  </div>
</template>

<script>
import AboutDialog from "@/components/AboutDialog";
import AccountsApi from "@/apis/AccountsApi";
const accountsApi = new AccountsApi();

export default {
  name: "NavigationBar",
  components: {
    AboutDialog
  },
  data() {
    return {
      drawer: false,
      navigationItems: [
        {
          label: "News",
          link: "/news",
          icon: "mdi-newspaper"
        },
        {
          label: "Books",
          link: "/books",
          icon: "mdi-book-open-page-variant"
        },
        {
          label: "Burritos",
          link: "/burritos",
          icon: "mdi-taco"
        },
        {
          label: "Fluids",
          link: "/fluids",
          icon: "mdi-brush"
        },
        {
          label: "Games",
          link: "/games",
          icon: "mdi-dice-d20"
        },
        // {
        //   label: "Cards",
        //   link: "/cards",
        //   icon: "mdi-cards"
        // },
        {
          label: "Jokes",
          link: "/jokes",
          icon: "mdi-emoticon"
        }
      ],
      logoutItem: [
        {
          label: "Log out",
          callback: this.logout,
          textTransform: false
        }
      ],
      currentUser: null
    };
  },
  created() {
    accountsApi.getCurrentUser().then(data => {
      this.currentUser = data;
    });
  },
  methods: {
    toggleDark() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
      var newUrl = location.pathname + "?dark=" + this.$vuetify.theme.dark;
      window.history.pushState("string", "Title", newUrl);
      if (window.needsRefresh) {
        var background = this.$vuetify.theme.dark ? 0 : 255;
        var colour = { r: background, g: background, b: background };
        this.$root.$emit("changeBackground", colour);
      }
    },
    closeGui() {
      if (window.gui && !location.href.includes("fluids")) {
        window.gui.close();
      }
    },
    goHome() {
      this.$router.push({
        name: "home",
        query: { dark: this.$vuetify.theme.dark }
      });
      location.reload();
    }
  }
};
</script>

<style>
.v-chip .v-icon {
  font-size: 16px;
}
</style>
