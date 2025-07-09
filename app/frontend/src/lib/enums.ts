import { z } from 'zod';

export const RoleEnum = z.enum([
    "admin",
    "teacher",
    "student",
]);

export const TableEnum = z.enum([
    "students",
    "teachers",
    "admin",
    "semesters",
]);

export const EventPurposeEnum = z.enum([
    "academic",
    "cultural",
    "sports",
    "graduation",
    "administration",
    "new semester",
    "other",
]);

export const EventOrganizerEnum = z.enum([
    "school",
    "school administration",
    "student club",
    "external organizer",
]);

export const EventLocationEnum = z.enum([
    "auditorium",
    "classroom",
    "sports field",
    "online",
    "other",
]);

export const EventEligibilityEnum = z.enum([
    "all",
    "students only",
    "faculty only",
    "invitation only",
]);

export const GenderEnum = z.enum([
    "male",
    "female",
]);

export const MaritalStatusEnum = z.enum([
    "single",
    "married",
    "divorced",
    "widowed",
    "prefer-not-to-say",
]);

export const ExperienceYearEnum = z.enum([
    "0",
    "1-2",
    "3-5",
    "6-10",
    "11-15",
    "16-20",
    "20+",
], {
    required_error: "Missing years of experience",
});

export const ScheduleEnum = z.enum([
    "full-time",
    "part-time",
    "flexible-hours",
    "substitute",
]);

export const GradeLevelEnum = z.enum([
    "primary",
    "middle school",
    "high school",
]);

export const StatusEnum = z.enum([
    "pending",
    "approved",
    "rejected",
    "interview-scheduled",
    "under-review",
]);

export const HighestDegreeEnum = z.enum([
    "bachelors",
    "masters",
    "doctorate",
]);

export const StudentApplicationStatusEnum = z.enum([
    "pending",
    "under-review",
    "documents-required",
    "approved",
    "rejected",
    "enrolled"
]);
export const AcademicTermEnum = z.enum([
    "First Term",
    "Second Term",
    "Third Term",
    "Fourth Term",
]);
export const MarkListTypeEnum = z.enum([
    "Test",
    "Quiz",
    "Assignment",
    "Midterm",
    "Final",
]);
export const AcademicTermTypeEnum = z.enum([
    "Semester",
    "Quarter"
]);

export type RoleEnumType = z.infer<typeof RoleEnum>;
export type TableEnumType = z.infer<typeof TableEnum>;
export type EventPurposeEnumType = z.infer<typeof EventPurposeEnum>;
export type EventOrganizerEnumType = z.infer<typeof EventOrganizerEnum>;
export type EventLocationEnumType = z.infer<typeof EventLocationEnum>;
export type EventEligibilityEnumType = z.infer<typeof EventEligibilityEnum>;
export type GenderEnumType = z.infer<typeof GenderEnum>;
export type MaritalStatusEnumType = z.infer<typeof MaritalStatusEnum>;
export type ExperienceYearEnumType = z.infer<typeof ExperienceYearEnum>;
export type ScheduleEnumType = z.infer<typeof ScheduleEnum>;
export type GradeLevelEnumType = z.infer<typeof GradeLevelEnum>;
export type StatusEnumType = z.infer<typeof StatusEnum>;
export type HighestDegreeEnumType = z.infer<typeof HighestDegreeEnum>;
