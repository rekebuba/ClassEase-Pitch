import { z } from "zod";
import { YearSetupSchema, GradeSchema, StreamSchema, SubjectSchema, YearSchema } from "./api-response-validation";

import {
    AdminSchema,
    StudentSchema,
    TeacherSchema,
    UserSchema,
    AcademicTermSchema,
    AssessmentSchema,
    EventSchema,
    MarkListSchema,
    RegistrationSchema,
    SectionSchema,
    StudentTermRecordSchema,
    TeacherTermRecordSchema,
    StudentYearRecordSchema,
    SubjectYearlyAverageSchema,
    TeacherRecordSchema,
    YearlySubjectSchema,
    TeacherSubjectLinkSchema,
    TeacherGradeLinkSchema
} from './api-response-validation';

export type YearSchema = z.infer<typeof YearSchema>;
export type GradeSchema = z.infer<typeof GradeSchema>;
export type SubjectSchema = z.infer<typeof SubjectSchema>;
export type StreamSchema = z.infer<typeof StreamSchema>;
export type Admin = z.infer<typeof AdminSchema>;
export type Student = z.infer<typeof StudentSchema>;
export type Teacher = z.infer<typeof TeacherSchema>;
export type User = z.infer<typeof UserSchema>;
export type Grade = z.infer<typeof GradeSchema>;
export type Subject = z.infer<typeof SubjectSchema>;
export type AcademicTerm = z.infer<typeof AcademicTermSchema>;
export type Assessment = z.infer<typeof AssessmentSchema>;
export type Event = z.infer<typeof EventSchema>;
export type MarkList = z.infer<typeof MarkListSchema>;
export type Registration = z.infer<typeof RegistrationSchema>;
export type Section = z.infer<typeof SectionSchema>;
export type Stream = z.infer<typeof StreamSchema>;
export type StudentTermRecord = z.infer<typeof StudentTermRecordSchema>;
export type TeacherTermRecord = z.infer<typeof TeacherTermRecordSchema>;
export type StudentYearRecord = z.infer<typeof StudentYearRecordSchema>;
export type SubjectYearlyAverage = z.infer<typeof SubjectYearlyAverageSchema>;
export type TeacherRecord = z.infer<typeof TeacherRecordSchema>;
export type Year = z.infer<typeof YearSchema>;
export type YearlySubject = z.infer<typeof YearlySubjectSchema>;
export type TeacherSubjectLink = z.infer<typeof TeacherSubjectLinkSchema>;
export type TeacherGradeLink = z.infer<typeof TeacherGradeLinkSchema>;

export type YearSetupType = z.infer<typeof YearSetupSchema>;
