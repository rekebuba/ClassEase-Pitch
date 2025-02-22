import api from './api';

const sharedApi = {
    getStudentAssessment: (requirements) => api.get('/student/assessment', { params: requirements }),
    getStudentAssessmentDetail: (requirements) => api.get('/student/assessment/detail', { params: requirements }),
    updateProfile: (data) => api.post('/upload/profile', data, { headers: { 'Content-Type': 'multipart/form-data' } }),
};

export default sharedApi;
