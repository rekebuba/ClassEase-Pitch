import { z } from "zod";
import {
    userSchema,
    StudentSchema,
    StudentsDataSchema,
    StatusCountSchema,
    AverageRangeSchema,
    GradeCountsSchema,
    searchParamsCache,
    StudentsViewSchema,
    tableId,
    tableIdValue,
    RangeSchema,
    SectionCountSchema,
} from "./validations";

export type RoleProps = 'admin' | 'teacher' | 'student';
export type UserDataProps = z.infer<typeof userSchema>;

// Defines a standard error response type
export type ErrorResponse = {
    success: false;
    error: {
        type: "validation" | "api" | "network" | "unknown";
        status: number;
        message: string;
        details?: any; // Zod errors or API response errors
    };
};

// Define a success response type
export type SuccessResponse<T> = {
    success: true;
    data: T;
};

// Combined response type
export type ApiHandlerResponse<T> = SuccessResponse<T> | ErrorResponse;


export type NavItem = {
    title: string;
    href: string;
};

export type NavMain = {
    title: string;
    icon: React.ComponentType;
    href: string;
    isActive?: boolean;
    items: NavItem[];
};

export type DataProps = {
    [key in RoleProps]: {
        user: {
            firstName: string;
            fatherName: string;
            grandFatherName: string;
            email: string;
            role: string;
        };
        system: {
            title: string;
            icon: React.ComponentType;
            href: string;
        }[];
        navMain: NavMain[];
    };
};

export type Student = z.infer<typeof StudentSchema>;
export type StudentsData = z.infer<typeof StudentsDataSchema>;
export type TableId = z.infer<typeof tableId>;
export type TableIdValue = z.infer<typeof tableIdValue>;
export type StatusCount = z.infer<typeof StatusCountSchema>;
export type RangeSchema = z.infer<typeof RangeSchema>;
export type AverageRange = z.infer<typeof AverageRangeSchema>;
export type GradeCounts = z.infer<typeof GradeCountsSchema>;
export type SectionCounts = z.infer<typeof SectionCountSchema>;
export interface StudentsDataResult {
    data: Student[]
    pageCount: number
    tableId: TableId
    statusCounts: StatusCount
    gradeCounts: GradeCounts
    sectionCounts: SectionCounts;
    averageRange: AverageRange
    isLoading: boolean
    error: Error | null
    refetch: () => Promise<void>
}

export type SearchParams = z.infer<typeof searchParamsCache>;
export type StudentsViews = z.infer<typeof StudentsViewSchema>
