import { z } from "zod";

export const TeacherApplicationSchema = z.object({
    id: z.string(),
    applicationDate: z.string(),
    status: z.enum(["pending", "under-review", "interview-scheduled", "approved", "rejected"]),

    // Personal Information
    firstName: z.string(),
    middleName: z.string().optional(),
    lastName: z.string(),
    preferredName: z.string().optional(),
    dateOfBirth: z.string(),
    gender: z.enum(["male", "female"]),
    nationality: z.string(),
    maritalStatus: z.enum(["single", "married", "divorced", "widowed", "prefer-not-to-say"]).optional(),

    // Contact Information
    address: z.string(),
    city: z.string(),
    state: z.string(),
    postalCode: z.string(),
    country: z.string(),
    primaryPhone: z.string(),
    secondaryPhone: z.string().optional(),
    personalEmail: z.string(),
    workEmail: z.string().optional(),

    // Emergency Contact
    emergencyContactName: z.string(),
    emergencyContactRelation: z.string(),
    emergencyContactPhone: z.string(),

    // Educational Background
    highestDegree: z.enum(["bachelors", "masters", "doctorate", "other"]),
    majorSubject: z.string(),
    minorSubject: z.string().optional(),
    university: z.string(),
    graduationYear: z.string(),
    gpa: z.string().optional(),

    // Teaching Information
    teachingLicense: z.boolean(),
    licenseNumber: z.string().optional(),
    licenseState: z.string().optional(),
    licenseExpirationDate: z.string().optional(),
    certifications: z.array(z.string()),
    specializations: z.array(z.string()),
    yearsOfExperience: z.enum(["0", "1-2", "3-5", "6-10", "11-15", "16-20", "20+"]),
    previousSchools: z.string().optional(),
    subjectsToTeach: z.array(z.string()),
    gradeLevelsToTeach: z.array(z.string()),
    preferredSchedule: z.enum(["full-time", "part-time", "substitute", "flexible"]).optional(),

    // Professional Skills
    languagesSpoken: z.array(z.string()),
    technologySkills: z.array(z.string()),
    specialSkills: z.string().optional(),

    // Employment Information
    positionApplyingFor: z.string(),
    departmentPreference: z.string().optional(),
    availableStartDate: z.string(),
    salaryExpectation: z.string().optional(),
    willingToRelocate: z.boolean(),
    hasTransportation: z.boolean(),

    // Background Information
    hasConvictions: z.boolean(),
    convictionDetails: z.string().optional(),
    hasDisciplinaryActions: z.boolean(),
    disciplinaryDetails: z.string().optional(),

    // References
    reference1Name: z.string(),
    reference1Title: z.string(),
    reference1Organization: z.string(),
    reference1Phone: z.string(),
    reference1Email: z.string(),
    reference2Name: z.string().optional(),
    reference2Title: z.string().optional(),
    reference2Organization: z.string().optional(),
    reference2Phone: z.string().optional(),
    reference2Email: z.string().optional(),
    reference3Name: z.string().optional(),
    reference3Title: z.string().optional(),
    reference3Organization: z.string().optional(),
    reference3Phone: z.string().optional(),
    reference3Email: z.string().optional(),

    // Additional Information
    teachingPhilosophy: z.string().optional(),
    whyTeaching: z.string().optional(),
    additionalComments: z.string().optional(),

    // Documents and Files
    resume: z.string().optional(),
    coverLetter: z.string().optional(),
    transcripts: z.string().optional(),
    teachingCertificate: z.string().optional(),
    backgroundCheck: z.string().optional(),
    profilePhoto: z.string().optional(),
});

export type TeacherApplication = z.infer<typeof TeacherApplicationSchema>;
