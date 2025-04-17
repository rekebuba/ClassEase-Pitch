import { z } from "zod";
import { userSchema } from "./validations";

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

export type Student = {
    id: string
    name: string
    email: string
    grade: number
    section: string
    status: "active" | "inactive" | "suspended"
    attendance: number
    averageGrade: number
    parentName: string
    parentEmail: string
    joinedDate: string
}


export type StudentsData = {
    data: Student[]
    pageCount: number
}
