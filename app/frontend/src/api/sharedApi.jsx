import api from './api';

const sharedApi = {
    getStudentAssessment: (requirements) => api.get('/student/assessment', { params: requirements }),
    getStudentAssessmentDetail: (requirements) => api.get('/student/assessment/detail', { params: requirements }),
};

export default sharedApi;
