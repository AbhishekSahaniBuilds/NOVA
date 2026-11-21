import { API_VERSION } from "./config";
import { checkAPIHealth } from "./routes/health";

const SUPPORTED_VERSIONS = ["v1"];

let initializationPromise = null;

export function initializeAPI() {
  if (initializationPromise) {
    return initializationPromise;
  }

  initializationPromise = (async () => {
    if (!SUPPORTED_VERSIONS.includes(API_VERSION)) {
      throw new Error(`Unsupported API version: ${API_VERSION}`);
    }

    const health = await checkAPIHealth();

    if (health.status !== "ok") {
      throw new Error("Backend health check failed.");
    }

    if (health.version !== API_VERSION) {
      throw new Error(
        `API version mismatch. Frontend: ${API_VERSION}, Backend: ${health.version}`,
      );
    }

    return {
      initialized: true,
      version: API_VERSION,
      health,
    };
  })().catch((error) => {
    initializationPromise = null;
    throw error;
  });

  return initializationPromise;
}
