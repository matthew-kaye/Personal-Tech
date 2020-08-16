<template>
  <div>
    <v-card class="ma-6">
      <v-card-title class="primary headline">
        <span class="mr-4 my-2 white--text" md="auto">Burrito Rankings</span>
        <v-btn class="mr-6" v-if="admin" color="primary" medium @click="addNewVendor()">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
        <v-spacer />
        <v-text-field
          dark
          outlined
          class="mb-n8"
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          style="max-width: 350px;"
        ></v-text-field>
      </v-card-title>
      <v-divider />
      <v-fab-transition>
        <v-data-table
          :headers="headers"
          :search="search"
          :items="vendors"
          disable-pagination
          hide-default-footer
          sort-desc
          calculate-widths
          :sort-by="'fields.rating'"
        >
          <template v-slot:item="row">
            <tr>
              <td
                class="hidden-xs-only"
                @click="viewVendor(row.item)"
                v-bind:style="{ cursor: 'pointer' }"
              >{{vendors.indexOf(row.item)+1}}</td>
              <td @click="viewVendor(row.item)" v-bind:style="{ cursor: 'pointer' }">
                <v-row justify="start" align="center" class="ma-n2">
                  <v-col cols="auto">
                    <v-img contain height="45" max-width="45" :src="row.item.fields['img_url']">
                      <template v-slot:placeholder>
                        <v-row class="fill-height ma-0" align="center" justify="center">
                          <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                        </v-row>
                      </template>
                    </v-img>
                  </v-col>
                  <v-col md="auto">{{ row.item.fields.name }}</v-col>
                </v-row>
              </td>
              <td @click="viewVendor(row.item)" v-bind:style="{ cursor: 'pointer' }">
                <v-chip class="white--text" :color="getRatingColour(row.item.fields.rating)">
                  {{ row.item.fields.rating.toFixed(2) }}
                  <v-icon right>mdi-star</v-icon>
                </v-chip>
              </td>
              <td class="hidden-xs-only">
                <a :href="row.item.fields.url" target="_blank">
                  <v-btn color="primary" dark medium>
                    <v-icon left>mdi-taco</v-icon>Visit Site
                  </v-btn>
                </a>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-fab-transition>
    </v-card>
    <BurritoDialog
      :dialogMode="dialogMode"
      :vendor="vendor"
      :admin="admin"
      @save="saveData"
      @update="updateData"
      @delete="warningDialog=true"
      ref="burritoDialog"
    />
    <WarningDialog cols="3" :dialog="warningDialog" @yes="deleteData" @no="warningDialog=false" />
  </div>
</template>

<script>
import BurritoApi from "@/apis/BurritoApi";
import BurritoDialog from "@/components/BurritoDialog";
import WarningDialog from "@/components/WarningDialog";
import AccountsApi from "@/apis/AccountsApi";
const accountsApi = new AccountsApi();
import colors from "vuetify/lib/util/colors";

const burritoApi = new BurritoApi();

export default {
  components: {
    BurritoDialog,
    WarningDialog
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
      currentUser: "",
      warningDialog: false
    };
  },
  computed: {
    headers() {
      return [
        { text: "Rank", align: "start", sortable: false, width: 0 },
        { text: "Name", align: "start", value: "fields.name" },
        { text: "Rating", align: "start", value: "fields.rating" },
        { text: "Actions", align: "start", sortable: false }
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
      this.$refs.burritoDialog.open();
    },
    viewVendor(vendor) {
      this.vendor = vendor;
      this.dialogMode = "View";
      this.$refs.burritoDialog.open();
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
    deleteData() {
      this.warningDialog = false;
      this.$refs.burritoDialog.close();
      burritoApi.deleteVendor(this.vendor.pk).then(data => {
        this.fetchVendors();
      });
    },
    fetchVendors() {
      burritoApi.getVendors({}).then(data => {
        this.vendors = JSON.parse(data).sort(function(a, b) {
          return b.fields.rating - a.fields.rating;
        });
      });
    },
    getRatingColour(rating) {
      if (rating >= 4.5) {
        return colors.green.darken1;
      } else if (rating >= 4) {
        return colors.lightGreen.darken1;
      } else if (rating >= 3.5) {
        return colors.orange.lighten1;
      } else if (rating >= 3) {
        return colors.orange.darken4;
      } else if (rating >= 2.5) {
        return colors.red.darken1;
      } else {
        return colors.red.darken4;
      }
    }
  }
};
</script>
