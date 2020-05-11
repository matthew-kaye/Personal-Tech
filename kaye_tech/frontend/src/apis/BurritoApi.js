import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const baseUrl = "/api/burritos/";

export default class BurritoApi {
  getVendor(id) {
    const url = baseUrl + id;
    return axios
      .get(url)
      .then((response) => response.data)
      .catch(error => console.log(error));
  }

  getVendors(data) {
    return axios
      .get(baseUrl, { params: data })
      .then((response) => response.data)
      .catch(error => console.log(error));
  }

  makeVendor(vendorData) {
    const data = { vendorData: vendorData };
    return axios
      .post(baseUrl, data)
      .then((response) => response.data)
      .catch(error => console.log(error));
  }

  updateVendor(data) {
    const url = baseUrl + data.id + "/";
    return axios
      .put(url, { vendorData: data })
      .then((response) => response.data)
      .catch(error => console.log(error));
  }

}
