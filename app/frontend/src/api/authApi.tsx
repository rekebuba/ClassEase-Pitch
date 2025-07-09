import { loginSchema } from '@/lib/validations';
import api from './api';
import { zodApiHandler } from './zod-api-handler';

const authApi = {
    login: (credentials: { identification: string, password: string }) => api.post('/auth/login', credentials),
    logout: () => api.post('/auth/logout'),
    refreshToken: () => api.post('/auth/refresh-token'),
};

export const login = async (credentials: { identification: string, password: string }) => {
    const response = await zodApiHandler(
        () => authApi.login(credentials),
        loginSchema,
    )

    if (!response.success) {
        throw new Error("login Failed", {
            cause: JSON.stringify(response.error.details),
        });
    }

    return response.data;
};

export default authApi;
