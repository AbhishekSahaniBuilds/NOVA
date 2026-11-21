import { apiRequest } from "../client";

export async function checkAPIHealth() {
  return apiRequest("/health");
}
