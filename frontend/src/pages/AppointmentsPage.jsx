import { useNavigate } from "react-router-dom";
import Navbar from "../components/common/Navbar";
import AppointmentList from "../components/appointment/AppointmentList";

const AppointmentsPage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: "100vh", background: "#f0f4ff" }}>
      {/* Top navbar */}
      <Navbar />

      <div
        style={{
          maxWidth: "480px",
          margin: "0 auto",
          padding: "20px 16px",
        }}
      >
        {/* Header */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "20px",
          }}
        >
          {/* Back button */}
          <button
            onClick={() => navigate("/")}
            style={{
              width: "36px",
              height: "36px",
              borderRadius: "50%",
              background: "white",
              border: "1px solid #e2e8f0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
            }}
          >
            <svg width="18" height="18" fill="#64748b" viewBox="0 0 24 24">
              <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
            </svg>
          </button>

          <div>
            <h1
              style={{
                fontSize: "18px",
                fontWeight: "600",
                color: "#1e293b",
              }}
            >
              My Appointments
            </h1>
            <p style={{ fontSize: "12px", color: "#94a3b8", marginTop: "2px" }}>
              View and manage your bookings
            </p>
          </div>
        </div>

        {/* Appointments list */}
        <AppointmentList />
      </div>
    </div>
  );
};

export default AppointmentsPage;