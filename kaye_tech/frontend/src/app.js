import Vue from "vue";
import VueRouter from "vue-router";

import vuetify from "./plugins/vuetify";

import App from "./App.vue";
import Index from "./pages/Index.vue";
import Joke from "./pages/Joke.vue";
import Tabletop from "./pages/Tabletop.vue";
import News from "./pages/News.vue";
import Books from "./pages/Books.vue";
import BookDetailPage from "./pages/BookDetailPage.vue";
import Burritos from "./pages/Burritos.vue";
import BurritoDetailPage from "./pages/Burritos.vue";


Vue.use(VueRouter);

const routes = [
  { path: "/", redirect: "/news" },
  { path: "/news", name: "news", component: News },
  { path: "/books", name: "books", component: Books },
  {
    path: "/book/:bookRank",
    name: "BookDetailPage",
    component: BookDetailPage
  },
  {
    path: "/burritos/:burritoId",
    name: "BurritoDetailPage",
    component: BurritoDetailPage
  },
  { path: "/burritos", name: "burritos", component: Burritos },
  { path: "/home", name: "home", component: Index },
  { path: "/jokes", name: "jokes", component: Joke },
  { path: "/tabletop", name: "tabletop", component: Tabletop },
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
