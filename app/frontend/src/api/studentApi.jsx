import api from './api';

const studentApi = {
    getPanelData: () => api.get('/student/panel'),
    getYearlyScore: () => api.get('/student/yearly_score'),
    getGrades: () => api.get('/student/grades'),
    updateProfile: (userData) => api.put('/student/profile', userData),
};

export default studentApi;
