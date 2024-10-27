import axios from "axios";

// services/apiService.js
const api = axios.create({
  baseURL: "http://localhost:5000/api/v1"
});

api.interceptors.request.use(
  config => {
    // Modify request before it is sent
    const token = localStorage.getItem("Authorization"); // Retrieve the token from local storage
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      const reason = error.response.data.reason;

      if (reason === "SESSION_EXPIRED") {
        alert("Your session has expired. Please log in again.");
        localStorage.removeItem("Authorization"); // Clear the token
      } else if (reason === "UNAUTHORIZED") {
        alert("You are not authorized to access this resource.");
      }

      window.location.href = "/login"; // Redirect to login page
    }
    return Promise.reject(error);
  }
);

export default api;

