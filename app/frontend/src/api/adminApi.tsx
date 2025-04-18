import api from './api';

const adminApi = {
    getDashboardData: () => api.get('/admin/dashboard'),
    getSchoolOverview: () => api.get('/admin/overview'),
    getStudents: (params?: { params: { grades?: [], year?: string } }) => api.get('/admin/students', { params }),
    getTeachers: () => api.get('/admin/teachers'),
    createUser: (userData) => api.post('/admin/users', userData),
    createMarkList: (markListData) => api.post('/admin/students/mark_list', markListData),
    assignTeacher: (requirements) => api.post('/admin/assign-teacher', requirements),
    updateProfile: (userData) => api.put('/admin/profile', userData),
    deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
    createEvent: (eventData) => api.post('/admin/event/new', eventData),
    getEvents: () => api.get('/admin/events'),
};

export default adminApi;
