<template>
  <div>
    <v-row class="mt-4 ml-3">
      <v-col md="auto">
        <v-btn color="primary" @click="snakeGame=!snakeGame">
          <v-icon class="mr-2">mdi-gamepad</v-icon>
          {{ snakeGame?"Close Snake Game":"Open Snake Game" }}
        </v-btn>
      </v-col>
      <v-col md="auto">
        <v-btn class="ml-6" color="primary" @click="capitalGame=!capitalGame">
          <v-icon class="mr-2">mdi-earth</v-icon>
          {{ capitalGame?"Close Capital Game":"Open Capital Game" }}
        </v-btn>
      </v-col>
      <v-col md="auto">
        <v-btn class="ml-6" color="primary" @click="damageCalculator=!damageCalculator">
          <v-icon class="mr-2">mdi-dice-d20</v-icon>
          {{ damageCalculator?"Close Calculator":"Open D&D Calculator" }}
        </v-btn>
      </v-col>
      <!-- <v-col>
        <v-btn
          class="ml-6"
          color="primary"
          @click="roomSelect=!roomSelect"
        >{{ roomSelect?"Close Room Select":"Join Room (Unfinished)" }}</v-btn>
      </v-col>-->
    </v-row>
    <v-fade-transition>
      <v-row v-if="snakeGame" class="ml-3">
        <v-col md="auto" v-if="snakeHighScores.length>0">
          <v-card cols="1" width="400">
            <v-list>
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
            <v-divider />
            <v-card-text>Direct the snake to eat the apple using the arrow keys, and press space bar to pause. Press any key to begin. Avoid hitting the walls!</v-card-text>
          </v-card>
        </v-col>
        <v-col>
          <SnakeGame class="pb-4" />
        </v-col>
      </v-row>
    </v-fade-transition>
    <v-fade-transition>
      <div v-if="capitalGame">
        <CapitalGuesser />
      </div>
    </v-fade-transition>
    <v-fade-transition>
      <div v-if="damageCalculator">
        <DamageCalculator ref="calculator" />
      </div>
    </v-fade-transition>
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
import CapitalGuesser from "@/components/CapitalGuesser.vue";
import DamageCalculator from "@/components/DamageCalculator.vue";
import SnakeApi from "@/apis/SnakeApi";
const snakeApi = new SnakeApi();
export default {
  components: {
    SnakeGame,
    CapitalGuesser,
    DamageCalculator
  },
  data() {
    return {
      roomName: "",
      snakeGame: false,
      capitalGame: false,
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
