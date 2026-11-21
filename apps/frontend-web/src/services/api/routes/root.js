import { apiRequest } from "../client.js";

export async function fetchRoot() {
  return apiRequest("/");
}
