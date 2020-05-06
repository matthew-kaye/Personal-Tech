import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const baseUrl = "/api/burritos/";

export default class ItemsApi {
  getVendor(id) {
    const url = baseUrl + id;
    return axios
      .get(url)
      .then((response) => response.data)
      .catch();
  }

  getItems(data) {
    return axios
      .get(baseUrl, { params: data })
      .then((response) => response.data)
      .catch();
  }

  makeVendor(vendorData) {
    const data = { vendorData: vendorData };
    return axios
      .post(baseUrl, data)
      .then((response) => response.data)
      .catch();
  }

  updateItem(id, data) {
    const url = baseUrl + id + "/";
    return axios.put(url, { formData: data }).then((response) => response.data);
  }

  updateItem(id, status) {
    const url = baseUrl + id + "/";
    return axios
      .patch(url, { status: status })
      .then((response) => response.data);
  }
}
