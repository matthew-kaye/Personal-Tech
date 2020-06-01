import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const baseUrl = "/api/snake/";

export default class BurritoApi {
    getScores(data) {
        return axios
            .get(baseUrl, { params: data })
            .then((response) => response.data)
            .catch(error => console.log(error));
    }

    submitScore(data) {
        const scoreData = { data: data };
        return axios
            .post(baseUrl, scoreData)
            .then((response) => response.data)
            .catch(error => console.log(error));
    }
}
