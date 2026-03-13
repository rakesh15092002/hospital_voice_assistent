import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const LoginForm = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError("Invalid email or password. Please try again.");
    } finally {
      setLoading(false);
    }
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
      {/* Glow bg */}
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
        {/* Logo */}
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
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.93 0 3.5 1.57 3.5 3.5S13.93 13 12 13s-3.5-1.57-3.5-3.5S10.07 6 12 6zm7 13H5v-.23c0-.62.28-1.2.76-1.58C7.47 15.82 9.64 15 12 15s4.53.82 6.24 2.19c.48.38.76.97.76 1.58V19z" />
            </svg>
          </div>
          <h2 style={{ fontSize: "22px", fontWeight: "700", color: "#f1f5f9" }}>
            Welcome Back
          </h2>
          <p style={{ fontSize: "13px", color: "#64748b", marginTop: "4px" }}>
            Sign in to City Care Hospital
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
          {/* Email */}
          <div style={{ marginBottom: "16px" }}>
            <label style={{ fontSize: "12px", color: "#64748b", display: "block", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="rakesh@example.com"
              required
              style={{
                width: "100%",
                padding: "12px 16px",
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.08)",
                borderRadius: "10px",
                fontSize: "14px",
                outline: "none",
                color: "#f1f5f9",
                boxSizing: "border-box",
              }}
            />
          </div>

          {/* Password */}
          <div style={{ marginBottom: "24px" }}>
            <label style={{ fontSize: "12px", color: "#64748b", display: "block", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "0.05em" }}>
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              style={{
                width: "100%",
                padding: "12px 16px",
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.08)",
                borderRadius: "10px",
                fontSize: "14px",
                outline: "none",
                color: "#f1f5f9",
                boxSizing: "border-box",
              }}
            />
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
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p style={{ textAlign: "center", fontSize: "13px", color: "#475569", marginTop: "20px" }}>
          Don't have an account?{" "}
          <span onClick={() => navigate("/register")} style={{ color: "#34d399", cursor: "pointer", fontWeight: "600" }}>
            Register
          </span>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;