import api from './api';

const studentApi = {
    getGrades: () => api.get('/student/grades'),
    submitAssignment: (assignmentData) => api.post('/student/assignments', assignmentData),
};

export default studentApi;
