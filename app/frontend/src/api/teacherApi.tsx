import { ApiHandlerResponse, QueryParams } from '@/lib/types';
import api from './api';
import { z } from 'zod';
import { zodApiHandler } from './zod-api-handler';
import { buildQueryParams } from '@/utils/build-query-params';

const teacherApi = {
    getUser: <T extends z.ZodObject<any>>(
        userId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/users/${userId}/teacher`, { params: buildQueryParams(params) }), schema)
    },
    getDashboardData: () => api.get('/teacher/dashboard'),
    getAssignedStudents: () => api.get('/teacher/students/assigned'),
    getStudents: (requirements) => api.get('/teacher/students', { params: requirements }),
    getStudentAssessment: (requirements) => api.get('/teacher/student/assessment', { params: requirements }),
    updateScore: (gradeData) => api.put('/teacher/students/mark_list', gradeData),
    updateProfile: (userData) => api.put('/teacher/profile', userData),
};

export default teacherApi;
