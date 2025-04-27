import { z } from "zod";
import {
    userSchema,
    StudentSchema,
    StudentsDataSchema
    StatusCountSchema,
    AttendanceRangeSchema,
    AverageRangeSchema,
    GradeCountsSchema,
    searchParamsCache,
    StudentsViewSchema,
    tableId,
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
export type StatusCount = z.infer<typeof StatusCountSchema>;
export type AttendanceRange = z.infer<typeof AttendanceRangeSchema>;
export type AverageRange = z.infer<typeof AverageRangeSchema>;
export type GradeCounts = z.infer<typeof GradeCountsSchema>;

export interface StudentsDataResult {
    data: Student[]
    pageCount: number
    statusCounts: StatusCount
    gradeCounts: GradeCounts
    attendanceRange: AttendanceRange
    averageRange: AverageRange
    isLoading: boolean
    error: Error | null
    refetch: () => Promise<void>
}

export type SearchParams = z.infer<typeof searchParamsCache>;
export type StudentsViews = z.infer<typeof StudentsViewSchema>
