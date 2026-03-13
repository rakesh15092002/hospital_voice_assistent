import API from "./axios";

export const getLiveKitToken = async () => {
  const response = await API.post("/livekit/token");
  const data = response.data;
  // Backend returns livekit_url, frontend needs url
  return {
    token: data.token,
    url: data.livekit_url,
    room: data.room,
    session_id: data.session_id,
  };
};