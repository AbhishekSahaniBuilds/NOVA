export const API_BASE_URL = import.meta.env.VITE_API_URL;
export const API_VERSION = "v1";

export const API_URL = `${API_BASE_URL}/api/${API_VERSION}`;

if (!API_BASE_URL) {
  throw new Error("VITE_API_URL is not configured.");
}
