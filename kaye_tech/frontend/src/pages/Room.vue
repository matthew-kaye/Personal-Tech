<template>
  <div>
    <v-card class="ma-6">
      <v-card-title class="primary headline">
        <span class="white--text ml-4">{{roomName}}</span>
      </v-card-title>
      <v-card-title class="ml-4 mt-2">Send a message to the chat:</v-card-title>
      <v-card-text class="ml-4">
        <v-row>
          <v-col cols="3" sm="3">
            <v-text-field
              v-model="chatMessage"
              @keypress.enter="submitMessage(chatMessage)"
              append-icon="mdi-magnify"
              label="Type message here"
              required
            ></v-text-field>
          </v-col>
          <v-col md="auto">
            <v-fab-transition>
              <v-btn
                v-if="chatMessage.length > 0"
                class="mb-2 mr-2"
                color="primary"
                @click="submitMessage(chatMessage)"
              >{{ "Send" }}</v-btn>
            </v-fab-transition>
          </v-col>
        </v-row>
        <textarea id="chat-log" cols="100" rows="20"></textarea>
        <br />
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import CanvasSheet from "@/components/CanvasSheet.vue";
import AccountsApi from "@/apis/AccountsApi";
const accountsApi = new AccountsApi();

export default {
  data() {
    return {
      chatMessage: "",
      chatSocket: null,
      roomName: this.$route.params.roomName,
      messages: [],
      currentUser: null
    };
  },
  created() {
    accountsApi.getCurrentUser().then(data => {
      this.currentUser = data;
    });
  },
  mounted() {
    this.chatSocket = new WebSocket(
      "ws://" + window.location.host + "/ws/cards/" + this.roomName + "/"
    );
    this.chatSocket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      document.querySelector("#chat-log").value += data.message + "\n";
    };
    this.chatSocket.onclose = function(e) {
      console.error("Chat socket closed unexpectedly");
    };
  },
  methods: {
    submitMessage(chatMessage) {
      chatMessage = `${this.currentUser.first_name}:  ${chatMessage}`;
      this.chatSocket.send(
        JSON.stringify({
          message: chatMessage
        })
      );
      this.chatMessage = "";
    }
  }
};
</script>

<style scoped></style>