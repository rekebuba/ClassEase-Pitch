import { SearchParams } from "@/lib/types";
import { api, zodApiHandler } from "@/api";
import { toast } from 'sonner';
import {
    AverageRangeSchema,
    GradeCountsSchema,
    SectionCountSchema,
    StatusCountSchema,
    StudentsDataSchema,
    StudentsViewSchema
} from '@/lib/validations';
import { z } from 'zod';
import qs from "qs";

export const adminApi = {
    getDashboardData: () => api.get('/admin/dashboard'),
    getSchoolOverview: () => api.get('/admin/overview'),
    getStudents: (validQuery: SearchParams) => api.post('/admin/students', validQuery),
    getStudentsStatusCounts: () => api.get('/admin/students/status-count'),
    getStudentsAverageRange: () => api.get('/admin/students/average-range'),
    getGradeCounts: () => api.get('/admin/students/grade-counts'),
    getSectionCounts: () => api.get('/admin/students/section-counts'),
    getAllStudentsViews: () => api.get('/admin/students/views'),
    getStudentsByView: (view: string) => api.get(`/admin/students/views/${view}`),
    getTeachers: () => api.get('/admin/teachers'),
    createUser: (userData) => api.post('/admin/users', userData),
    createMarkList: (markListData) => api.post('/admin/students/mark_list', markListData),
    assignTeacher: (requirements) => api.post('/admin/assign-teacher', requirements),
    updateProfile: (userData) => api.put('/admin/profile', userData),
    deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
    createEvent: (eventData) => api.post('/admin/event/new', eventData),
    getEvents: () => api.get('/admin/events'),
};

export const getStudents = async (validQuery: SearchParams) => {
    const response = await zodApiHandler(
        () => adminApi.getStudents(validQuery),
        StudentsDataSchema,
    );

    if (!response.success) {
        throw new Error("Failed to fetch students data", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
}

export const getStudentsStatusCounts = async () => {
    const response = await zodApiHandler(
        () => adminApi.getStudentsStatusCounts(),
        StatusCountSchema,
    );

    if (!response.success) {
        console.error(response.error.details);
        throw new Error("Failed to fetch students status counts", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
}

export const getStudentsAverageRange = async () => {
    const response = await zodApiHandler(
        () => adminApi.getStudentsAverageRange(),
        AverageRangeSchema,
    );

    if (!response.success) {
        throw new Error("Failed to fetch students grade counts", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
}

export const getGradeCounts = async () => {
    const response = await zodApiHandler(
        () => adminApi.getGradeCounts(),
        GradeCountsSchema,
    );

    if (!response.success) {
        console.error(response.error.details);
        throw new Error("Failed to fetch students grade counts", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
}

export const getSectionCounts = async () => {
    const response = await zodApiHandler(
        () => adminApi.getSectionCounts(),
        SectionCountSchema,
    );

    if (!response.success) {
        console.error(response.error.details);
        throw new Error("Failed to fetch students section counts", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
}

export const getAllStudentsViews = async () => {
    const response = await zodApiHandler(
        () => adminApi.getAllStudentsViews(),
        StudentsViewSchema.array(),
    );

    if (!response.success) {
        toast.error(response.error.message, {
            style: { color: "red" },
        });
        console.error(response.error.details);
        throw new Error("Failed to fetch students views", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
}

export const getStudentsByView = async (view: string) => {
    const response = await zodApiHandler(
        () => adminApi.getStudentsByView(view),
        StudentsViewSchema,
    );

    if (!response.success) {
        toast.error(response.error.message, {
            style: { color: "red" },
        });
        console.error(response.error.details);
        throw new Error("Failed to fetch students by view", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
}
