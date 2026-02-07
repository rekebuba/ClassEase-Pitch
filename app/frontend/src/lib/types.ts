import type {
  AverageRangeSchema,
  GradeCountsSchema,
  RangeSchema,
  searchParamsCache,
  SectionCountSchema,
  StatusCountSchema,
  StudentSchema,
  StudentsDataSchema,
  StudentsViewSchema,
  tableId,
  tableIdValue,
  userSchema,
  ViewSchema,
} from "./validations";
import type { LinkOptions } from "@tanstack/react-router";
import type { z } from "zod";

export type RoleProps = "admin" | "teacher" | "student";
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

export type QueryParams = {
  /**
   * Fields to select (e.g., ["id", "name"])
   */
  fields?: string[];
  /**
   * Relationships to expand (e.g., ["author", "comments"])
   */
  expand?: string[];
  /**
   * Nested field selection for expanded relationships
   * (e.g., { author: ["id", "name"], comments: ["id"] })
   */
  nestedFields?: Record<string, string[]>;
  /**
   * Additional query parameters
   */
  params?: Record<string, string | number | boolean>;
};

export type NavBarItem = {
  title: string;
  to: LinkOptions["to"];
  params?: LinkOptions["params"];
  search?: LinkOptions["search"];
  icon?: React.ComponentType;
};

export type NavMainItem = {
  title: string;
  icon: React.ComponentType;
  isActive?: boolean;
  items: NavBarItem[];
  params?: LinkOptions["params"];
  search?: LinkOptions["search"];
};

export type MainNavItem = {
  navBar: NavBarItem[];
  navMain: NavMainItem[];
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
    navMain: NavMainItem[];
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
export type StudentsDataResult = {
  data: Student[];
  pageCount: number;
  tableId: TableId;
  statusCounts: StatusCount;
  gradeCounts: GradeCounts;
  sectionCounts: SectionCounts;
  averageRange: AverageRange;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
};

export type SearchParams = z.infer<typeof searchParamsCache>;
export type View = z.infer<typeof ViewSchema>;
export type StudentsViews = z.infer<typeof StudentsViewSchema>;
export type renameViewData = Pick<StudentsViews, "viewId" | "name">;
