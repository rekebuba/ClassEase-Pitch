import api from './api';

const adminApi = {
    getDashboardData: () => api.get('/admin/dashboard'),
    getSchoolOverview: () => api.get('/admin/overview'),
    getStudents: (requirements) => api.get('/admin/students', { params: requirements }),
    getTeachers: (requirements) => api.get('/admin/teachers', { params: requirements }),
    getStudentAssessment: (requirements) => api.get('/admin/student/assessment', { params: requirements }),
    getStudentAssessmentDetail: (requirements) => api.get('/admin/student/assessment/detail', { params: requirements }),
    createUser: (userData) => api.post('/admin/users', userData),
    createMarkList: (markListData) => api.post('/admin/students/mark_list', markListData),
    assignTeacher: (requirements) => api.post('/admin/assign-teacher', requirements),
    updateProfile: (userData) => api.put('/admin/profile', userData),
    deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
};

export default adminApi;
