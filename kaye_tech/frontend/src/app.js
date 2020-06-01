import Vue from "vue";
import VueRouter from "vue-router";
import vuetify from "./plugins/vuetify";
import App from "./App.vue";
import Home from "./pages/Home.vue"
import Canvas from "./pages/Canvas.vue";
import Joke from "./pages/Joke.vue";
import News from "./pages/News.vue";
import Books from "./pages/Books.vue";
import BookDetailPage from "./pages/BookDetailPage.vue";
import Burritos from "./pages/Burritos.vue";
import Games from "./pages/Games.vue";
import Room from "./pages/Room.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", name: "home", component: Home },
  { path: "/news", name: "news", component: News },
  { path: "/books", name: "books", component: Books },
  {
    path: "/book/:bookRank",
    name: "BookDetailPage",
    component: BookDetailPage
  },
  {
    path: "/games/:roomName",
    name: "room",
    component: Room
  },
  { path: "/burritos", name: "burritos", component: Burritos },
  { path: "/canvas", name: "canvas", component: Canvas },
  { path: "/jokes", name: "jokes", component: Joke },
  { path: "/games", name: "games", component: Games },
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