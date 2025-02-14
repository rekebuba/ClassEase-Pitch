import api from './api';

const adminApi = {
    getDashboardData: () => api.get('/admin/dashboard'),
    createUser: (userData) => api.post('/admin/users', userData),
    deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
};

export default adminApi;
