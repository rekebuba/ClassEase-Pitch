import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

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
    const token = localStorage.getItem("apiKey"); // Retrieve the token from local storage
    if (token) {
      config.headers.apiKey = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

api.interceptors.request.use(config => {
  if (config.params) {
    config.paramsSerializer = params => {
      return Object.entries(params)
        .map(([key, value]) => {
          if (Array.isArray(value)) {
            return `${key}=${value.join(',')}`;
          }
          return `${key}=${value}`;
        })
        .join('&');
    };
  }
  return config;
});

api.interceptors.response.use(
  response => response,
  error => {
    const status = error.response?.status || 500;
    const message = error.response?.data?.message ||
      error.message ||
      error?.apiErrorMsg ||
      "API request failed"

    // Redirect based on status code
    switch (status) {
      case 401: // unauthorized
        window.location.href = `/login?from=${encodeURIComponent(window.location.pathname)}`;;
        localStorage.removeItem("apiKey"); // Clear the token
        toast.warning(error.response?.data?.message || "Unauthorized access. Please log in again.");
        break;
      case 403:
        window.location.href = `/forbidden?from=${encodeURIComponent(window.location.pathname)}`;;
        break;
      case 400:
        toast.warning(message);
        break;
      default:
        toast.error(error.response?.data.message || "An unexpected error occurred.", {
          description: error.response?.data.details || "Please try again later.",
          style: { color: 'red' }
        });
      // window.location.href = `/server-error?from=${encodeURIComponent(window.location.pathname)}`;;
    }

    return Promise.reject(error);
  }
);

export default api;
