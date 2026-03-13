import axios from "axios";

// Create an Axios instance with default settings
const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000", 
  headers: {
    "Content-Type": "application/json", 
  },
});

// Request interceptor — add token to every request if available
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); // Get token from localStorage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // Add Authorization header
    }
    return config; // Return the updated config
  },
  (error) => Promise.reject(error) // Handle request errors
);

// Response interceptor — logout user on 401 Unauthorized
API.interceptors.response.use(
  (response) => response, 
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token"); // Remove token if unauthorized
      window.location.href = "/login"; // Redirect to login page
    }
    return Promise.reject(error); 
  }
);

export default API; // Export the Axios instance