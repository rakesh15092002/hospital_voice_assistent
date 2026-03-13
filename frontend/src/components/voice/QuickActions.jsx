import { useNavigate } from "react-router-dom";

const actions = [
  {
    id: 1, label: "Find Doctor",
    icon: <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z" /></svg>,
    route: null, color: "#34d399",
  },
  {
    id: 2, label: "Appointments",
    icon: <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z" /></svg>,
    route: "/appointments", color: "#60a5fa",
  },
  {
    id: 3, label: "Pharmacy",
    icon: <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M20 6h-2.18c.07-.31.18-.61.18-.93C18 3.38 16.62 2 14.93 2c-1.14 0-2.12.65-2.67 1.62L12 4.77l-.26-.48C11.19 2.65 10.2 2 9.07 2 7.38 2 6 3.38 6 5.07c0 .32.09.62.18.93H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2z" /></svg>,
    route: null, color: "#a78bfa",
  },
  {
    id: 4, label: "Lab Info",
    icon: <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M19.8 18.4L14 10.67V6h1c.55 0 1-.45 1-1s-.45-1-1-1H9c-.55 0-1 .45-1 1s.45 1 1 1h1v4.67L4.2 18.4C3.71 19.06 4.18 20 5 20h14c.82 0 1.29-.94.8-1.6z" /></svg>,
    route: null, color: "#fbbf24",
  },
  {
    id: 5, label: "Emergency",
    icon: <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z" /></svg>,
    route: null, color: "#f87171", isEmergency: true,
  },
];

const QuickActions = ({ onActionClick }) => {
  const navigate = useNavigate();

  const handleClick = (action) => {
    if (action.route) { navigate(action.route); return; }
    if (action.isEmergency) { window.location.href = "tel:108"; return; }
    onActionClick && onActionClick(action.label);
  };

  return (
    <div style={{ display: "flex", gap: "8px", justifyContent: "center", padding: "0 4px" }}>
      {actions.map((action) => (
        <div
          key={action.id}
          onClick={() => handleClick(action)}
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "6px",
            padding: "12px 6px",
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.06)",
            borderRadius: "14px",
            cursor: "pointer",
            transition: "all 0.2s ease",
          }}
        >
          <div style={{
            width: "42px", height: "42px",
            borderRadius: "12px",
            background: `rgba(${action.color === "#34d399" ? "52,211,153" : action.color === "#60a5fa" ? "96,165,250" : action.color === "#a78bfa" ? "167,139,250" : action.color === "#fbbf24" ? "251,191,36" : "248,113,113"},0.1)`,
            display: "flex", alignItems: "center", justifyContent: "center",
            color: action.color,
          }}>
            {action.icon}
          </div>
          <span style={{ fontSize: "10px", fontWeight: "500", color: action.color, textAlign: "center" }}>
            {action.label}
          </span>
        </div>
      ))}
    </div>
  );
};

export default QuickActions;