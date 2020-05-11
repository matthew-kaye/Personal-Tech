<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <v-row justify="start">
          <v-col md="auto">
            <v-img
              max-height="50"
              max-width="50"
              v-if="vendorData.imageUrl"
              :src="vendorData.imageUrl"
            />
          </v-col>
          <v-col class="mt-1">
            <h1 v-if="dialogMode!='View'">Add Burrito Vendor</h1>
            <h1 v-if="dialogMode=='View'">{{vendorData.name}}</h1>
          </v-col>
        </v-row>
      </v-card-title>
      <v-divider />
      <br />
      <v-card-text>
        <v-text-field
          v-if="dialogMode!='View'"
          v-model="vendorData.name"
          label="Vendor name"
          required
        >
          <br />
        </v-text-field>
        <v-textarea v-if="editable" v-model="vendorData.review" label="Review" required></v-textarea>
        <v-card v-if="!editable" elevation="12">
          <v-card-title class="primary headline white--text">
            <span style="font-size:14pt">Review</span>
          </v-card-title>
          <v-divider />
          <v-card-text class="secondary--text">
            <div v-html="reviewDisplay"></div>
          </v-card-text>
        </v-card>

        <br />
        <v-text-field :readonly="!editable" v-model="vendorData.url" label="Url" required></v-text-field>
        <br />
        <v-text-field
          v-if="editable"
          :readonly="!editable"
          v-model="vendorData.imageUrl"
          label="Image Url"
          required
        ></v-text-field>

        <br />
        <br />
        <v-slider
          :readonly="!editable"
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
        <v-btn
          color="primary"
          :disabled="!editable"
          v-if="vendorData.id"
          text
          @click="update"
        >Update</v-btn>
        <v-btn color="primary" v-if="!vendorData.id" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false
    };
  },
  computed: {
    reviewDisplay() {
      return this.vendorData.review
        ? this.vendorData.review.replace(/\n/g, "<br>")
        : null;
    },
    vendorData() {
      return {
        id: this.vendor ? this.vendor.pk : null,
        name: this.vendor ? this.vendor.fields.name : "",
        review: this.vendor ? this.vendor.fields.description : "",
        url: this.vendor ? this.vendor.fields.url : "",
        imageUrl: this.vendor ? this.vendor.fields.img_url : "",
        rating: this.vendor ? this.vendor.fields.rating : 0
      };
    },
    editable() {
      return this.dialogMode != "View";
    }
  },
  props: {
    dialogMode: String,
    vendor: Object
  },
  methods: {
    close() {
      this.dialog = false;
    },
    save() {
      this.$emit("save", this.vendorData);
      this.dialog = false;
    },
    update() {
      this.$emit("update", this.vendorData);
      this.dialog = false;
    }
  }
};
</script>
