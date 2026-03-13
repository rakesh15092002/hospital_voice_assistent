import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // Handle logout - clear auth and redirect to login
  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "14px 20px",
        background: "white",
        borderBottom: "1px solid #e2e8f0",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}
    >
      {/* Logo */}
      <div
        style={{ display: "flex", alignItems: "center", gap: "10px", cursor: "pointer" }}
        onClick={() => navigate("/")}
      >
        <div
          style={{
            width: "36px",
            height: "36px",
            background: "#1a56db",
            borderRadius: "8px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <svg width="20" height="20" fill="white" viewBox="0 0 24 24">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z" />
          </svg>
        </div>
        <div>
          <div style={{ fontSize: "14px", fontWeight: "600", color: "#1e293b" }}>
            City Care Hospital
          </div>
          <div style={{ fontSize: "11px", color: "#94a3b8" }}>
            Your Health, Our Priority
          </div>
        </div>
      </div>

      {/* Right side - user info + logout */}
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        {/* Language toggle */}
        <div style={{ fontSize: "13px", color: "#64748b" }}>
          English | हिंदा
        </div>

        {/* User name */}
        {user && (
          <div
            style={{
              width: "34px",
              height: "34px",
              borderRadius: "50%",
              background: "#e6f1fb",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "13px",
              fontWeight: "600",
              color: "#1a56db",
              cursor: "pointer",
            }}
            title={user.name}
          >
            {user.name?.charAt(0).toUpperCase()}
          </div>
        )}

        {/* Logout button */}
        <button
          onClick={handleLogout}
          style={{
            background: "transparent",
            border: "1px solid #e2e8f0",
            borderRadius: "8px",
            padding: "6px 14px",
            fontSize: "13px",
            color: "#64748b",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default Navbar;