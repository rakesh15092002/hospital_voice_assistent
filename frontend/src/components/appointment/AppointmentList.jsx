import { useEffect } from "react";
import { useAppointment } from "../../context/AppointmentContext";
import AppointmentCard from "./AppointmentCard";

const AppointmentList = () => {
  const { appointments, loading, error, fetchAppointments } = useAppointment();

  // Fetch appointments on component mount
  useEffect(() => {
    fetchAppointments();
  }, [fetchAppointments]);

  // Loading state
  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "40px 0" }}>
        <div
          style={{
            width: "36px",
            height: "36px",
            border: "3px solid #e2e8f0",
            borderTop: "3px solid #1a56db",
            borderRadius: "50%",
            animation: "spin 0.8s linear infinite",
            margin: "0 auto",
          }}
        />
        <p style={{ fontSize: "13px", color: "#94a3b8", marginTop: "12px" }}>
          Loading appointments...
        </p>
        <style>{`
          @keyframes spin {
            0%   { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div
        style={{
          background: "#fef2f2",
          border: "1px solid #fecaca",
          borderRadius: "10px",
          padding: "16px",
          textAlign: "center",
        }}
      >
        <p style={{ fontSize: "13px", color: "#dc2626" }}>{error}</p>
        <button
          onClick={fetchAppointments}
          style={{
            marginTop: "10px",
            padding: "8px 16px",
            background: "#1a56db",
            color: "white",
            border: "none",
            borderRadius: "8px",
            fontSize: "13px",
            cursor: "pointer",
          }}
        >
          Try Again
        </button>
      </div>
    );
  }

  // Empty state
  if (appointments.length === 0) {
    return (
      <div style={{ textAlign: "center", padding: "40px 16px" }}>
        <div
          style={{
            width: "64px",
            height: "64px",
            background: "#e6f1fb",
            borderRadius: "50%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            margin: "0 auto 16px",
          }}
        >
          <svg width="28" height="28" fill="#1a56db" viewBox="0 0 24 24">
            <path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z" />
          </svg>
        </div>
        <p style={{ fontSize: "15px", fontWeight: "600", color: "#1e293b" }}>
          No appointments yet
        </p>
        <p style={{ fontSize: "13px", color: "#94a3b8", marginTop: "4px" }}>
          Talk to Eve to book your first appointment
        </p>
      </div>
    );
  }

  // Appointments list
  return (
    <div>
      {/* Count */}
      <p
        style={{
          fontSize: "13px",
          color: "#64748b",
          marginBottom: "12px",
        }}
      >
        {appointments.length} appointment{appointments.length > 1 ? "s" : ""} found
      </p>

      {/* Cards */}
      {appointments.map((appointment) => (
        <AppointmentCard key={appointment.id} appointment={appointment} />
      ))}
    </div>
  );
};

export default AppointmentList;