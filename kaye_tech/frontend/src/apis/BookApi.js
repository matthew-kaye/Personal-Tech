import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

const listUrl = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json";
const reviewUrl = "https://api.nytimes.com/svc/books/v3/reviews.json";
const nytApiKey = "XF7JacilFFCdHR6kKTSESVYB220aKanS";

export default class BookApi {
  fetchBooks() {
    return axios
      .get(listUrl, {
        params: {
          "api-key": nytApiKey
        },
        headers: { Accept: "application/json" }
      })
      .then((response) => response.data)
      .catch(error => console.log(error));
  }

  fetchReviews(isbn) {
    return axios
      .get(reviewUrl, {
        params: {
          "api-key": nytApiKey,
          isbn: isbn
        },
        headers: { Accept: "application/json" }
      })
      .then((response) => response.data)
      .catch(error => console.log(error));
  }

}
