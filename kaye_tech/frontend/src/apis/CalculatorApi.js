import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const baseUrl = "/api/calculator/";

export default class CalculatorApi {
    getDamage(data) {
        return axios
            .get(baseUrl, { params: data })
            .then((response) => response.data);
    }
}
