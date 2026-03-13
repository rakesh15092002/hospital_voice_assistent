import API from "./axios";

// Fetch LiveKit token from backend to join voice room
export const getLiveKitToken = async () => {
  const response = await API.post("/livekit/token");
  return response.data;
};