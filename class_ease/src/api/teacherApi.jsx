import api from './api';

const teacherApi = {
    getDashboardData: () => api.get('/teacher/dashboard'),
    getAssignedStudents: () => api.get('/teacher/students/assigned'),
    getStudents: (requirements) => api.get('/teacher/students', { params: requirements }),
    getStudentAssessment: (requirements) => api.get('/teacher/student/assessment', { params: requirements }),
    updateGrade: (studentId, gradeData) => api.put(`/teacher/students/${studentId}/grade`, gradeData),
    updateProfile: (userData) => api.put('/teacher/profile', userData),
};

export default teacherApi;
