import api from './api';

const studentApi = {
    getPanelData: () => api.get('/student/panel'),
    getYearlyScore: () => api.get('/student/yearly_score'),
    getGrades: () => api.get('/student/grades'),
    submitAssignment: (assignmentData) => api.post('/student/assignments', assignmentData),
    updateProfile: (userData) => api.put('/student/profile', userData),
};

export default studentApi;
