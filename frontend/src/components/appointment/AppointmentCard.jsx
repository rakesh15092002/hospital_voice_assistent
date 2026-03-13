import { useAppointment } from "../../context/AppointmentContext";

const statusColors = {
  confirmed: { bg: "rgba(52,211,153,0.1)", color: "#34d399", border: "rgba(52,211,153,0.2)" },
  cancelled: { bg: "rgba(248,113,113,0.1)", color: "#f87171", border: "rgba(248,113,113,0.2)" },
  completed: { bg: "rgba(96,165,250,0.1)", color: "#60a5fa", border: "rgba(96,165,250,0.2)" },
  pending:   { bg: "rgba(251,191,36,0.1)", color: "#fbbf24", border: "rgba(251,191,36,0.2)" },
};

const AppointmentCard = ({ appointment }) => {
  const { cancel } = useAppointment();

  const formatDate = (dateStr) => {
    if (!dateStr) return "N/A";
    return new Date(dateStr).toLocaleString("en-IN", {
      day: "numeric", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  };

  const handleCancel = async () => {
    if (window.confirm("Cancel this appointment?")) await cancel(appointment.id);
  };

  const s = statusColors[appointment.status] || statusColors.pending;

  return (
    <div style={{
      background: "rgba(255,255,255,0.03)",
      border: "1px solid rgba(255,255,255,0.07)",
      borderRadius: "14px",
      padding: "16px",
      marginBottom: "12px",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div style={{
            width: "42px", height: "42px", borderRadius: "50%",
            background: "rgba(52,211,153,0.1)",
            border: "1px solid rgba(52,211,153,0.2)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: "14px", fontWeight: "700", color: "#34d399",
          }}>
            {appointment.doctor_id}
          </div>
          <div>
            <p style={{ fontSize: "14px", fontWeight: "600", color: "#f1f5f9" }}>Doctor ID: {appointment.doctor_id}</p>
            <p style={{ fontSize: "12px", color: "#475569" }}>Appointment #{appointment.id}</p>
          </div>
        </div>
        <span style={{
          background: s.bg, color: s.color,
          border: `1px solid ${s.border}`,
          padding: "4px 10px", borderRadius: "20px",
          fontSize: "11px", fontWeight: "600", textTransform: "capitalize",
        }}>
          {appointment.status}
        </span>
      </div>

      <div style={{
        display: "flex", alignItems: "center", gap: "8px",
        padding: "8px 12px", marginBottom: "12px",
        background: "rgba(255,255,255,0.02)",
        borderRadius: "8px",
        border: "1px solid rgba(255,255,255,0.05)",
      }}>
        <svg width="14" height="14" fill="#475569" viewBox="0 0 24 24">
          <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z" />
        </svg>
        <span style={{ fontSize: "13px", color: "#64748b" }}>
          {formatDate(appointment.slot_time || appointment.created_at)}
        </span>
      </div>

      {appointment.status === "confirmed" && (
        <button onClick={handleCancel} style={{
          width: "100%", padding: "9px",
          background: "transparent",
          border: "1px solid rgba(248,113,113,0.3)",
          borderRadius: "8px", fontSize: "13px",
          color: "#f87171", cursor: "pointer", fontWeight: "500",
        }}>
          Cancel Appointment
        </button>
      )}
    </div>
  );
};

export default AppointmentCard;