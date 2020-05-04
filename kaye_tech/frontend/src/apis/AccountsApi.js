import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default class AccountsApi {
  getCurrentUser() {
    const url = "/api/currentuser";
    return axios
      .get(url)
      .then((response) => response.data)
      .catch(error => console.log(error));
  }
}
