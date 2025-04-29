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

export const StudentSchema = z.object({
    id: z.string(),
    name: z.string(),
    avatarUrl: z.string().optional(),
    grade: z.number(),
    section: z.string(),
    attendance: z.number(),
    averageGrade: z.number(),
    status: z.enum(["active", "inactive", "suspended"]),
    // joinedDate: z.string().transform((val) => new Date(val)),
    parentName: z.string(),
    parentPhone: z.string(),
});

export const tableId = z.record(
    StudentSchema.keyof(),
    z.string()
);

export const StudentsDataSchema = z.object({
    data: z.array(StudentSchema),
    pageCount: z.number(),
    tableId: tableId,
});

const StatusFieldSchema = StudentSchema.pick({ status: true });

export const StatusCountSchema = z.record(
    StatusFieldSchema.shape.status,
    z.number()
);

export const AttendanceRangeSchema = z.object({
    min: z.number(),
    max: z.number(),
});

export const AverageRangeSchema = z.object({
    min: z.number(),
    max: z.number(),
});

export const GradeCountsSchema = z.record(z.coerce.number(), z.number());

const SortItemSchema = z.object({
    id: z.string(),
    desc: z.boolean(),
    tableId: z.string()
});

export const searchParamsCache = z.object({
    filterFlag: z.enum(["Advanced filters", ""]).default(""),
    page: z.number().default(1),
    perPage: z.number().default(10),
    // advanced filter
    sort: z.array(SortItemSchema).default([]),
    filters: z.array(z.any()).optional(),
    joinOperator: z.enum(["and", "or"]).default("and"),
});


export const searchParamMap = {
    filterFlag: parseAsStringEnum(["Advanced filters", ""]).withDefault(""),
    page: parseAsInteger.withDefault(1),
    perPage: parseAsInteger.withDefault(10),
    sort: getSortingStateParser(),
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
    viewId: parseAsString.withDefault(""),
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


export const StudentsViewSchema = z.object({
    id: z.string().uuid(),
    name: z.string(),
    columns: z.array(z.string()),
    searchParams: searchParamsCache.optional(),
    createdAt: z.string().optional(),
    updatedAt: z.string().optional(),
    // createdAt: z.string().transform((val) => new Date(val)),
    // updatedAt: z.string().transform((val) => new Date(val)),
})
