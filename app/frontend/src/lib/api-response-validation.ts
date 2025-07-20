import { z } from 'zod';
import {
    GenderEnum, RoleEnum,
    GradeLevelEnum,
    HighestDegreeEnum,
    ExperienceYearEnum,
    ScheduleEnum,
    MaritalStatusEnum,
    StatusEnum,
    EventPurposeEnum,
    EventOrganizerEnum,
    EventLocationEnum,
    EventEligibilityEnum,
    StudentApplicationStatusEnum,
    AcademicTermEnum,
    MarkListTypeEnum,
    AcademicTermTypeEnum,
} from './enums';
import { DOBSchema } from './validations';

export const UserSchema = z.object({
    id: z.string(),
    identification: z.string(),
    role: RoleEnum,
    imagePath: z.string().optional(),
});

export const AdminSchema = z.object({
    id: z.string().optional(),
    userId: z.string().optional(),
    firstName: z.string(),
    fatherName: z.string(),
    grandFatherName: z.string(),
    dateOfBirth: DOBSchema,
    gender: GenderEnum,
    email: z.string().email(),
    phone: z.string(),
    address: z.string(),
});

export const StudentSchema = z.object({
    id: z.string().optional(),
    startingGradeId: z.string(),
    firstName: z.string(),
    fatherName: z.string(),
    dateOfBirth: DOBSchema,
    gender: GenderEnum,
    address: z.string(),
    city: z.string(),
    state: z.string(),
    postalCode: z.string(),
    fatherPhone: z.string(),
    motherPhone: z.string(),
    parentEmail: z.string().email(),
    grandFatherName: z.string().optional(),
    nationality: z.string().optional(),
    bloodType: z.string().optional(),
    studentPhoto: z.string().optional(),
    previousSchool: z.string().optional(),
    previousGrades: z.string().optional(),
    transportation: z.string().optional(),
    guardianName: z.string().optional(),
    guardianPhone: z.string().optional(),
    guardianRelation: z.string().optional(),
    emergencyContactName: z.string().optional(),
    emergencyContactPhone: z.string().optional(),
    disabilityDetails: z.string().optional(),
    siblingDetails: z.string().optional(),
    medicalDetails: z.string().optional(),
    siblingInSchool: z.boolean(),
    hasMedicalCondition: z.boolean(),
    hasDisability: z.boolean(),
    isTransfer: z.boolean(),
    status: StudentApplicationStatusEnum,
    userId: z.string().optional(),
});

export const TeacherSchema = z.object({
    id: z.string().optional(),
    firstName: z.string(),
    fatherName: z.string(),
    grandFatherName: z.string(),
    dateOfBirth: DOBSchema,
    gender: GenderEnum,
    nationality: z.string(),
    socialSecurityNumber: z.string(),
    address: z.string(),
    city: z.string(),
    state: z.string(),
    postalCode: z.string(),
    country: z.string(),
    primaryPhone: z.string(),
    personalEmail: z.string().email(),
    emergencyContactName: z.string(),
    emergencyContactRelation: z.string(),
    emergencyContactPhone: z.string(),
    emergencyContactEmail: z.string().email(),
    highestDegree: HighestDegreeEnum,
    university: z.string(),
    graduationYear: z.number(),
    gpa: z.number(),
    positionApplyingFor: z.string(),
    yearsOfExperience: ExperienceYearEnum,
    preferredSchedule: ScheduleEnum,
    reference1Name: z.string(),
    reference1Title: z.string(),
    reference1Organization: z.string(),
    reference1Phone: z.string(),
    reference1Email: z.string().email(),
    maritalStatus: MaritalStatusEnum.optional(),
    secondaryPhone: z.string().optional(),
    additionalDegrees: z.string().optional(),
    teachingLicense: z.boolean().optional(),
    licenseNumber: z.string().optional(),
    licenseState: z.string().optional(),
    licenseExpirationDate: z.string().datetime().optional(),
    certifications: z.string().optional(),
    specializations: z.string().optional(),
    previousSchools: z.string().optional(),
    specialSkills: z.string().optional(),
    professionalDevelopment: z.string().optional(),
    hasConvictions: z.boolean(),
    convictionDetails: z.string().optional(),
    hasDisciplinaryActions: z.boolean(),
    disciplinaryDetails: z.string().optional(),
    reference2Name: z.string().optional(),
    reference2Title: z.string().optional(),
    reference2Organization: z.string().optional(),
    reference2Phone: z.string().optional(),
    reference2Email: z.string().email().optional(),
    reference3Name: z.string().optional(),
    reference3Title: z.string().optional(),
    reference3Organization: z.string().optional(),
    reference3Phone: z.string().optional(),
    reference3Email: z.string().email().optional(),
    resume: z.string().optional(),
    coverLetter: z.string().optional(),
    transcripts: z.string().optional(),
    teachingCertificate: z.string().optional(),
    backgroundCheck: z.string().optional(),
    teachingPhilosophy: z.string().optional(),
    whyTeaching: z.string().optional(),
    additionalComments: z.string().optional(),
    agreeToTerms: z.boolean(),
    agreeToBackgroundCheck: z.boolean(),
    userId: z.string().optional(),
    status: StatusEnum,
});

export const GradeSchema = z.object({
    id: z.string().optional(),
    year_id: z.string(),
    grade: z.string(),
    level: GradeLevelEnum,
    has_stream: z.boolean(),
});

export const SubjectSchema = z.object({
    id: z.string().optional(),
    name: z.string(),
    code: z.string(),
});

export const AcademicTermSchema = z.object({
    id: z.string().optional(),
    yearId: z.string(),
    name: AcademicTermEnum,
    startDate: z.string().datetime(),
    endDate: z.string().datetime(),
    registrationStart: z.string().datetime().optional(),
    registrationEnd: z.string().datetime().optional(),
});

export const AssessmentSchema = z.object({
    id: z.string().optional(),
    studentId: z.string(),
    studentTermRecordId: z.string(),
    yearlySubjectId: z.string(),
    total: z.number().optional(),
    rank: z.number().optional(),
});

export const EventSchema = z.object({
    id: z.string().optional(),
    yearId: z.string(),
    title: z.string(),
    purpose: EventPurposeEnum,
    organizer: EventOrganizerEnum,
    startDate: z.string().datetime(),
    endDate: z.string().datetime(),
    startTime: z.string().datetime(),
    endTime: z.string().datetime(),
    location: EventLocationEnum.optional(),
    isHybrid: z.boolean(),
    onlineLink: z.string().optional(),
    eligibility: EventEligibilityEnum.optional(),
    hasFee: z.boolean(),
    feeAmount: z.number(),
    description: z.string().optional(),
});

export const MarkListSchema = z.object({
    id: z.string().optional(),
    studentId: z.string(),
    studentTermRecordId: z.string(),
    yearlySubjectId: z.string(),
    type: MarkListTypeEnum,
    percentage: z.number().optional(),
    score: z.number().optional(),
});

export const RegistrationSchema = z.object({
    id: z.string().optional(),
    studentId: z.string(),
    subjectId: z.string(),
    semesterId: z.string(),
    registrationDate: z.string().datetime(),
});

export const SectionSchema = z.object({
    id: z.string().optional(),
    section: z.string().optional(),
});

export const StreamSchema = z.object({
    id: z.string().optional(),
    yearId: z.string(),
    name: z.string(),
});

export const StudentTermRecordSchema = z.object({
    id: z.string().optional(),
    studentId: z.string(),
    academicTermId: z.string(),
    sectionId: z.string(),
    studentYearRecordId: z.string().optional(),
    average: z.number().optional(),
    rank: z.number().optional(),
});

export const StudentYearRecordSchema = z.object({
    id: z.string().optional(),
    studentId: z.string(),
    gradeId: z.string(),
    yearId: z.string(),
    streamId: z.string().optional(),
    finalScore: z.number().optional(),
    rank: z.number().optional(),
});

export const SubjectYearlyAverageSchema = z.object({
    id: z.string().optional(),
    studentId: z.string(),
    yearlySubjectId: z.string(),
    studentYearRecordId: z.string().optional(),
    average: z.number().optional(),
    rank: z.number().optional(),
});

export const TeacherRecordSchema = z.object({
    id: z.string().optional(),
    teacherId: z.string(),
    academicTermId: z.string(),
});

export const YearSchema = z.object({
    id: z.string().optional(),
    calendarType: AcademicTermTypeEnum,
    academicYear: z.string(),
    ethiopianYear: z.number(),
    gregorianYear: z.string().optional(),
    startDate: z.string().datetime(),
    endDate: z.string().datetime(),
    status: z.string().optional(),
    createdAt: z.string().datetime().optional(),
    updatedAt: z.string().datetime().optional(),
});

export const YearlySubjectSchema = z.object({
    id: z.string().optional(),
    yearId: z.string().optional(),
    subjectId: z.string(),
    gradeId: z.string(),
    streamId: z.string().optional(),
});

export const TeacherSubjectLinkSchema = z.object({
    id: z.string().optional(),
    teacherId: z.string(),
    subjectId: z.string(),
});

export const TeacherGradeLinkSchema = z.object({
    id: z.string().optional(),
    teacherId: z.string(),
    gradeId: z.string(),
});

// Relationships
export const UserWithAdminSchema = UserSchema.extend({ admin: AdminSchema });
export const UserWithTeacherSchema = UserSchema.extend({ teacher: TeacherSchema });
export const UserWithStudentSchema = UserSchema.extend({ student: StudentSchema });
export type UserProfile = z.infer<typeof UserWithAdminSchema> | z.infer<typeof UserWithTeacherSchema> | z.infer<typeof UserWithStudentSchema>;

export const GradeWithSectionsSchema = GradeSchema.extend({
    sections: z.array(SectionSchema).optional()
});
