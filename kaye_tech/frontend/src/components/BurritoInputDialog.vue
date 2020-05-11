<template>
  <v-dialog v-model="isVisible" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Add Burrito Vendor</span>
      </v-card-title>
      <v-divider />
      <br />
      <v-card-text>
        <v-row justify="start">
          <v-col>
            <v-text-field v-model="vendorData.name" label="Vendor name" required></v-text-field>
          </v-col>
          <v-col cols="1" md="auto">
            <v-img
              max-height="50"
              max-width="50"
              v-if="vendorData.imageUrl"
              :src="vendorData.imageUrl"
            />
          </v-col>
        </v-row>
        <br />
        <v-textarea v-model="vendorData.review" label="Review" required></v-textarea>
        <br />
        <v-text-field v-model="vendorData.url" label="Url" required></v-text-field>
        <br />
        <v-text-field v-model="vendorData.imageUrl" label="Image Url" required></v-text-field>

        <br />
        <br />
        <v-slider
          thumb-label="always"
          label="Rating"
          step="0.01"
          v-model="vendorData.rating"
          max="5"
          min="0"
        ></v-slider>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="close">Close</v-btn>
        <v-btn color="primary" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import AccountsApi from "@/apis/AccountsApi";
const accountsApi = new AccountsApi();

export default {
  components: {},
  created() {},
  data() {
    return {
      vendorData: {
        name: "",
        review: "",
        url: "",
        imageUrl: "",
        rating: 0
      }
    };
  },
  computed: {
    isVisible() {
      return this.dialog;
    }
  },
  props: {
    dialog: Boolean
  },
  methods: {
    close() {
      this.$emit("close");
    },
    save() {
      this.$emit("save", this.vendorData);
      this.$emit("close");
    }
  }
};
</script>
