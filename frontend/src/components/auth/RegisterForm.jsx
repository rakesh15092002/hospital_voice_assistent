import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const RegisterForm = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(name, email, password);
      navigate("/");
    } catch (err) {
      setError("Registration failed. Email may already be in use.");
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    width: "100%",
    padding: "12px 16px",
    background: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "10px",
    fontSize: "14px",
    outline: "none",
    color: "#f1f5f9",
    boxSizing: "border-box",
  };

  const labelStyle = {
    fontSize: "12px",
    color: "#64748b",
    display: "block",
    marginBottom: "8px",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0f1e",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: "20px",
    }}>
      <div style={{
        position: "fixed", top: "20%", left: "50%", transform: "translateX(-50%)",
        width: "400px", height: "400px",
        background: "radial-gradient(circle, rgba(52,211,153,0.06) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />

      <div style={{
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.08)",
        borderRadius: "20px",
        padding: "36px 32px",
        width: "100%",
        maxWidth: "400px",
        backdropFilter: "blur(20px)",
      }}>
        <div style={{ textAlign: "center", marginBottom: "32px" }}>
          <div style={{
            width: "64px", height: "64px",
            background: "rgba(52,211,153,0.1)",
            border: "1px solid rgba(52,211,153,0.2)",
            borderRadius: "16px",
            display: "flex", alignItems: "center", justifyContent: "center",
            margin: "0 auto 16px",
          }}>
            <svg width="28" height="28" fill="#34d399" viewBox="0 0 24 24">
              <path d="M15 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
            </svg>
          </div>
          <h2 style={{ fontSize: "22px", fontWeight: "700", color: "#f1f5f9" }}>
            Create Account
          </h2>
          <p style={{ fontSize: "13px", color: "#64748b", marginTop: "4px" }}>
            Join City Care Hospital
          </p>
        </div>

        {error && (
          <div style={{
            background: "rgba(239,68,68,0.1)",
            border: "1px solid rgba(239,68,68,0.2)",
            borderRadius: "10px",
            padding: "10px 14px",
            fontSize: "13px",
            color: "#f87171",
            marginBottom: "20px",
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "16px" }}>
            <label style={labelStyle}>Full Name</label>
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Rakesh Maurya" required style={inputStyle} />
          </div>
          <div style={{ marginBottom: "16px" }}>
            <label style={labelStyle}>Email Address</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="rakesh@example.com" required style={inputStyle} />
          </div>
          <div style={{ marginBottom: "24px" }}>
            <label style={labelStyle}>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" required style={inputStyle} />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "13px",
              background: loading ? "rgba(52,211,153,0.4)" : "linear-gradient(135deg, #34d399, #059669)",
              color: "white",
              border: "none",
              borderRadius: "10px",
              fontSize: "14px",
              fontWeight: "600",
              cursor: loading ? "not-allowed" : "pointer",
              boxShadow: "0 0 20px rgba(52,211,153,0.2)",
            }}
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p style={{ textAlign: "center", fontSize: "13px", color: "#475569", marginTop: "20px" }}>
          Already have an account?{" "}
          <span onClick={() => navigate("/login")} style={{ color: "#34d399", cursor: "pointer", fontWeight: "600" }}>
            Sign In
          </span>
        </p>
      </div>
    </div>
  );
};

export default RegisterForm;