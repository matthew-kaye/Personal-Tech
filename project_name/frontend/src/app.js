import Vue from "vue";
import VueRouter from "vue-router";

import vuetify from "./plugins/vuetify";

import App from "./App.vue";
import Index from "./pages/Index.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", redirect: "/project_name" },
  { path: "/project_name", name: "project_name", component: Index }
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
