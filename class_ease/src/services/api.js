import axios from "axios";

/**
 * Creates an instance of axios with a predefined base URL.
 * 
 * The base URL is set to "http://localhost:5000/api/v1", which is the root endpoint
 * for the API. This instance can be used to make HTTP requests to the API endpoints
 * under this base URL.
 * 
 * @constant {AxiosInstance} api - An axios instance configured with the base URL.
 */
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
    if (error.response && (error.response.status === 401 || error.response.status === 404)) {
      const reason = error.response.data.reason;

      if (reason === "SESSION_EXPIRED") {
        window.location.href = "/login"; // Redirect to login page
        localStorage.removeItem("Authorization"); // Clear the token
        alert("Your session has expired. Please log in again.");
      } else if (reason === "UNAUTHORIZED") {
        window.location.href = "/login"; // Redirect to login page
        alert("You are not authorized to access this resource.");
      }

    }
    return Promise.reject(error);
  }
);

export default api;
