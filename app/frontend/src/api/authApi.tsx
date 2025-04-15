import api from './api';

const authApi = {
    login: (credentials: {id: string, password: string}) => api.post('/auth/login', credentials),
    logout: () => api.post('/auth/logout'),
    refreshToken: () => api.post('/auth/refresh-token'),
};

export default authApi;
