<template>
  <div>
    <v-row class="mt-4">
      <v-col md="auto">
        <v-btn
          color="primary"
          class="ml-6"
          @click="snakeGame=!snakeGame"
        >{{ snakeGame?"Close Snake Game":"Open Snake Game" }}</v-btn>
      </v-col>
      <v-slide-y-transition>
        <v-col md="auto" v-if="snakeGame && snakeHighScores.length>0">
          <v-list width="400">
            <v-list-item color="primary">Top 10 Leaderboard</v-list-item>
            <v-divider />
            <v-list-item v-for="item in snakeHighScores" :key="item.fields.id">
              <v-list-item-content>{{item.fields.name}}</v-list-item-content>
              <v-list-item-content class="ml-4">{{item.fields.score}}</v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>
      </v-slide-y-transition>
      <v-col>
        <v-slide-y-transition>
          <SnakeGame v-if="snakeGame" class="pb-6" />
        </v-slide-y-transition>
      </v-col>
    </v-row>
    <v-card class="ma-6">
      <v-card-title class="primary headline">
        <span class="white--text">Join a room</span>
      </v-card-title>
      <v-card-title>What room would you like to join?</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="3" sm="3">
            <v-text-field
              v-model="roomName"
              @keypress.enter="joinRoom(roomName)"
              append-icon="mdi-magnify"
              label="Type in the room name"
              required
            ></v-text-field>
          </v-col>
          <v-col md="auto">
            <v-fab-transition>
              <v-btn
                v-if="roomName.length > 0"
                class="mb-2 mr-2"
                color="primary"
                @click="joinRoom(roomName)"
              >{{ "Join" }}</v-btn>
            </v-fab-transition>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import SnakeGame from "@/components/SnakeGame.vue";
import SnakeApi from "@/apis/SnakeApi";
const snakeApi = new SnakeApi();
export default {
  components: {
    SnakeGame
  },
  data() {
    return {
      roomName: "",
      snakeGame: false,
      snakeHighScores: []
    };
  },
  created() {
    snakeApi.getScores({}).then(data => {
      this.snakeHighScores = JSON.parse(data).slice(0, 10);
    });
  },
  methods: {
    joinRoom(roomName) {
      window.location.pathname = "/games/" + roomName + "/";
    }
  }
};
</script>

<style scoped></style>