import Vue from "vue";
import VueRouter from "vue-router";

import vuetify from "./plugins/vuetify";

import App from "./App.vue";
import Index from "./pages/Index.vue";
import Joke from "./pages/Joke.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", redirect: "/kaye_tech" },
  { path: "/kaye_tech", name: "kaye_tech", component: Index },
  { path: "/jokes", name: "jokes", component: Joke },
];

const router = new VueRouter({
  mode: "history",
  base: __dirname,
  routes
});

window.Vue = Vue;
new Vue({
  router,
  vuetify,
  render: (h) => h(App)
}).$mount("#app");
