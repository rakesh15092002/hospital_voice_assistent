import API from "./axios";

// Get all voice sessions
export const getMySessions = async () => {
  const response = await API.get("/voice/sessions");
  return response.data;
};

// Get logs for a specific session
export const getSessionLogs = async (sessionId) => {
  const response = await API.get(`/voice/sessions/${sessionId}/logs`);
  return response.data;
};