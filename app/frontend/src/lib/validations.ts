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

export const studentSchema = z.object({
    data: z.object({
        firstName: z.string(),
        fatherName: z.string(),
        grandFatherName: z.string(),
        identification: z.string(),
        imagePath: z.string(),
    }),
    pageCount: z.number(),

    // year: z.number(),
    // grade: z.string(),
    // section: z.string(),
});
