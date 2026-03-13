import { useNavigate } from "react-router-dom";
import AppointmentList from "../components/appointment/AppointmentList";

const AppointmentsPage = () => {
  const navigate = useNavigate();

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
          <p style={{ fontSize: "15px", fontWeight: "600", color: "#f1f5f9" }}>My Appointments</p>
          <p style={{ fontSize: "11px", color: "#475569" }}>View and manage your bookings</p>
        </div>
      </div>

      <div style={{ maxWidth: "480px", margin: "0 auto", padding: "20px 16px" }}>
        <AppointmentList />
      </div>
    </div>
  );
};

export default AppointmentsPage;