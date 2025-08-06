import { toast } from 'sonner';
import api from './api';
import { zodApiHandler } from './zod-api-handler';
import { z } from 'zod';
import { TeacherRegistrationFormData } from '@/lib/form-validation';
import { ApiHandlerResponse, QueryParams } from '@/lib/types';
import { buildQueryParams } from '@/utils/build-query-params';


const sharedApi = {
    getUser: <T extends z.ZodTypeAny>(
        userId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/users/${userId}`, { params: buildQueryParams(params) }), schema)
    },
    getYear: <T extends z.ZodTypeAny>(
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get('/years', { params: buildQueryParams(params) }), schema)
    },
    getYearDetail: <T extends z.ZodTypeAny>(
        yearId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/years/${yearId}`, { params: buildQueryParams(params) }), schema)
    },
    getSubject: <T extends z.ZodTypeAny>(
        yearId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/years/${yearId}/subjects`, { params: buildQueryParams(params) }), schema)
    },
    getSubjectDetail: <T extends z.ZodTypeAny>(
        subjectId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/subjects/${subjectId}`, { params: buildQueryParams(params) }), schema)
    },
    getGrade: <T extends z.ZodTypeAny>(
        yearId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/years/${yearId}/grades`, { params: buildQueryParams(params) }), schema)
    },
    getGradeDetail: <T extends z.ZodTypeAny>(
        gradeId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/grades/${gradeId}`, { params: buildQueryParams(params) }), schema)
    },
    getStream: <T extends z.ZodTypeAny>(
        yearId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/years/${yearId}/streams`, { params: buildQueryParams(params) }), schema)
    },
    getStreamDetail: <T extends z.ZodTypeAny>(
        streamId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/streams/${streamId}`, { params: buildQueryParams(params) }), schema)
    },
    getSection: <T extends z.ZodTypeAny>(
        yearId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/years/${yearId}/sections`, { params: buildQueryParams(params) }), schema)
    },
    getSectionDetail: <T extends z.ZodTypeAny>(
        sectionId: string,
        schema: T,
        params?: QueryParams
    ): Promise<ApiHandlerResponse<z.infer<T>>> => {
        return zodApiHandler(() => api.get(`/sections/${sectionId}`, { params: buildQueryParams(params) }), schema)
    },


    getDashboardData: () => api.get('/'),
    getAcademicYears: async () => zodApiHandler(() => api.get('/academic_years'), YearSchema.array()),
    getSubjects: async () => zodApiHandler(() => api.get('/subjects'), SubjectSchema.array()),
    getGrades: async () => zodApiHandler(() => api.get('/grades'), GradeSchema.array()),
    getStreams: async () => zodApiHandler(() => api.get('/streams'), StreamSchema.array()),
    getStudentAssessment: (requirements) => api.get('/student/assessment', { params: requirements }),
    getStudentAssessmentDetail: (requirements) => api.get('/student/assessment/detail', { params: requirements }),
    updateProfile: (data) => api.post('/upload/profile', data, { headers: { 'Content-Type': 'multipart/form-data' } }),
    availableSubjects: () => api.get('/available-subjects'),
    availableGrade: () => api.get('/available-grades'),
    saveTeacherRegistration: (data: TeacherRegistrationFormData) => api.post('/register/teacher', data),
};

export default sharedApi;


export const availableSubjects = async () => {
    const response = await zodApiHandler(
        () => sharedApi.availableSubjects(),
        z.array(z.string())
    );

    if (!response.success) {
        toast.error(response.error.message, {
            style: { color: "red" },
        });
        console.error(response.error.details);
        throw new Error("Failed to update teacher application status", {
            cause: JSON.stringify(response.error.details),
        });
    }


    return response.data;
};

export const availableGradeLevels = async () => {
    const response = await zodApiHandler(
        () => sharedApi.availableGrade(),
        z.array(z.number())
    );

    if (!response.success) {
        toast.error(response.error.message, {
            style: { color: "red" },
        });
        console.error(response.error.details);
        throw new Error("Failed to fetch available grade levels", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
};

export const saveTeacherRegistration = async (data: TeacherRegistrationFormData) => {
    const response = await zodApiHandler(
        () => sharedApi.saveTeacherRegistration(data),
        ApiResponse
    );

    if (!response.success) {
        toast.error(response.error.message, {
            style: { color: "red" },
        });
        console.error(response.error.details);
        throw new Error("Failed to save teacher registration", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
}
