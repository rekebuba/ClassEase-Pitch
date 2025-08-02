import { ApiHandlerResponse, QueryParams } from '@/lib/types';
import api from './api';
import { z } from 'zod';
import { zodApiHandler } from './zod-api-handler';
import { buildQueryParams } from '@/utils/build-query-params';

const studentApi = {
    getUser: <T extends z.ZodObject<any>>(
        userId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/users/${userId}/student`, { params: buildQueryParams(params) }), schema)
    },
    getCoursesToRegister: () => api.get('/student/course/registration'),
    registerCourses: () => api.post('/student/course/registration'),
    getYearlyScore: () => api.get('/student/yearly_score'),
    getGrades: () => api.get('/student/grades'),
    updateProfile: (userData) => api.put('/student/profile', userData),
};

export default studentApi;
