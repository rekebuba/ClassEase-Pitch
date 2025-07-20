import { z } from "zod";
import { GradeSchema, StreamSchema, SubjectSchema, YearSchema } from "./api-response-validation";

export type YearSchema = z.infer<typeof YearSchema>;
export type GradeSchema = z.infer<typeof GradeSchema>;
export type SubjectSchema = z.infer<typeof SubjectSchema>;
export type StreamSchema = z.infer<typeof StreamSchema>;
