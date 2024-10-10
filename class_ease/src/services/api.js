import axios from 'axios';

const API_URL = 'http://localhost:5000/api/v1';  // Adjust the URL based on your backend

export const login = async (credentials) => {
    try {
        const response = await axios.post(`${API_URL}/login`, credentials);
        localStorage.setItem('token', response.data.token);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getStudents = () => axios.get(`${API_URL}/students`);

export const getTeachers = () => axios.get(`${API_URL}/teachers`);

export const getClasses = () => axios.get(`${API_URL}/classes`);

// Add other API calls as needed
