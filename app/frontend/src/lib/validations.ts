import { z } from "zod";
import { getFiltersStateParser, getSortingStateParser } from "@/lib/parsers";
import {
    createSearchParamsCache,
    parseAsArrayOf,
    parseAsInteger,
    parseAsString,
    parseAsStringEnum,
} from "nuqs/server";
import { flagConfig } from "@/config/flag";


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

export const searchParamsCache = z.object({
    filterFlag: z.enum(
        flagConfig.featureFlags.map((flag) => flag.value) as [string, ...string[]]
    ),
    page: z.number().default(1),
    perPage: z.number().default(10),
    // sort: z.array(z.object({ id: z.string(), desc: z.boolean() })).default([
    //     { id: "createdAt", desc: true },
    // ]),
    filters: z.array(z.any()).default([]),
    joinOperator: z.enum(["and", "or"]).default("and"),
});

export type GetStudentsSchema = Awaited<
    ReturnType<typeof searchParamsCache.parse>
>;
