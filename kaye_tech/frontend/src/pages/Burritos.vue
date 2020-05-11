<template>
  <div>
    <v-card class="ma-6">
      <v-data-table :headers="headers" :items="vendors" :sort-by="'rating'">
        <template v-slot:item="row">
          <tr v-bind:style="{ cursor: 'pointer' }" @click="viewVendor(row.item)">
            <td>
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
            <td>{{ row.item.fields.rating }}</td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
    <BurritoInputDialog
      :dialog="burritoInputDialog"
      @close="burritoInputDialog = false"
      @save="saveData"
      ref="burritoInputDialog"
    />
    <v-btn
      color="primary"
      fixed
      bottom
      right
      fab
      large
      class="mb-12 mr-4"
      @click="burritoInputDialog = true"
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

const burritoApi = new BurritoApi();

export default {
  components: {
    BurritoInputDialog
  },
  created() {
    burritoApi.getVendors({}).then(data => {
      this.vendors = JSON.parse(data);
    });

    accountsApi.getCurrentUser().then(data => {
      this.currentUser = data;
      console.log(data);
    });
  },
  data() {
    return {
      burritoInputDialog: false,
      vendors: [],
      vendorData: {
        name: "",
        description: "",
        url: "",
        img_url: "",
        rating: 0
      }
    };
  },
  computed: {
    headers() {
      return [
        { text: "Name", align: "start", value: "name" },
        { text: "Rating", align: "start", value: "rating" }
      ];
    }
  },
  methods: {
    viewVendor() {
      console.log("view vendor");
    },
    saveData(vendorData) {
      burritoApi.makeVendor(vendorData);
    }
  }
};
</script>
