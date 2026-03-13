import { useState, useEffect, useRef } from "react";
import { useApp } from "../../context/AppContext";
import MicButton from "./MicButton";
import Waveform from "./Waveform";
import ChatBubble from "./ChatBubble";
import QuickActions from "./QuickActions";

const VoiceRoom = () => {
  const { status } = useApp();
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm Eve, your hospital assistant. How can I help you today?", isUser: false },
  ]);
  const [typedMessage, setTypedMessage] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const addMessage = (text, isUser) => {
    setMessages((prev) => [...prev, { id: Date.now(), text, isUser }]);
  };

  const handleQuickAction = (label) => {
    addMessage(label, true);
    setTimeout(() => addMessage(`Sure! I can help you with ${label}. Start the voice call or type your question.`, false), 800);
  };

  const handleTypedSubmit = (e) => {
    e.preventDefault();
    if (!typedMessage.trim()) return;
    addMessage(typedMessage, true);
    setTypedMessage("");
    setTimeout(() => addMessage("Please start the voice call so Eve can assist you better.", false), 800);
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "calc(100vh - 65px)",
      background: "#0a0f1e",
      maxWidth: "480px",
      margin: "0 auto",
      position: "relative",
    }}>
      {/* Background glow */}
      <div style={{
        position: "absolute", top: "30%", left: "50%", transform: "translateX(-50%)",
        width: "300px", height: "300px",
        background: "radial-gradient(circle, rgba(52,211,153,0.04) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />

      {/* Chat area */}
      <div style={{ flex: 1, overflowY: "auto", padding: "16px", display: "flex", flexDirection: "column" }}>
        {messages.map((msg) => (
          <ChatBubble key={msg.id} message={msg.text} isUser={msg.isUser} />
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* Mic + Waveform */}
      <div style={{ padding: "16px 16px 8px", display: "flex", flexDirection: "column", alignItems: "center", gap: "16px" }}>
        <MicButton />
        <div style={{ width: "100%" }}>
          <Waveform />
        </div>
      </div>

      {/* Text input */}
      <form onSubmit={handleTypedSubmit} style={{ display: "flex", alignItems: "center", gap: "10px", padding: "8px 16px" }}>
        <input
          type="text"
          value={typedMessage}
          onChange={(e) => setTypedMessage(e.target.value)}
          placeholder="Or type your question..."
          style={{
            flex: 1, padding: "12px 16px",
            background: "rgba(255,255,255,0.04)",
            border: "1px solid rgba(255,255,255,0.08)",
            borderRadius: "50px",
            fontSize: "14px", outline: "none",
            color: "#f1f5f9",
          }}
        />
        <button type="submit" style={{
          width: "44px", height: "44px", borderRadius: "50%",
          background: "linear-gradient(135deg, #34d399, #059669)",
          border: "none", cursor: "pointer",
          display: "flex", alignItems: "center", justifyContent: "center",
          boxShadow: "0 0 16px rgba(52,211,153,0.3)",
        }}>
          <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        </button>
      </form>

      {/* Quick actions */}
      <div style={{ padding: "8px 16px 16px" }}>
        <QuickActions onActionClick={handleQuickAction} />
      </div>
    </div>
  );
};

export default VoiceRoom;