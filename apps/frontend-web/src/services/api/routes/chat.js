import { apiRequest } from "../client.js";

export async function fetchChat({
  content,
  message_history = [],
  control_mode = false,
  tool_approval = null,
}) {
  return apiRequest("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content,
      message_history,
      control_mode,
      tool_approval,
    }),
  });
}
