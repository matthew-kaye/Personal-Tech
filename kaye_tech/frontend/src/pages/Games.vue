<template>
  <div>
    <v-row class="mt-4 ml-3">
      <v-col md="auto">
        <v-btn
          color="primary"
          @click="snakeGame=!snakeGame"
        >{{ snakeGame?"Close Snake Game":"Open Snake Game" }}</v-btn>
      </v-col>
      <v-col md="auto">
        <v-btn
          class="ml-6"
          color="primary"
          @click="damageCalculator=!damageCalculator"
        >{{ damageCalculator?"Close Calculator":"Open D&D Calculator" }}</v-btn>
      </v-col>
      <v-col>
        <v-btn
          class="ml-6"
          color="primary"
          @click="roomSelect=!roomSelect"
        >{{ roomSelect?"Close Room Select":"Join Room (Unfinished)" }}</v-btn>
      </v-col>
    </v-row>
    <v-fab-transition>
      <Tabletop ref="calculator" v-show="damageCalculator" />
    </v-fab-transition>
    <v-slide-y-transition>
      <v-row v-if="snakeGame" class="ml-3">
        <v-col md="auto" v-if="snakeHighScores.length>0">
          <v-list width="400">
            <v-list-item color="primary">
              Top 10 Leaderboard
              <v-btn icon @click="fetchScores" class="ml-4">
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </v-list-item>
            <v-divider />
            <v-list-item v-for="item in snakeHighScores" :key="item.fields.id">
              <v-list-item-content>{{item.fields.name}}</v-list-item-content>
              <v-list-item-content class="ml-4">{{item.fields.score}}</v-list-item-content>
            </v-list-item>
          </v-list>
          <v-card cols="1">
            <v-card-text>Press any key to start, and space bar to pause</v-card-text>
          </v-card>
        </v-col>
        <v-col>
          <SnakeGame class="pb-4" />
        </v-col>
      </v-row>
    </v-slide-y-transition>
    <v-slide-y-transition>
      <v-card class="ma-6" v-if="roomSelect">
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
    </v-slide-y-transition>
  </div>
</template>

<script>
import SnakeGame from "@/components/SnakeGame.vue";
import Tabletop from "@/components/Tabletop.vue";
import SnakeApi from "@/apis/SnakeApi";
const snakeApi = new SnakeApi();
export default {
  components: {
    SnakeGame,
    Tabletop
  },
  data() {
    return {
      roomName: "",
      snakeGame: false,
      damageCalculator: false,
      roomSelect: false,
      snakeHighScores: []
    };
  },
  created() {
    this.fetchScores();
  },
  methods: {
    joinRoom(roomName) {
      window.location.pathname = "/games/" + roomName + "/";
    },
    fetchScores() {
      snakeApi.getScores({}).then(data => {
        this.snakeHighScores = JSON.parse(data).slice(0, 10);
      });
    }
  }
};
</script>

<style scoped></style>