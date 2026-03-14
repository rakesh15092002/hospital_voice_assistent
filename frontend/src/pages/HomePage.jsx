import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useApp } from "../context/AppContext";
import MicButton from "../components/voice/MicButton";
import Waveform from "../components/voice/Waveform";
import QuickActions from "../components/voice/QuickActions";
import ChatBubble from "../components/voice/ChatBubble";
import { useState, useEffect, useRef } from "react";
import { getSessionLogs } from "../api/voice";

const HomePage = () => {
  const { user, logout } = useAuth();
  const { status, currentSessionId } = useApp();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm Eve, your hospital assistant. How can I help you today?", isUser: false },
  ]);
  const [typedMessage, setTypedMessage] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    let interval;
    if (status === "recording" && currentSessionId) {
      interval = setInterval(async () => {
        try {
          const logs = await getSessionLogs(currentSessionId);
          const newMessages = logs.map(log => [
            { id: `user-${log.id}`, text: log.transcript, isUser: true },
            log.ai_response ? { id: `eve-${log.id}`, text: log.ai_response, isUser: false } : null
          ]).flat().filter(Boolean);
          setMessages(prev => {
            // Avoid duplicates by checking ids
            const existingIds = new Set(prev.map(m => m.id));
            const uniqueNew = newMessages.filter(m => !existingIds.has(m.id));
            return [...prev, ...uniqueNew];
          });
        } catch (err) {
          console.error("Failed to fetch logs:", err);
        }
      }, 2000); // Poll every 2 seconds
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [status, currentSessionId]);

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

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div style={{
      height: "100vh",
      background: "#0a0f1e",
      display: "flex",
      flexDirection: "column",
      overflow: "hidden",
    }}>

      {/* Navbar */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "0 24px",
        background: "rgba(255,255,255,0.02)",
        borderBottom: "1px solid rgba(255,255,255,0.05)",
        height: "60px",
        flexShrink: 0,
      }}>
        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <div style={{
            width: "32px", height: "32px",
            background: "rgba(52,211,153,0.1)",
            border: "1px solid rgba(52,211,153,0.2)",
            borderRadius: "8px",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}>
            <svg width="16" height="16" fill="#34d399" viewBox="0 0 24 24">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z" />
            </svg>
          </div>
          <div>
            <p style={{ fontSize: "13px", fontWeight: "600", color: "#f1f5f9" }}>City Care Hospital</p>
            <p style={{ fontSize: "10px", color: "#475569" }}>Your Health, Our Priority</p>
          </div>
        </div>

        {/* Right side */}
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          {/* Live indicator */}
          <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <div style={{
              width: "7px", height: "7px", borderRadius: "50%",
              background: status === "recording" ? "#34d399" : "#334155",
              boxShadow: status === "recording" ? "0 0 8px #34d399" : "none",
              animation: status === "recording" ? "pulse 1.5s infinite" : "none",
            }} />
            <span style={{ fontSize: "11px", color: status === "recording" ? "#34d399" : "#475569" }}>
              {status === "recording" ? "Live" : "Offline"}
            </span>
          </div>

          <button onClick={() => navigate("/appointments")} style={{
            fontSize: "12px", background: "rgba(255,255,255,0.04)",
            border: "1px solid rgba(255,255,255,0.08)",
            padding: "6px 12px", borderRadius: "8px",
            cursor: "pointer", color: "#94a3b8",
          }}>
            Appointments
          </button>

          <button onClick={() => navigate("/history")} style={{
            fontSize: "12px", background: "rgba(255,255,255,0.04)",
            border: "1px solid rgba(255,255,255,0.08)",
            padding: "6px 12px", borderRadius: "8px",
            cursor: "pointer", color: "#94a3b8",
          }}>
            History
          </button>

          <div style={{
            width: "30px", height: "30px", borderRadius: "50%",
            background: "rgba(52,211,153,0.1)",
            border: "1px solid rgba(52,211,153,0.2)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: "12px", fontWeight: "700", color: "#34d399",
          }}>
            {user?.name?.charAt(0).toUpperCase()}
          </div>

          <button onClick={handleLogout} style={{
            fontSize: "12px", background: "transparent",
            border: "1px solid rgba(255,255,255,0.08)",
            padding: "6px 12px", borderRadius: "8px",
            cursor: "pointer", color: "#94a3b8",
          }}>
            Logout
          </button>
        </div>
      </div>

      {/* Main 2-column layout */}
      <div style={{
        flex: 1,
        display: "flex",
        overflow: "hidden",
      }}>

        {/* LEFT SIDE — Mic + Waveform + Quick Actions */}
        <div style={{
          width: "680px",
          flexShrink: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "32px 24px",
          borderRight: "1px solid rgba(255,255,255,0.05)",
          gap: "32px",
          position: "relative",
        }}>
          {/* Background glow */}
          <div style={{
            position: "absolute",
            width: "280px", height: "280px",
            background: "radial-gradient(circle, rgba(52,211,153,0.06) 0%, transparent 70%)",
            pointerEvents: "none",
          }} />

          {/* Eve label */}
          <div style={{ textAlign: "center" }}>
            <div style={{
              display: "inline-flex", alignItems: "center", gap: "8px",
              background: "rgba(52,211,153,0.08)",
              border: "1px solid rgba(52,211,153,0.15)",
              borderRadius: "20px", padding: "6px 16px",
            }}>
              <div style={{
                width: "8px", height: "8px", borderRadius: "50%",
                background: status === "recording" ? "#34d399" : "#334155",
                animation: status === "recording" ? "pulse 1.5s infinite" : "none",
              }} />
              <span style={{ fontSize: "13px", color: "#34d399", fontWeight: "600" }}>
                Eve — AI Assistant
              </span>
            </div>
            <p style={{ fontSize: "12px", color: "#475569", marginTop: "8px" }}>
              {status === "idle" && "Tap mic to start voice session"}
              {status === "processing" && "Connecting to Eve..."}
              {status === "recording" && "Eve is listening to you"}
            </p>
          </div>

          {/* Mic button */}
          <MicButton />

          {/* Waveform */}
          <div style={{ width: "100%" }}>
            <Waveform />
          </div>

          {/* Quick actions */}
          <div style={{ width: "100%" }}>
            <p style={{ fontSize: "11px", color: "#334155", textAlign: "center", marginBottom: "10px", textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Quick Actions
            </p>
            <QuickActions onActionClick={(label) => {
              setMessages((prev) => [
                ...prev,
                { id: Date.now(), text: label, isUser: true },
                { id: Date.now() + 1, text: `Sure! I can help you with ${label}. Start the voice call or type below.`, isUser: false },
              ]);
            }} />
          </div>
        </div>

        {/* RIGHT SIDE — Transcript + Input */}
        <div style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}>

          {/* Chat header */}
          <div style={{
            padding: "16px 24px",
            borderBottom: "1px solid rgba(255,255,255,0.05)",
            display: "flex", alignItems: "center", justifyContent: "space-between",
            flexShrink: 0,
          }}>
            <div>
              <p style={{ fontSize: "14px", fontWeight: "600", color: "#f1f5f9" }}>Live Transcript</p>
              <p style={{ fontSize: "11px", color: "#475569" }}>
                {messages.length - 1} messages in this session
              </p>
            </div>
            <button
              onClick={() => setMessages([{ id: 1, text: "Hello! I'm Eve, your hospital assistant. How can I help you today?", isUser: false }])}
              style={{
                fontSize: "11px", color: "#475569",
                background: "rgba(255,255,255,0.03)",
                border: "1px solid rgba(255,255,255,0.07)",
                padding: "5px 12px", borderRadius: "6px",
                cursor: "pointer",
              }}
            >
              Clear
            </button>
          </div>

          {/* Messages */}
          <div style={{
            flex: 1,
            overflowY: "auto",
            padding: "20px 24px",
            display: "flex",
            flexDirection: "column",
          }}>
            {messages.map((msg) => (
              <ChatBubble key={msg.id} message={msg.text} isUser={msg.isUser} />
            ))}
            <div ref={chatEndRef} />
          </div>

          {/* Input */}
          <div style={{
            padding: "16px 24px",
            borderTop: "1px solid rgba(255,255,255,0.05)",
            flexShrink: 0,
          }}>
            <form onSubmit={handleTypedSubmit} style={{ display: "flex", gap: "10px", alignItems: "center" }}>
              <input
                type="text"
                value={typedMessage}
                onChange={(e) => setTypedMessage(e.target.value)}
                placeholder="Type a message to Eve..."
                style={{
                  flex: 1,
                  padding: "12px 18px",
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
                flexShrink: 0,
              }}>
                <svg width="18" height="18" fill="white" viewBox="0 0 24 24">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                </svg>
              </button>
            </form>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </div>
  );
};

export default HomePage;