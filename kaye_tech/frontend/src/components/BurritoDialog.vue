<template>
  <v-dialog v-model="dialog" max-width="700px">
    <v-card>
      <v-card-title v-if="dialogMode!='View'">
        <span class="headline">Add Burrito Vendor</span>
        <v-spacer />
        <v-btn icon @click="dialog=false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-divider class="mb-n2" v-if="dialogMode!='View'" />
      <v-card-title>
        <v-row justify="start" align="center">
          <v-col cols="auto" v-show="vendorData.imageUrl">
            <v-img contain max-height="50" max-width="50" :src="vendorData.imageUrl" />
          </v-col>
          <v-col cols="auto">
            <h2 v-if="dialogMode=='View' && !editable">{{vendorData.name}}</h2>
            <v-text-field
              outlined
              class="mt-2 mb-n6"
              v-if="editable"
              v-model="vendorData.name"
              label="Vendor name"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="auto">
            <v-btn
              v-if="admin && dialogMode=='View' && editable"
              @click="toggleEditMode()"
              color="primary"
              dark
              medium
            >
              <v-icon left>mdi-pencil</v-icon>Toggle Edit
            </v-btn>
            <v-btn large @click="deleteVendor()" color="primary" v-if="admin && !editable" icon>
              <v-icon large class="mb-1">mdi-delete-circle</v-icon>
            </v-btn>
          </v-col>
          <v-spacer />
          <v-col v-if="dialogMode=='View'">
            <v-btn icon @click="dialog=false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>
      <v-divider />
      <br />
      <v-card-text>
        <v-textarea outlined v-if="editable" v-model="vendorData.review" label="Review" required></v-textarea>
        <v-card v-if="!editable" elevation="12">
          <v-card-title @click="toggleEditMode()" class="primary headline white--text">
            <span style="font-size:14pt">Review</span>
          </v-card-title>
          <v-divider />
          <v-card-text class="secondary--text">
            <div v-html="reviewDisplay"></div>
          </v-card-text>
        </v-card>
        <br />
        <v-text-field outlined :readonly="!editable" v-model="vendorData.url" label="Url" required></v-text-field>
        <br />
        <v-text-field
          outlined
          v-if="editable"
          :readonly="!editable"
          v-model="vendorData.imageUrl"
          label="Image Url"
          required
        ></v-text-field>
        <br />
        <br />
        <v-slider
          :readonly="!editable && !admin"
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
          :disabled="!editable &&!admin"
          v-if="vendorData.id"
          text
          @click="updateVendor()"
        >Update</v-btn>
        <v-btn color="primary" v-if="!vendorData.id" text @click="saveVendor()">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      adminAccess: false
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
      return this.dialogMode != "View" || this.adminAccess;
    }
  },
  props: {
    dialogMode: String,
    vendor: Object,
    admin: Boolean
  },
  methods: {
    open() {
      this.adminAccess = false;
      this.dialog = true;
    },
    close() {
      this.dialog = false;
    },
    saveVendor() {
      this.$emit("save", this.vendorData);
      this.dialog = false;
    },
    updateVendor() {
      this.$emit("update", this.vendorData);
      this.dialog = false;
    },
    deleteVendor() {
      this.$emit("delete");
    },
    toggleEditMode() {
      if (this.admin) {
        this.adminAccess = !this.adminAccess;
      }
    }
  }
};
</script>
