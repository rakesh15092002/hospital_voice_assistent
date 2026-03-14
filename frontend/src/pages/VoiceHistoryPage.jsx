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
        background: "#0d1117", /* navbar bg */
        borderBottom: "1px solid #1e2433", /* navbar border */
        height: "65px",
      }}>
        <button onClick={() => navigate("/")} style={{
          width: "36px", height: "36px", borderRadius: "50%",
          background: "#161b27", /* button bg */
          border: "1px solid #1e2433", /* button border */
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
            background: "#2d1515", /* error bg — dark red */
            border: "1px solid #5c2323", /* error border */
            borderRadius: "10px", padding: "12px 16px",
            fontSize: "13px", color: "#f87171", marginBottom: "16px",
          }}>
            {error}
          </div>
        )}

        {loadingSessions ? (
          <div style={{ textAlign: "center", padding: "60px 0" }}>
            <div style={{
              width: "36px", height: "36px",
              border: "3px solid #1a1f2e", /* spinner track */
              borderTop: "3px solid #34d399", /* spinner active */
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
          <div style={{ textAlign: "center", padding: "60px 16px" }}>
            <div style={{
              width: "64px", height: "64px",
              background: "#0d2d20", /* empty state icon bg — dark green */
              border: "1px solid #1a4a33", /* empty state icon border */
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
          <div>
            <p style={{ fontSize: "13px", color: "#475569", marginBottom: "14px" }}>
              {sessions.length} session{sessions.length > 1 ? "s" : ""} found
            </p>

            {sessions.map((session) => (
              <div key={session.id}>
                <div
                  onClick={() => handleSessionClick(session)}
                  style={{
                    background: selectedSession?.id === session.id
                      ? "#0d2d20" /* selected session bg — dark green */
                      : "#0f1420", /* unselected session bg */
                    border: selectedSession?.id === session.id
                      ? "1px solid #1a4a33" /* selected border */
                      : "1px solid #1a2030", /* unselected border */
                    borderRadius: "14px",
                    padding: "14px 16px",
                    marginBottom: "8px",
                    cursor: "pointer",
                    transition: "all 0.2s ease",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                      <div style={{
                        width: "38px", height: "38px", borderRadius: "10px",
                        background: "#0d2d20", /* icon bg — dark green */
                        border: "1px solid #1a4a33", /* icon border */
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
                        {/* ✅ FIXED: created_at → started_at */}
                        <p style={{ fontSize: "11px", color: "#475569", marginTop: "2px" }}>
                          {formatDate(session.started_at)}
                        </p>
                      </div>
                    </div>

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

                {selectedSession?.id === session.id && (
                  <div style={{
                    marginBottom: "12px",
                    marginLeft: "12px",
                    borderLeft: "2px solid #1a4a33", /* thread line — dark green */
                    paddingLeft: "12px",
                  }}>
                    {loadingLogs ? (
                      <div style={{ padding: "20px 0", textAlign: "center" }}>
                        <div style={{
                          width: "24px", height: "24px",
                          border: "2px solid #1a1f2e", /* spinner track */
                          borderTop: "2px solid #34d399", /* spinner active */
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
                          background: "#0d1117", /* log card bg */
                          border: "1px solid #1a1f2e", /* log card border */
                          borderRadius: "10px",
                          padding: "12px",
                          marginBottom: "8px",
                        }}>
                          {log.is_emergency && (
                            <span style={{
                              display: "inline-block",
                              background: "#2d1515", /* emergency badge bg */
                              border: "1px solid #5c2323", /* emergency badge border */
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
                              background: "#0d1a2d", /* user bubble bg — dark blue */
                              border: "1px solid #1a2d4a", /* user bubble border */
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
                                background: "#0d2d20", /* eve bubble bg — dark green */
                                border: "1px solid #1a4a33", /* eve bubble border */
                                borderRadius: "8px", padding: "8px 10px",
                              }}>
                                {log.ai_response}
                              </p>
                            </div>
                          )}

                          {/* Timestamp */}
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