<template>
  <div>
    <v-card class="ma-6">
      <v-data-table :headers="headers" :items="vendors">
        <template v-slot:item="row">
          <tr v-bind:style="{ cursor: 'pointer' }" @click="viewVendor(row.item)">
            <td>
              <p>{{ row.item.rank }}</p>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
    <v-speed-dial
      v-model="fab"
      bottom
      right
      direction="top"
      transition="slide-y-reverse-transition"
      fixed
      class="ma-12"
    >
      <template v-slot:activator>
        <v-btn v-model="fab" fab color="primary">
          <v-icon v-if="fab">mdi-close</v-icon>
          <v-icon v-else>mdi-chevron-up</v-icon>
        </v-btn>
      </template>
      <v-btn fab dark small color="primary" @click="console.log('add')">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
      <v-btn fab dark small color="green" @click="console.log('edit')">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn fab dark small color="red" @click="console.log('delete')">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-speed-dial>
  </div>
</template>

<script>
import BurritoApi from "@/apis/BurritoApi";
const burritoApi = new BurritoApi();

export default {
  components: {},
  created() {
    burritoApi.makeVendor({
      name: "Chilango",
      rating: 4.9
    });
  },
  data() {
    return {
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
      return [{ text: "Name", align: "start", value: "name", width: 250 }];
    }
  },
  methods: {}
};
</script>
