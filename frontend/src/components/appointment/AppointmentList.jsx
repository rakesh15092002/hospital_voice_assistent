import { useEffect } from "react";
import { useAppointment } from "../../context/AppointmentContext";
import AppointmentCard from "./AppointmentCard";

const AppointmentList = () => {
  const { appointments, loading, error, fetchAppointments } = useAppointment();

  useEffect(() => { fetchAppointments(); }, [fetchAppointments]);

  if (loading) return (
    <div style={{ textAlign: "center", padding: "60px 0" }}>
      <div style={{
        width: "36px", height: "36px",
        border: "3px solid rgba(255,255,255,0.05)",
        borderTop: "3px solid #34d399",
        borderRadius: "50%",
        animation: "spin 0.8s linear infinite",
        margin: "0 auto",
      }} />
      <p style={{ fontSize: "13px", color: "#475569", marginTop: "12px" }}>Loading appointments...</p>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );

  if (error) return (
    <div style={{
      background: "rgba(248,113,113,0.1)", border: "1px solid rgba(248,113,113,0.2)",
      borderRadius: "12px", padding: "20px", textAlign: "center",
    }}>
      <p style={{ fontSize: "13px", color: "#f87171" }}>{error}</p>
      <button onClick={fetchAppointments} style={{
        marginTop: "12px", padding: "8px 20px",
        background: "rgba(52,211,153,0.1)", color: "#34d399",
        border: "1px solid rgba(52,211,153,0.2)",
        borderRadius: "8px", fontSize: "13px", cursor: "pointer",
      }}>Try Again</button>
    </div>
  );

  if (appointments.length === 0) return (
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
          <path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z" />
        </svg>
      </div>
      <p style={{ fontSize: "15px", fontWeight: "600", color: "#f1f5f9" }}>No appointments yet</p>
      <p style={{ fontSize: "13px", color: "#475569", marginTop: "6px" }}>Talk to Eve to book your first appointment</p>
    </div>
  );

  return (
    <div>
      <p style={{ fontSize: "13px", color: "#475569", marginBottom: "14px" }}>
        {appointments.length} appointment{appointments.length > 1 ? "s" : ""} found
      </p>
      {appointments.map((a) => <AppointmentCard key={a.id} appointment={a} />)}
    </div>
  );
};

export default AppointmentList;