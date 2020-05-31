<template>
  <div>
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
    <v-row>
      <v-col md="auto">
        <v-btn
          color="primary"
          class="ml-6"
          @click="snakeGame=!snakeGame"
        >{{ snakeGame?"Close Snake Game":"Open Snake Game" }}</v-btn>
      </v-col>
      <v-col>
        <v-slide-y-transition>
          <SnakeGame v-if="snakeGame" class="pb-6" />
        </v-slide-y-transition>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import SnakeGame from "@/components/SnakeGame.vue";
export default {
  components: {
    SnakeGame
  },
  data() {
    return {
      roomName: "",
      snakeGame: true
    };
  },
  methods: {
    joinRoom(roomName) {
      window.location.pathname = "/games/" + roomName + "/";
    }
  }
};
</script>

<style scoped></style>