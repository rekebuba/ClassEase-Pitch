import { z } from "zod";
import { ExperienceYearEnum, GenderEnum, GradeLevelEnum, HighestDegreeEnum, MaritalStatusEnum, ScheduleEnum, StatusEnum } from "./enums";

export const TeacherApplicationSchema = z.object({
    id: z.string(),
    applicationDate: z.string(),
    status: StatusEnum,

    // Personal Information
    firstName: z.string(),
    fatherName: z.string(),
    grandFatherName: z.string(),
    dateOfBirth: z.string(),
    gender: GenderEnum,
    nationality: z.string(),
    maritalStatus: MaritalStatusEnum.nullable(),

    // Contact Information
    address: z.string(),
    city: z.string(),
    state: z.string(),
    postalCode: z.string(),
    country: z.string(),
    primaryPhone: z.string(),
    secondaryPhone: z.string().nullable(),
    personalEmail: z.string(),

    // Emergency Contact
    emergencyContactName: z.string(),
    emergencyContactRelation: z.string(),
    emergencyContactPhone: z.string(),

    // Educational Background
    highestDegree: HighestDegreeEnum,
    university: z.string(),
    graduationYear: z.number(),
    gpa: z.number(),

    // Teaching Information
    teachingLicense: z.boolean(),
    licenseNumber: z.string().nullable(),
    licenseState: z.string().nullable(),
    licenseExpirationDate: z.string().nullable(),
    yearsOfExperience: ExperienceYearEnum,
    previousSchools: z.string().nullable(),
    preferredSchedule: ScheduleEnum.nullable(),

    // Professional Skills
    specialSkills: z.string().nullable(),

    // Employment Information
    positionApplyingFor: z.string(),
    salaryExpectation: z.string().optional().nullable(),

    // Background Information
    hasConvictions: z.boolean(),
    convictionDetails: z.string().nullable(),
    hasDisciplinaryActions: z.boolean(),
    disciplinaryDetails: z.string().nullable(),

    // References
    reference1Name: z.string(),
    reference1Title: z.string(),
    reference1Organization: z.string(),
    reference1Phone: z.string(),
    reference1Email: z.string(),
    reference2Name: z.string().nullable(),
    reference2Title: z.string().nullable(),
    reference2Organization: z.string().nullable(),
    reference2Phone: z.string().nullable(),
    reference2Email: z.string().nullable(),
    reference3Name: z.string().nullable(),
    reference3Title: z.string().nullable(),
    reference3Organization: z.string().nullable(),
    reference3Phone: z.string().nullable(),
    reference3Email: z.string().nullable(),

    // Additional Information
    teachingPhilosophy: z.string().nullable(),
    whyTeaching: z.string().nullable(),
    additionalComments: z.string().nullable(),

    // Documents and Files
    resume: z.string().nullable(),
    coverLetter: z.string().nullable(),
    transcripts: z.string().nullable(),
    teachingCertificate: z.string().nullable(),
    backgroundCheck: z.string().nullable(),
    profilePhoto: z.string().optional().nullable(),
});

export const DetailTeacherAPPlicationSchema = z.object({
    subjectsToTeach: z.array(z.string()),
    gradeLevelsToTeach: z.array(z.number()),
})

export const TeacherApplicationWithDetailsSchema = TeacherApplicationSchema.merge(DetailTeacherAPPlicationSchema);

export type TeacherApplication = z.infer<typeof TeacherApplicationSchema>;
export type TeacherApplicationWithDetails = z.infer<typeof TeacherApplicationWithDetailsSchema>;
