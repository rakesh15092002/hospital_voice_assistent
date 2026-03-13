import { useAppointment } from "../../context/AppointmentContext";

// Status badge colors
const statusColors = {
  confirmed: { bg: "#dcfce7", color: "#166534" },
  cancelled: { bg: "#fef2f2", color: "#dc2626" },
  completed: { bg: "#e6f1fb", color: "#1a56db" },
  pending:   { bg: "#fef9c3", color: "#854d0e" },
};

const AppointmentCard = ({ appointment }) => {
  const { cancel } = useAppointment();

  // Format date to readable format
  const formatDate = (dateStr) => {
    if (!dateStr) return "N/A";
    return new Date(dateStr).toLocaleString("en-IN", {
      day: "numeric",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  // Handle cancel button click
  const handleCancel = async () => {
    if (window.confirm("Are you sure you want to cancel this appointment?")) {
      await cancel(appointment.id);
    }
  };

  const statusStyle = statusColors[appointment.status] || statusColors.pending;

  return (
    <div
      style={{
        background: "white",
        border: "1px solid #e2e8f0",
        borderRadius: "12px",
        padding: "16px",
        marginBottom: "12px",
      }}
    >
      {/* Top row - doctor info + status */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: "12px",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          {/* Doctor avatar */}
          <div
            style={{
              width: "42px",
              height: "42px",
              borderRadius: "50%",
              background: "#e6f1fb",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "14px",
              fontWeight: "600",
              color: "#1a56db",
              flexShrink: 0,
            }}
          >
            {appointment.doctor_id}
          </div>

          <div>
            <p style={{ fontSize: "14px", fontWeight: "600", color: "#1e293b" }}>
              Doctor ID: {appointment.doctor_id}
            </p>
            <p style={{ fontSize: "12px", color: "#94a3b8", marginTop: "2px" }}>
              Appointment #{appointment.id}
            </p>
          </div>
        </div>

        {/* Status badge */}
        <span
          style={{
            background: statusStyle.bg,
            color: statusStyle.color,
            padding: "4px 10px",
            borderRadius: "20px",
            fontSize: "11px",
            fontWeight: "600",
            textTransform: "capitalize",
          }}
        >
          {appointment.status}
        </span>
      </div>

      {/* Slot time */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "6px",
          marginBottom: "12px",
          padding: "8px 12px",
          background: "#f8fafc",
          borderRadius: "8px",
        }}
      >
        <svg width="14" height="14" fill="#64748b" viewBox="0 0 24 24">
          <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z" />
        </svg>
        <span style={{ fontSize: "13px", color: "#64748b" }}>
          {formatDate(appointment.slot_time || appointment.created_at)}
        </span>
      </div>

      {/* Cancel button - only show if confirmed */}
      {appointment.status === "confirmed" && (
        <button
          onClick={handleCancel}
          style={{
            width: "100%",
            padding: "8px",
            background: "transparent",
            border: "1px solid #fecaca",
            borderRadius: "8px",
            fontSize: "13px",
            color: "#dc2626",
            cursor: "pointer",
            fontWeight: "500",
          }}
        >
          Cancel Appointment
        </button>
      )}
    </div>
  );
};

export default AppointmentCard;