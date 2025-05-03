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

const intOrNull = z.union([z.number(), z.literal("N/A"), z.null()]).transform((val) => val ?? "N/A")
const stringOrNull = z.union([z.string(), z.literal("N/A"), z.null()]).transform((val) => val ?? "N/A")


export const StudentSchema = z.object({
    identification: z.string(),
    imagePath: z.string().optional(),
    studentName: z.string(),
    guardianName: z.string(),
    guardianPhone: z.string(),
    grade: z.number(),
    sectionI: stringOrNull,
    sectionII: stringOrNull,
    averageI: intOrNull,
    averageII: intOrNull,
    rankI: intOrNull,
    rankII: intOrNull,
    finalScore: intOrNull,
    rank: intOrNull,
    isActive: z.union([z.boolean(), z.enum(["active", "inactive", "suspended"])]).transform((val) => val ? 'active' : 'inactive'),
    createdAt: z.string(),
});

export const tableIdValue = z.union([
    z.string(),
    z.array(z.tuple([z.string(), z.string()])),
]);

export const tableId = z.record(
    StudentSchema.keyof(),
    tableIdValue
).optional();

export const StudentsDataSchema = z.object({
    data: z.array(StudentSchema),
    pageCount: z.number(),
    tableId: tableId,
});

const StatusFieldSchema = StudentSchema.pick({ isActive: true });

export const StatusCountSchema = z.record(
    StatusFieldSchema.shape.isActive,
    z.number()
);

export const RangeSchema = z.object({
    min: intOrNull,
    max: intOrNull,
});

export const AverageRangeSchema = z.object({
    totalAverage: RangeSchema,
    averageI: RangeSchema,
    averageII: RangeSchema,
    rank: RangeSchema,
    rankI: RangeSchema,
    rankII: RangeSchema,
});

export const GradeCountsSchema = z.record(z.coerce.number(), z.number());

const SortItemSchema = z.object({
    id: z.string(),
    desc: z.boolean(),
    tableId: tableIdValue
});

export const searchParamsCache = z.object({
    page: z.number().default(1),
    perPage: z.number().default(10),
    // advanced filter
    sort: z.array(SortItemSchema).optional(),
    filters: z.array(z.any()).optional(),
    joinOperator: z.enum(["and", "or"]).default("and"),
});


export const searchParamMap = {
    page: parseAsInteger.withDefault(1),
    perPage: parseAsInteger.withDefault(10),
    sort: getSortingStateParser().withDefault([]),
    filters: getFiltersStateParser().withDefault([]),
    joinOperator: parseAsStringEnum(["and", "or"]).withDefault("and"),
    createdAt: parseAsString.withDefault(""),
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
