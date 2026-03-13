import { useState, useEffect, useRef } from "react";
import { useAuth } from "../../context/AuthContext";
import { getLiveKitToken } from "../../api/livekit";
import { Room, RoomEvent, Track } from "livekit-client";
import MicButton from "./MicButton";
import ChatBubble from "./ChatBubble";
import QuickActions from "./QuickActions";

const VoiceRoom = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm Eve, your hospital assistant. How can I help you today?",
      isUser: false,
    },
  ]);
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState("");
  const [typedMessage, setTypedMessage] = useState("");
  const chatEndRef = useRef(null);
  const roomRef = useRef(null);

  // Auto scroll to bottom when new message arrives
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Cleanup room on unmount
  useEffect(() => {
    return () => {
      if (roomRef.current) {
        roomRef.current.disconnect();
      }
    };
  }, []);

  // Add a new message to chat
  const addMessage = (text, isUser) => {
    setMessages((prev) => [...prev, { id: Date.now(), text, isUser }]);
  };

  // Connect to LiveKit room and start real voice session
  const handleStart = async () => {
    try {
      setIsConnecting(true);
      setError("");

      // 1. Get token and URL from backend
      const data = await getLiveKitToken();
      
      // ✅ FIX: Backend sends 'livekit_url', not 'url'
      const { token, livekit_url } = data;

      if (!livekit_url || !token) {
        throw new Error("Connection details missing from server.");
      }

      // 2. Create LiveKit room
      const room = new Room({
        audioCaptureDefaults: {
          autoGainControl: true,
          echoCancellation: true,
          noiseSuppression: true,
        },
      });

      roomRef.current = room;

      // Listen for agent audio track - Eve's voice
      room.on(RoomEvent.TrackSubscribed, (track) => {
        if (track.kind === Track.Kind.Audio) {
          const audioElement = track.attach();
          audioElement.autoplay = true;
          document.body.appendChild(audioElement);
          addMessage("Eve is speaking...", false);
        }
      });

      // Listen for data messages from agent
      room.on(RoomEvent.DataReceived, (payload) => {
        try {
          const message = JSON.parse(new TextDecoder().decode(payload));
          if (message.text) {
            addMessage(message.text, false);
          }
        } catch (e) {
          // Not a JSON message
        }
      });

      // Room disconnected
      room.on(RoomEvent.Disconnected, () => {
        setIsConnected(false);
        addMessage("Call ended. Tap mic to start again.", false);
      });

      // 3. Connect to LiveKit cloud using the corrected variable
      await room.connect(livekit_url, token);

      // 4. Enable microphone
      await room.localParticipant.setMicrophoneEnabled(true);

      setIsConnected(true);
      addMessage("Connected! Eve is listening. Please speak now.", false);
    } catch (err) {
      console.error("LiveKit connection error:", err);
      setError("Failed to connect. Make sure your LiveKit URL and token are valid.");
      setIsConnected(false);
    } finally {
      setIsConnecting(false);
    }
  };

  // Disconnect from LiveKit room
  const handleStop = async () => {
    if (roomRef.current) {
      try {
        await roomRef.current.localParticipant.setMicrophoneEnabled(false);
        await roomRef.current.disconnect();
      } catch (e) {
        console.error("Error during disconnect:", e);
      }
      roomRef.current = null;
    }
    setIsConnected(false);
    addMessage("Call ended. Tap mic to start again.", false);
  };

  // Handle quick action button click
  const handleQuickAction = (label) => {
    addMessage(label, true);
    setTimeout(() => {
      addMessage(
        `Sure! I can help you with ${label}. Please start the voice call or type your question.`,
        false
      );
    }, 800);
  };

  // Handle typed message submit
  const handleTypedSubmit = (e) => {
    e.preventDefault();
    if (!typedMessage.trim()) return;
    addMessage(typedMessage, true);
    setTypedMessage("");
    setTimeout(() => {
      addMessage(
        "Please start the voice call so Eve can assist you better.",
        false
      );
    }, 800);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "calc(100vh - 65px)",
        background: "#f0f4ff",
        maxWidth: "480px",
        margin: "0 auto",
      }}
    >
      {/* Chat messages area */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "16px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {messages.map((msg) => (
          <ChatBubble key={msg.id} message={msg.text} isUser={msg.isUser} />
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* Error message */}
      {error && (
        <div
          style={{
            margin: "0 16px",
            padding: "10px 14px",
            background: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: "8px",
            fontSize: "13px",
            color: "#dc2626",
          }}
        >
          {error}
        </div>
      )}

      {/* Mic button */}
      <div style={{ padding: "20px 16px 12px" }}>
        {isConnecting ? (
          <div style={{ textAlign: "center", color: "#64748b", fontSize: "14px" }}>
            Connecting to Eve...
          </div>
        ) : (
          <MicButton onStart={handleStart} onStop={handleStop} isConnected={isConnected} />
        )}
      </div>

      {/* Type message input */}
      <form
        onSubmit={handleTypedSubmit}
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
          padding: "0 16px 12px",
        }}
      >
        <input
          type="text"
          value={typedMessage}
          onChange={(e) => setTypedMessage(e.target.value)}
          placeholder="Or type your question..."
          style={{
            flex: 1,
            padding: "12px 16px",
            border: "1px solid #e2e8f0",
            borderRadius: "50px",
            fontSize: "14px",
            outline: "none",
            background: "white",
            color: "#1e293b",
          }}
        />
        <button
          type="submit"
          style={{
            width: "44px",
            height: "44px",
            borderRadius: "50%",
            background: "#1a56db",
            border: "none",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        </button>
      </form>

      {/* Quick action buttons */}
      <div style={{ padding: "0 0 16px" }}>
        <QuickActions onActionClick={handleQuickAction} />
      </div>
    </div>
  );
};

export default VoiceRoom;