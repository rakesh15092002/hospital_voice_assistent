import { useApp } from "../../context/AppContext";

const MicButton = () => {
  const { status, handleMicClick } = useApp();
  const isRecording = status === "recording";
  const isProcessing = status === "processing";

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "12px" }}>
      {/* Ripple + button wrapper */}
      <div style={{ position: "relative", display: "flex", alignItems: "center", justifyContent: "center", width: "112px", height: "112px" }}>
        {isRecording && (
          <>
            <span style={{
              position: "absolute", inset: 0, borderRadius: "50%",
              border: "1px solid rgba(52,211,153,0.3)",
              animation: "ping 1.5s ease-out infinite",
            }} />
            <span style={{
              position: "absolute", inset: "-8px", borderRadius: "50%",
              border: "1px solid rgba(52,211,153,0.15)",
              animation: "ping 1.5s ease-out infinite 0.4s",
            }} />
          </>
        )}

        <button
          onClick={handleMicClick}
          disabled={isProcessing}
          style={{
            width: "96px", height: "96px",
            borderRadius: "50%",
            border: isRecording ? "1px solid rgba(52,211,153,0.4)" : "1px solid rgba(255,255,255,0.1)",
            background: isRecording
              ? "rgba(6,78,59,0.8)"
              : "linear-gradient(135deg, #1e293b, #0f172a)",
            color: "#34d399",
            display: "flex", alignItems: "center", justifyContent: "center",
            cursor: isProcessing ? "not-allowed" : "pointer",
            opacity: isProcessing ? 0.6 : 1,
            transition: "all 0.3s ease",
            boxShadow: isRecording
              ? "0 0 40px rgba(52,211,153,0.4)"
              : "0 8px 32px rgba(0,0,0,0.5)",
            transform: isRecording ? "scale(1.05)" : "scale(1)",
          }}
        >
          {isProcessing ? (
            <svg style={{ width: "32px", height: "32px", animation: "spin 1s linear infinite", color: "#fbbf24" }} viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeOpacity="0.25" />
              <path fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 100 16v-4l-3 3 3 3v-4a8 8 0 01-8-8z" />
            </svg>
          ) : isRecording ? (
            <svg style={{ width: "32px", height: "32px" }} viewBox="0 0 24 24" fill="currentColor">
              <rect x="6" y="6" width="12" height="12" rx="2" />
            </svg>
          ) : (
            <svg style={{ width: "32px", height: "32px" }} viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 1a4 4 0 0 1 4 4v6a4 4 0 0 1-8 0V5a4 4 0 0 1 4-4z" />
              <path d="M19 10a1 1 0 0 0-2 0 5 5 0 0 1-10 0 1 1 0 0 0-2 0 7 7 0 0 0 6 6.93V19H9a1 1 0 0 0 0 2h6a1 1 0 0 0 0-2h-2v-2.07A7 7 0 0 0 19 10z" />
            </svg>
          )}
        </button>
      </div>

      {/* Status text */}
      <p style={{ fontSize: "13px", fontWeight: "500", color: isRecording ? "#34d399" : "#475569" }}>
        {isProcessing ? "Connecting..." : isRecording ? "Listening... Tap to stop" : "Tap to Speak"}
      </p>

      <style>{`
        @keyframes ping {
          0% { transform: scale(1); opacity: 1; }
          100% { transform: scale(1.5); opacity: 0; }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default MicButton;