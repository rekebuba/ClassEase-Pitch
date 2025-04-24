import { z } from "zod";
import { getFiltersStateParser, getSortingStateParser } from "@/lib/parsers";
import {
    parseAsArrayOf,
    parseAsInteger,
    parseAsString,
    parseAsStringEnum,
} from "nuqs";
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
    filterFlag: z.enum(["Advanced filters", ""]).default(""),
    page: z.number().default(1),
    perPage: z.number().default(10),
    sort: z.array(z.object({ id: z.string(), desc: z.boolean() })).default([
        { id: "createdAt", desc: true },
    ]),
    name: z.string().optional(),
    grade: z.array(z.number()).optional(),
    section: z.array(z.string()).optional(),
    attendance: z.array(z.coerce.number()).optional(),
    averageGrade: z.array(z.coerce.number()).optional(),
    status: z.array(z.string()).optional(),
    estimatedHours: z.array(z.coerce.number()).optional(),
    createdAt: z.array(z.coerce.number()).optional(),
    // advanced filter
    filters: z.array(z.any()).optional(),
    joinOperator: z.enum(["and", "or"]).default("and"),
});

export type SearchParams = Awaited<
    ReturnType<typeof searchParamsCache.parse>
>;

export const searchParamMap = {
    filterFlag: parseAsStringEnum(["Advanced filters", ""]).withDefault(""),
    page: parseAsInteger.withDefault(1),
    perPage: parseAsInteger.withDefault(10),
    sort: getSortingStateParser().withDefault([
        { id: "createdAt", desc: true },
    ]),
    name: parseAsString.withDefault(""),
    grade: parseAsArrayOf(z.number()).withDefault([]),
    section: parseAsArrayOf(z.string()).withDefault([]),
    attendance: parseAsArrayOf(z.coerce.number()).withDefault([]),
    averageGrade: parseAsArrayOf(z.coerce.number()).withDefault([]),
    status: parseAsArrayOf(z.string()).withDefault([]),
    estimatedHours: parseAsArrayOf(z.coerce.number()).withDefault([]),
    createdAt: parseAsArrayOf(z.coerce.number()).withDefault([]),
    // advanced filter
    filters: getFiltersStateParser().withDefault([]),
    joinOperator: parseAsStringEnum(["and", "or"]).withDefault("and"),
}

export type SearchParamMapSchema = typeof searchParamMap;


export const createViewSchema = z.object({
    name: z.string().min(1),
    columns: z.string().array().optional(),
    filterParams: z.object({
        joinOperator: z.enum(["and", "or"]).optional(),
        sort: z.string().optional(),
        filters: z
            .object({
                field: z.enum(["title", "status", "priority"]),
                value: z.string(),
                isMulti: z.boolean().default(false),
            })
            .array()
            .optional(),
    }).optional(),
})

export type CreateViewSchema = z.infer<typeof createViewSchema>

export const editViewSchema = createViewSchema.extend({
    id: z.string().uuid(),
})

export type EditViewSchema = z.infer<typeof editViewSchema>

export const deleteViewSchema = z.object({
    id: z.string().uuid(),
})

export type DeleteViewSchema = z.infer<typeof deleteViewSchema>

export type FilterParams = NonNullable<CreateViewSchema["filterParams"]>
export type Operator = FilterParams["joinOperator"]
export type Sort = FilterParams["sort"]
export type Filter = NonNullable<FilterParams["filters"]>[number]


export const viewSchema = z.object({
    id: z.string().uuid(),
    name: z.string(),
    columns: z.array(z.string()),
    filterParams: z.object({
        joinOperator: z.enum(["and", "or"]).optional(),
        sort: z.string().optional(),
        filters: z
            .object({
                field: z.enum(["title", "status", "priority"]),
                value: z.string(),
                isMulti: z.boolean().default(false),
            })
            .array()
            .optional(),
    }).optional(),
    createdAt: z.string(),
    updatedAt: z.string(),
    // createdAt: z.string().transform((val) => new Date(val)),
    // updatedAt: z.string().transform((val) => new Date(val)),
})
export type View = z.infer<typeof viewSchema>
