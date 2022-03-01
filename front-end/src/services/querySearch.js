import axios from "axios";

const url = "http://127.0.0.1:5000/api/search/";

export async function getResult(query) {
  return await axios.get(`${url}${query}`);
}
