import api from './api';

const teacherApi = {
    getStudents: () => api.get('/teacher/students'),
    updateGrade: (studentId, gradeData) => api.put(`/teacher/students/${studentId}/grade`, gradeData),
};

export default teacherApi;
