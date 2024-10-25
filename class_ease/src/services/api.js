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

// export const login = async credentials => {
//   try {
//     const response = await axios.post(`${API_URL}/login`, credentials);
// localStorage.setItem("token", response.data.token);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const adminPage = async () => {
//   try {
//     const response = await axios.get(`${API_URL}/admin/dashboard`);
//     return response.data;
//   } catch (error) {
//     throw error;
//   }
// };

// export const getStudents = () => axios.get(`${API_URL}/students`);

// export const getTeachers = () => axios.get(`${API_URL}/teachers`);

// export const getClasses = () => axios.get(`${API_URL}/classes`);

// // Add other API calls as needed
