import { z } from "zod";

export const logoutSchema = z.object({
    message: z.string(),
});

export const loginSchema = z.object({
    id: z.string(),
    password: z.string(),
    apiKey: z.string(),
    role: z.enum(["admin", "teacher", "student"]),
});

export const userSchema = z.object({
    user: z.object({
        imagePath: z.string().optional(),
        role: z.enum(["Admin", "Teacher", "Student"]),
        identification: z.string(),
    }),
    detail: z.object({
        firstName: z.string(),
        fatherName: z.string(),
        grandFatherName: z.string()
    })
});
