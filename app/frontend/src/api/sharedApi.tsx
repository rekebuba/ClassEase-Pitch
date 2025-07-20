import { toast } from 'sonner';
import api from './api';
import { zodApiHandler } from './zod-api-handler';
import { z } from 'zod';
import { TeacherRegistrationFormData } from '@/lib/form-validation';
import { RoleEnumType } from '@/lib/enums';
import { UserWithAdminSchema, UserWithTeacherSchema, UserWithStudentSchema, UserProfile, SubjectSchema, GradeSchema, YearSchema, StreamSchema } from "@/lib/api-response-validation";
const sharedApi = {
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

export const getDashboardData = async (userRole: RoleEnumType) => {

    let schema: z.ZodSchema<UserProfile>;
    switch (userRole) {
        case 'admin':
            schema = UserWithAdminSchema;
            break;
        case 'teacher':
            schema = UserWithTeacherSchema;
            break;
        case 'student':
            schema = UserWithStudentSchema;
            break;
        default:
            throw new Error("Invalid user role");
    }

    const response = await zodApiHandler(
        () => sharedApi.getDashboardData(),
        schema
    );

    return response;
};

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
