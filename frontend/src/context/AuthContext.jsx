import { createContext, useContext, useState, useEffect } from "react";
import { loginUser, registerUser } from "../api/auth";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // On app load - check if token exists in localStorage
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");
    // Fix 1 - check undefined before JSON.parse
    if (savedToken && savedUser && savedUser !== "undefined") {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  // Login function - save token and user to state and localStorage
  const login = async (email, password) => {
    const data = await loginUser(email, password);
    setToken(data.access_token);

    // Fix 2 - backend returns user data directly, not data.user
    const userData = {
      id: data.user_id,
      name: data.name,
      email: email,
    };
    setUser(userData);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(userData));
    return data;
  };

  // Register function - auto login after register
  const register = async (name, email, password) => {
    await registerUser(name, email, password);
    return await login(email, password);
  };

  // Logout function - clear state and localStorage
  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider
      value={{ user, token, loading, login, register, logout, isAuthenticated }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);