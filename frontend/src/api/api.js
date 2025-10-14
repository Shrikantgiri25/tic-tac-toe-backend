import axios from "axios";
import { toast } from "react-toastify";

// Base API URL from environment variable or fallback
const API_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

// Create Axios instance
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Needed if using cookies/CSRF in future
});

// Request interceptor to attach JWT access token and optional CSRF token
api.interceptors.request.use((config) => {
  // Attach JWT access token
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  // Optional: attach CSRF token if using SessionAuthentication
  const csrfToken = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }

  return config;
});

// Response interceptor for handling errors globally and token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle expired JWT token (401)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");

      if (refreshToken) {
        try {
          const res = await axios.post(`${API_URL}/auth/refresh/`, { refresh: refreshToken });
          localStorage.setItem("access_token", res.data.access);

          // Retry original request with new access token
          originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh token failed
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          toast.error("Session expired. Please log in again.");
          window.location.href = "/login";
        }
      } else {
        toast.error("Please log in again.");
        window.location.href = "/login";
      }
    }

    // Generic error handling
    if (error.response) {
      const message =
        error.response.data?.detail ||
        error.response.data?.message ||
        "Something went wrong!";
      toast.error(message);
    } else if (error.request) {
      toast.error("No response from server. Please try again later.");
    } else {
      toast.error("Request failed. Please try again.");
    }

    return Promise.reject(error);
  }
);

// ✅ Auth API endpoints
export const auth = {
  register: (data) => api.post("/accounts/register/", data),
  login: (data) => api.post("/accounts/login/", data),
  getCurrentUser: () => api.get("/accounts/me/"),
  getLeaderboard: () => api.get("/accounts/leaderboard/"),
};

// ✅ Game API endpoints
export const games = {
  joinMatchmaking: () => api.post("/games/matchmaking/"),
  createGame: () => api.post("/games/create/"),
  getGame: (gameId) => api.get(`/games/${gameId}/`),
  getMyGames: () => api.get("/games/my/"),
};

// Default export for custom requests
export default api;
