import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getMySessions, getSessionLogs } from "../api/voice";

const VoiceHistoryPage = () => {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loadingSessions, setLoadingSessions] = useState(true);
  const [loadingLogs, setLoadingLogs] = useState(false);
  const [error, setError] = useState("");

  // Fetch all sessions on mount
  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      setLoadingSessions(true);
      const data = await getMySessions();
      setSessions(data);
    } catch (err) {
      setError("Failed to load sessions.");
    } finally {
      setLoadingSessions(false);
    }
  };

  // Fetch logs when session is selected
  const handleSessionClick = async (session) => {
    if (selectedSession?.id === session.id) {
      setSelectedSession(null);
      setLogs([]);
      return;
    }
    setSelectedSession(session);
    setLoadingLogs(true);
    try {
      const data = await getSessionLogs(session.id);
      setLogs(data);
    } catch (err) {
      setError("Failed to load logs.");
    } finally {
      setLoadingLogs(false);
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "N/A";
    return new Date(dateStr).toLocaleString("en-IN", {
      day: "numeric", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  };

  return (
    <div style={{ minHeight: "100vh", background: "#0a0f1e" }}>

      {/* Navbar */}
      <div style={{
        display: "flex", alignItems: "center", gap: "14px",
        padding: "14px 20px",
        background: "rgba(255,255,255,0.02)",
        borderBottom: "1px solid rgba(255,255,255,0.05)",
        height: "65px",
      }}>
        <button onClick={() => navigate("/")} style={{
          width: "36px", height: "36px", borderRadius: "50%",
          background: "rgba(255,255,255,0.04)",
          border: "1px solid rgba(255,255,255,0.08)",
          display: "flex", alignItems: "center", justifyContent: "center",
          cursor: "pointer",
        }}>
          <svg width="18" height="18" fill="#94a3b8" viewBox="0 0 24 24">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
          </svg>
        </button>
        <div>
          <p style={{ fontSize: "15px", fontWeight: "600", color: "#f1f5f9" }}>Voice History</p>
          <p style={{ fontSize: "11px", color: "#475569" }}>All sessions and conversation logs</p>
        </div>
      </div>

      <div style={{ maxWidth: "480px", margin: "0 auto", padding: "20px 16px" }}>

        {error && (
          <div style={{
            background: "rgba(248,113,113,0.1)",
            border: "1px solid rgba(248,113,113,0.2)",
            borderRadius: "10px", padding: "12px 16px",
            fontSize: "13px", color: "#f87171", marginBottom: "16px",
          }}>
            {error}
          </div>
        )}

        {/* Loading sessions */}
        {loadingSessions ? (
          <div style={{ textAlign: "center", padding: "60px 0" }}>
            <div style={{
              width: "36px", height: "36px",
              border: "3px solid rgba(255,255,255,0.05)",
              borderTop: "3px solid #34d399",
              borderRadius: "50%",
              animation: "spin 0.8s linear infinite",
              margin: "0 auto",
            }} />
            <p style={{ fontSize: "13px", color: "#475569", marginTop: "12px" }}>
              Loading sessions...
            </p>
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
          </div>
        ) : sessions.length === 0 ? (
          /* Empty state */
          <div style={{ textAlign: "center", padding: "60px 16px" }}>
            <div style={{
              width: "64px", height: "64px",
              background: "rgba(52,211,153,0.1)",
              border: "1px solid rgba(52,211,153,0.15)",
              borderRadius: "50%",
              display: "flex", alignItems: "center", justifyContent: "center",
              margin: "0 auto 16px",
            }}>
              <svg width="28" height="28" fill="#34d399" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z" />
              </svg>
            </div>
            <p style={{ fontSize: "15px", fontWeight: "600", color: "#f1f5f9" }}>No sessions yet</p>
            <p style={{ fontSize: "13px", color: "#475569", marginTop: "6px" }}>
              Start a voice call with Eve to see history here
            </p>
          </div>
        ) : (
          /* Sessions list */
          <div>
            <p style={{ fontSize: "13px", color: "#475569", marginBottom: "14px" }}>
              {sessions.length} session{sessions.length > 1 ? "s" : ""} found
            </p>

            {sessions.map((session) => (
              <div key={session.id}>
                {/* Session card */}
                <div
                  onClick={() => handleSessionClick(session)}
                  style={{
                    background: selectedSession?.id === session.id
                      ? "rgba(52,211,153,0.05)"
                      : "rgba(255,255,255,0.03)",
                    border: selectedSession?.id === session.id
                      ? "1px solid rgba(52,211,153,0.2)"
                      : "1px solid rgba(255,255,255,0.07)",
                    borderRadius: "14px",
                    padding: "14px 16px",
                    marginBottom: "8px",
                    cursor: "pointer",
                    transition: "all 0.2s ease",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                      {/* Icon */}
                      <div style={{
                        width: "38px", height: "38px", borderRadius: "10px",
                        background: "rgba(52,211,153,0.1)",
                        border: "1px solid rgba(52,211,153,0.2)",
                        display: "flex", alignItems: "center", justifyContent: "center",
                      }}>
                        <svg width="18" height="18" fill="#34d399" viewBox="0 0 24 24">
                          <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z" />
                        </svg>
                      </div>
                      <div>
                        <p style={{ fontSize: "13px", fontWeight: "600", color: "#f1f5f9" }}>
                          Session #{session.id}
                        </p>
                        <p style={{ fontSize: "11px", color: "#475569", marginTop: "2px" }}>
                          {formatDate(session.created_at)}
                        </p>
                      </div>
                    </div>

                    {/* Arrow */}
                    <svg
                      width="16" height="16" fill="#475569" viewBox="0 0 24 24"
                      style={{
                        transform: selectedSession?.id === session.id ? "rotate(90deg)" : "rotate(0deg)",
                        transition: "transform 0.2s ease",
                      }}
                    >
                      <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z" />
                    </svg>
                  </div>
                </div>

                {/* Logs expanded */}
                {selectedSession?.id === session.id && (
                  <div style={{
                    marginBottom: "12px",
                    marginLeft: "12px",
                    borderLeft: "2px solid rgba(52,211,153,0.2)",
                    paddingLeft: "12px",
                  }}>
                    {loadingLogs ? (
                      <div style={{ padding: "20px 0", textAlign: "center" }}>
                        <div style={{
                          width: "24px", height: "24px",
                          border: "2px solid rgba(255,255,255,0.05)",
                          borderTop: "2px solid #34d399",
                          borderRadius: "50%",
                          animation: "spin 0.8s linear infinite",
                          margin: "0 auto",
                        }} />
                      </div>
                    ) : logs.length === 0 ? (
                      <p style={{ fontSize: "13px", color: "#475569", padding: "12px 0" }}>
                        No conversation logs for this session.
                      </p>
                    ) : (
                      logs.map((log) => (
                        <div key={log.id} style={{
                          background: "rgba(255,255,255,0.02)",
                          border: "1px solid rgba(255,255,255,0.05)",
                          borderRadius: "10px",
                          padding: "12px",
                          marginBottom: "8px",
                        }}>
                          {/* Emergency badge */}
                          {log.is_emergency && (
                            <span style={{
                              display: "inline-block",
                              background: "rgba(248,113,113,0.1)",
                              border: "1px solid rgba(248,113,113,0.2)",
                              color: "#f87171",
                              fontSize: "10px", fontWeight: "600",
                              padding: "2px 8px", borderRadius: "20px",
                              marginBottom: "8px",
                            }}>
                              🚨 EMERGENCY
                            </span>
                          )}

                          {/* User transcript */}
                          <div style={{ marginBottom: "8px" }}>
                            <p style={{ fontSize: "10px", color: "#475569", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                              You said
                            </p>
                            <p style={{
                              fontSize: "13px", color: "#94a3b8",
                              background: "rgba(96,165,250,0.05)",
                              border: "1px solid rgba(96,165,250,0.1)",
                              borderRadius: "8px", padding: "8px 10px",
                            }}>
                              {log.transcript}
                            </p>
                          </div>

                          {/* Eve response */}
                          {log.ai_response && (
                            <div>
                              <p style={{ fontSize: "10px", color: "#475569", marginBottom: "4px", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                                Eve replied
                              </p>
                              <p style={{
                                fontSize: "13px", color: "#a7f3d0",
                                background: "rgba(52,211,153,0.05)",
                                border: "1px solid rgba(52,211,153,0.1)",
                                borderRadius: "8px", padding: "8px 10px",
                              }}>
                                {log.ai_response}
                              </p>
                            </div>
                          )}

                          {/* Time */}
                          <p style={{ fontSize: "10px", color: "#334155", marginTop: "8px" }}>
                            {formatDate(log.created_at)}
                          </p>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default VoiceHistoryPage;