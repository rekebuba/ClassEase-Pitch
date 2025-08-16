import { z } from "zod";

export const RoleEnum = z.enum(["admin", "teacher", "student"]);

export const TableEnum = z.enum(["students", "teachers", "admin", "semesters"]);

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

export const GenderEnum = z.enum(["male", "female"]);

export const BloodTypeEnum = z.enum([
  "A+",
  "A-",
  "B+",
  "B-",
  "AB+",
  "AB-",
  "O+",
  "O-",
  "unknown",
]);

export const MaritalStatusEnum = z.enum([
  "single",
  "married",
  "divorced",
  "widowed",
  "prefer-not-to-say",
]);

export const ExperienceYearEnum = z.enum(
  ["0", "1-2", "3-5", "6-10", "11-15", "16-20", "20+"],
  {
    required_error: "Missing years of experience",
  },
);

export const ScheduleEnum = z.enum([
  "full-time",
  "part-time",
  "flexible-hours",
  "substitute",
]);

export const GradeEnum = z.enum([
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
  "11",
  "12",
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

export const HighestDegreeEnum = z.enum(["bachelors", "masters", "doctorate"]);

export const StudentApplicationStatusEnum = z.enum([
  "pending",
  "under-review",
  "documents-required",
  "approved",
  "rejected",
  "enrolled",
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

export const AcademicTermTypeEnum = z.enum(["Semester", "Quarter"]);

export const AcademicYearStatusEnum = z.enum([
  "upcoming",
  "active",
  "completed",
  "archived",
]);

export type RoleType = z.infer<typeof RoleEnum>;
export type TableType = z.infer<typeof TableEnum>;
export type EventPurposeType = z.infer<typeof EventPurposeEnum>;
export type EventOrganizerType = z.infer<typeof EventOrganizerEnum>;
export type EventLocationType = z.infer<typeof EventLocationEnum>;
export type EventEligibilityType = z.infer<typeof EventEligibilityEnum>;
export type GenderType = z.infer<typeof GenderEnum>;
export type MaritalStatusType = z.infer<typeof MaritalStatusEnum>;
export type ExperienceYearType = z.infer<typeof ExperienceYearEnum>;
export type ScheduleType = z.infer<typeof ScheduleEnum>;
export type GradeLevelType = z.infer<typeof GradeLevelEnum>;
export type StatusType = z.infer<typeof StatusEnum>;
export type HighestDegreeType = z.infer<typeof HighestDegreeEnum>;
export type AcademicTermType = z.infer<typeof AcademicTermEnum>;
export type AcademicYearStatusType = z.infer<typeof AcademicYearStatusEnum>;
export type StudentApplicationStatusType = z.infer<
  typeof StudentApplicationStatusEnum
>;
export type MarkListType = z.infer<typeof MarkListTypeEnum>;
export type AcademicTermName = z.infer<typeof AcademicTermTypeEnum>;
