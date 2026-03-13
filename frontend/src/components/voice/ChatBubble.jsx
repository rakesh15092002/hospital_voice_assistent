const ChatBubble = ({ message, isUser }) => {
  return (
    <div style={{
      display: "flex",
      justifyContent: isUser ? "flex-end" : "flex-start",
      alignItems: "flex-end",
      gap: "8px",
      marginBottom: "12px",
    }}>
      {!isUser && (
        <div style={{
          width: "32px", height: "32px", borderRadius: "50%",
          background: "rgba(52,211,153,0.1)",
          border: "1px solid rgba(52,211,153,0.2)",
          display: "flex", alignItems: "center", justifyContent: "center",
          flexShrink: 0,
        }}>
          <svg width="16" height="16" fill="#34d399" viewBox="0 0 24 24">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z" />
          </svg>
        </div>
      )}

      <div style={{
        maxWidth: "72%",
        padding: "10px 14px",
        borderRadius: isUser ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
        background: isUser ? "rgba(52,211,153,0.15)" : "rgba(255,255,255,0.05)",
        color: isUser ? "#a7f3d0" : "#cbd5e1",
        fontSize: "14px",
        lineHeight: "1.5",
        border: isUser ? "1px solid rgba(52,211,153,0.2)" : "1px solid rgba(255,255,255,0.06)",
      }}>
        {message}
      </div>

      {isUser && (
        <div style={{
          width: "32px", height: "32px", borderRadius: "50%",
          background: "rgba(96,165,250,0.1)",
          border: "1px solid rgba(96,165,250,0.2)",
          display: "flex", alignItems: "center", justifyContent: "center",
          flexShrink: 0,
        }}>
          <svg width="16" height="16" fill="#60a5fa" viewBox="0 0 24 24">
            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
          </svg>
        </div>
      )}
    </div>
  );
};

export default ChatBubble;