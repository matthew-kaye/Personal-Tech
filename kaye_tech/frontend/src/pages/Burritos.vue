<template>
  <div>
    <v-card class="ma-6">
      <v-card-title class="headline">
        <span class="white--text">Burrito Rankings</span>
        <v-spacer />
        <v-text-field
          class="ml-5"
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          style="max-width: 350px;"
        ></v-text-field>
      </v-card-title>
      <v-divider />
      <v-data-table
        :headers="headers"
        :search="search"
        :items="vendors"
        sort-desc
        :sort-by="'fields.rating'"
      >
        <template v-slot:item="row">
          <tr>
            <td @click="viewVendor(row.item)" v-bind:style="{ cursor: 'pointer' }">
              <v-row justify="start" align="center">
                <v-col md="auto">
                  <v-img
                    max-height="40"
                    max-width="40"
                    v-if="row.item.fields['img_url']"
                    :src="row.item.fields['img_url']"
                  />
                </v-col>
                <v-col md="auto">{{ row.item.fields.name }}</v-col>
              </v-row>
            </td>
            <td @click="viewVendor(row.item)" v-bind:style="{ cursor: 'pointer' }">
              <v-chip :color="getRatingColour(row.item.fields.rating)">
                {{ row.item.fields.rating.toFixed(2) }}
                <v-icon right>mdi-star</v-icon>
              </v-chip>
            </td>
            <td>
              <a :href="row.item.fields.url">
                <v-btn color="primary" dark medium>
                  <v-icon left>mdi-taco</v-icon>Visit Site
                </v-btn>
              </a>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
    <br />
    <br />
    <BurritoInputDialog
      :dialogMode="dialogMode"
      :vendor="vendor"
      :admin="admin"
      @save="saveData"
      @update="updateData"
      ref="burritoInputDialog"
    />
    <v-btn
      v-if="admin"
      color="primary"
      fixed
      bottom
      right
      fab
      large
      class="mb-12 mr-4"
      @click="addNewVendor()"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
  </div>
</template>

<script>
import BurritoApi from "@/apis/BurritoApi";
import BurritoInputDialog from "@/components/BurritoInputDialog";
import AccountsApi from "@/apis/AccountsApi";
const accountsApi = new AccountsApi();
import colors from "vuetify/lib/util/colors";

const burritoApi = new BurritoApi();

export default {
  components: {
    BurritoInputDialog
  },
  created() {
    this.fetchVendors();
    accountsApi.getCurrentUser().then(data => {
      this.currentUser = data.username;
    });
  },
  data() {
    return {
      search: "",
      vendors: [],
      vendor: null,
      dialogMode: "",
      currentUser: ""
    };
  },
  computed: {
    headers() {
      return [
        { text: "Name", align: "start", value: "fields.name" },
        { text: "Rating", align: "start", value: "fields.rating" },
        { text: "Actions", align: "start" }
      ];
    },
    vendorData() {
      return {
        id: this.vendor.pk,
        name: this.vendor.fields.name,
        review: this.vendor.fields.description,
        url: this.vendor.fields.url,
        imageUrl: this.vendor.fields.img_url,
        rating: this.vendor.fields.rating
      };
    },
    admin() {
      return this.currentUser == "mattkindlekaye";
    }
  },
  methods: {
    addNewVendor() {
      this.vendor = null;
      this.dialogMode = "Create";
      this.$refs.burritoInputDialog.open();
    },
    viewVendor(vendor) {
      this.vendor = vendor;
      this.dialogMode = "View";
      this.$refs.burritoInputDialog.open();
    },
    saveData(vendorData) {
      burritoApi.makeVendor(vendorData).then(data => {
        this.fetchVendors();
      });
    },
    updateData(vendorData) {
      burritoApi.updateVendor(vendorData).then(data => {
        this.fetchVendors();
      });
    },
    fetchVendors() {
      burritoApi.getVendors({}).then(data => {
        this.vendors = JSON.parse(data);
      });
    },
    getRatingColour(rating) {
      if (rating >= 4) {
        return colors.green.darken1;
      } else if (rating >= 3) {
        return colors.orange.darken1;
      } else {
        return colors.red.darken1;
      }
    }
  }
};
</script>
