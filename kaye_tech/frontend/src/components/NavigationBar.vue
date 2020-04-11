<template>
  <div v-if="currentUser">
    <v-navigation-drawer v-model="drawer" absolute temporary app>
      <v-list>
        <v-list-item v-for="item in navigationItems" :key="item.label" :to="item.link" link>
          <v-list-item-icon>
            <v-icon color="secondary">{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ item.label }}</v-list-item-title>
        </v-list-item>
        <v-list-item href="/accounts/logout/">
          <v-list-item-icon>
            <v-icon color="secondary">mdi-logout</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Log Out</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar dark color="primary">
      <v-app-bar-nav-icon class="hidden-lg-and-up" @click="drawer = !drawer"></v-app-bar-nav-icon>
      <router-link to="/" tag="span" style="cursor: pointer; display: flex;">
        <v-img class="ml-2" max-height="50" max-width="60" src="/static/frontend/vue-logo.svg.png" />

        <v-toolbar-title class="ma-3">
          <b class="headline font-weight-bold">Kaye Tech</b>
        </v-toolbar-title>
      </router-link>
      <v-spacer></v-spacer>
      <v-tooltip bottom color="tooltip">
        <template v-slot:activator="{ on }">
          <v-btn icon text @click="toggleDark" v-on="on">
            <v-icon>mdi-brightness-6</v-icon>
          </v-btn>
        </template>
        Toggle dark mode
      </v-tooltip>
      <v-toolbar-items class="hidden-md-and-down">
        <v-chip class="ma-4 pa-0" outlined color="white">
          <v-btn text v-for="item in navigationItems" :key="item.label" :to="item.link">
            <v-icon left dark>{{ item.icon }}</v-icon>
            {{ item.label }}
          </v-btn>
        </v-chip>
      </v-toolbar-items>
      <v-avatar class="ml-2" size="40">
        <img :src="currentUser.profile.avatar" />
      </v-avatar>
      <v-btn class="ml-2 mr-1" icon text href="/accounts/logout/">
        <v-icon dark>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>
import AccountsApi from "@/apis/AccountsApi";

const accountsApi = new AccountsApi();

export default {
  name: "NavigationBar",
  data() {
    return {
      drawer: false,
      navigationItems: [
        {
          label: "Home",
          link: "/kaye_tech",
          icon: "mdi-home"
        },
        {
          label: "Home2",
          link: "/kaye_tech",
          icon: "mdi-home"
        },
        {
          label: "Home3",
          link: "/kaye_tech",
          icon: "mdi-home"
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
      if (this.currentUser.profile === null) {
        location.href = "/accounts/logout/";
      }
    });
  },
  methods: {
    toggleDark() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    }
  }
};
</script>

<style>
.v-chip .v-icon {
  font-size: 16px;
}
</style>
