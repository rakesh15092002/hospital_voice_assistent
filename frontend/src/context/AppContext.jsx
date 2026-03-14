import { createContext, useContext, useState, useRef } from "react";
import { AuthProvider } from "./AuthContext";
import { AppointmentProvider } from "./AppointmentContext";
import { getLiveKitToken } from "../api/livekit";
import { Room, RoomEvent, Track } from "livekit-client";

const AppStateContext = createContext();

export const useApp = () => useContext(AppStateContext);

const AppStateProvider = ({ children }) => {
  const [status, setStatus] = useState("idle");
  const [analyser, setAnalyser] = useState(null);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const roomRef = useRef(null);
  const audioCtxRef = useRef(null);

  const handleMicClick = async () => {
    if (status === "recording") {
      setStatus("idle");
      setAnalyser(null);
      if (roomRef.current) {
        await roomRef.current.localParticipant.setMicrophoneEnabled(false);
        await roomRef.current.disconnect();
        roomRef.current = null;
      }
      if (audioCtxRef.current) {
        audioCtxRef.current.close();
        audioCtxRef.current = null;
      }
      return;
    }
    try {
      setStatus("processing");
      const data = await getLiveKitToken();
      const { token, url, session_id } = data;
      setCurrentSessionId(session_id);

      const room = new Room({
        audioCaptureDefaults: { autoGainControl: true, echoCancellation: true, noiseSuppression: true },
      });
      roomRef.current = room;

      room.on(RoomEvent.TrackSubscribed, (track) => {
        if (track.kind === Track.Kind.Audio) {
          const el = track.attach();
          el.autoplay = true;
          document.body.appendChild(el);
        }
      });

      room.on(RoomEvent.Disconnected, () => {
        setStatus("idle");
        setAnalyser(null);
        setCurrentSessionId(null);
      });

      await room.connect(url, token);
      await room.localParticipant.setMicrophoneEnabled(true);

      const audioCtx = new AudioContext();
      audioCtxRef.current = audioCtx;
      const analyserNode = audioCtx.createAnalyser();
      analyserNode.fftSize = 2048;
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const source = audioCtx.createMediaStreamSource(stream);
      source.connect(analyserNode);

      setAnalyser(analyserNode);
      setStatus("recording");
    } catch (err) {
      console.error("Connection error:", err);
      setStatus("idle");
    }
  };

  return (
    <AppStateContext.Provider value={{ status, analyser, handleMicClick, currentSessionId }}>
      {children}
    </AppStateContext.Provider>
  );
};

const AppContext = ({ children }) => (
  <AuthProvider>
    <AppointmentProvider>
      <AppStateProvider>
        {children}
      </AppStateProvider>
    </AppointmentProvider>
  </AuthProvider>
);

export default AppContext;