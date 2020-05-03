import axios from "axios";
const guardianApiKey = "24e1ad31-618f-4937-acb3-9f414756ce88";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const contentUrl = "https://content.guardianapis.com/search";
const sectionsUrl = "https://content.guardianapis.com/sections";

export default class NewsApi {
    fetchArticles(requestParams) {
        return axios
            .get(contentUrl, {
                params: {
                    ...requestParams,
                    "api-key": guardianApiKey
                },
                headers: { Accept: "application/json" }
            })
            .then((response) => response.data)
            .catch(error => console.log(error));
    }

    fetchSections() {
        return axios
            .get(sectionsUrl, {
                params: {
                    "api-key": guardianApiKey
                },
                headers: { Accept: "application/json" }
            })
            .then((response) => response.data)
            .catch(error => console.log(error));
    }
}
