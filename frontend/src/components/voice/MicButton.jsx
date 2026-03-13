import { useState } from "react";

const MicButton = ({ onStart, onStop }) => {
  const [isListening, setIsListening] = useState(false);

  // Toggle mic on/off and call parent handlers
  const handleClick = () => {
    if (isListening) {
      setIsListening(false);
      onStop && onStop();
    } else {
      setIsListening(true);
      onStart && onStart();
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      {/* Outer pulse ring - only shows when listening */}
      <div
        style={{
          display: "inline-block",
          borderRadius: "50%",
          padding: "12px",
          background: isListening ? "rgba(26, 86, 219, 0.1)" : "transparent",
          animation: isListening ? "pulse 1.5s infinite" : "none",
        }}
      >
        {/* Mic button */}
        <div
          onClick={handleClick}
          style={{
            width: "90px",
            height: "90px",
            borderRadius: "50%",
            background: isListening ? "#ef4444" : "#1a56db",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            boxShadow: isListening
              ? "0 0 0 8px rgba(239, 68, 68, 0.15)"
              : "0 0 0 8px rgba(26, 86, 219, 0.15)",
            transition: "all 0.3s ease",
          }}
        >
          <svg width="36" height="36" fill="white" viewBox="0 0 24 24">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z" />
          </svg>
        </div>
      </div>

      {/* Status text */}
      <p
        style={{
          marginTop: "12px",
          fontSize: "14px",
          fontWeight: "500",
          color: isListening ? "#ef4444" : "#64748b",
        }}
      >
        {isListening ? "Listening... Tap to stop" : "Tap to Speak"}
      </p>

      <style>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.08); opacity: 0.8; }
        }
      `}</style>
    </div>
  );
};

export default MicButton;