import { z } from 'zod';
import { ISODateString } from './validations';
import {
    GenderEnum,
    RoleEnum,
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

/********************** Flat Schema ************************/
export const UserSchema = z.object({
    id: z.string(),
    identification: z.string(),
    role: RoleEnum,
    imagePath: z.string().optional(),
});

export const AdminSchema = z.object({
    id: z.string(),
    userId: z.string().optional(),
    firstName: z.string(),
    fatherName: z.string(),
    grandFatherName: z.string(),
    dateOfBirth: ISODateString,
    gender: GenderEnum,
    email: z.string().email(),
    phone: z.string(),
    address: z.string(),
});

export const StudentSchema = z.object({
    id: z.string(),
    startingGradeId: z.string(),
    firstName: z.string(),
    fatherName: z.string(),
    dateOfBirth: ISODateString,
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
    id: z.string(),
    firstName: z.string(),
    fatherName: z.string(),
    grandFatherName: z.string(),
    dateOfBirth: ISODateString,
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
    licenseExpirationDate: ISODateString.optional(),
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
    id: z.string(),
    yearId: z.string(),
    grade: z.string().min(1),
    level: GradeLevelEnum,
    hasStream: z.boolean(),
});

export const SubjectSchema = z.object({
    id: z.string(),
    name: z.string().min(1),
    code: z.string(),
});

export const AcademicTermSchema = z.object({
    id: z.string().optional(),
    yearId: z.string(),
    name: AcademicTermEnum,
    startDate: ISODateString,
    endDate: ISODateString,
    registrationStart: ISODateString.optional(),
    registrationEnd: ISODateString.optional(),
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
    startDate: ISODateString,
    endDate: ISODateString,
    startTime: ISODateString,
    endTime: ISODateString,
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
    registrationDate: ISODateString,
});

export const SectionSchema = z.object({
    id: z.string(),
    gradeId: z.string(),
    section: z.string(),
});

export const StreamSchema = z.object({
    id: z.string(),
    gradeId: z.string(),
    name: z.string().min(1),
});

export const StudentTermRecordSchema = z.object({
    id: z.string().optional(),
    studentId: z.string(),
    academicTermId: z.string(),
    gradeId: z.string(),
    sectionId: z.string(),
    streamId: z.string().optional().nullable(),
    average: z.number().optional(),
    rank: z.number().optional(),
});

export const TeacherTermRecordSchema = z.object({
    id: z.string().optional(),
    teacherId: z.string(),
    academicTermId: z.string(),
    subjectId: z.string(),
    gradeId: z.string(),
    sectionId: z.string(),
    streamId: z.string().optional().nullable()
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
    id: z.string(),
    calendarType: AcademicTermTypeEnum,
    name: z.string(),
    startDate: ISODateString,
    endDate: ISODateString,
    status: z.string(),
    createdAt: ISODateString,
    updatedAt: ISODateString,
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


/********************** Schema Relationship ************************/
export const YearRelationSchema = z.object({
    events: z.array(EventSchema),
    academicTerms: z.array(AcademicTermSchema),
    grades: z.array(GradeSchema),
    students: z.array(StudentSchema),
    teachers: z.array(TeacherSchema),
    subjects: z.array(SubjectSchema),
});

export const GradeRelationSchema = z.object({
    year: YearSchema,
    streams: z.array(StreamSchema),
    teacherTermRecords: z.array(TeacherTermRecordSchema),
    studentTermRecords: z.array(StudentTermRecordSchema),
    teachers: z.array(TeacherSchema),
    students: z.array(StudentSchema),
    sections: z.array(SectionSchema),
    subjects: z.array(SubjectSchema),
});

export const StreamRelationSchema = z.object({
    grade: GradeSchema,
    teacherTermRecords: z.array(TeacherTermRecordSchema),
    studentTermRecords: z.array(StudentTermRecordSchema),
    yearlySubjects: z.array(YearlySubjectSchema),
    students: z.array(StudentYearRecordSchema),
    subjects: z.array(SubjectSchema),
});

export const SubjectRelationSchema = z.object({
    teacherTermRecords: z.array(TeacherTermRecordSchema),
    teachers: z.array(TeacherSchema),
    grades: z.array(GradeSchema),
    streams: z.array(StreamSchema),
});

export const AcademicTermRelationSchema = z.object({
    year: YearSchema.optional(),
    teacher_term_records: z.array(TeacherTermRecordSchema).optional(),
    student_term_records: z.array(StudentTermRecordSchema).optional(),
    teacher_records: z.array(TeacherRecordSchema).optional(),
});

/********************** Schema With Relationship ************************/
export const YearWithRelationSchema = YearSchema.extend(YearRelationSchema.shape);
export const GradeWithRelationSchema = GradeSchema.extend(GradeRelationSchema.shape);
export const StreamWithRelationSchema = StreamSchema.extend(StreamRelationSchema.shape);
export const SubjectWithRelationSchema = SubjectSchema.extend(SubjectRelationSchema.shape);
export const AcademicTermWithRelationSchema = AcademicTermSchema.extend(AcademicTermRelationSchema.shape);

export const YearSetupSchema = YearSchema.extend({
    grades: z.array(
        GradeSchema.extend({
            subjects: z.array(SubjectSchema),
            sections: z.array(SectionSchema),
            streams: z.array(StreamSchema.extend({
                subjects: z.array(SubjectSchema),
            })),
        })
    ),
    subjects: z.array(
        SubjectSchema.extend({
            grades: z.array(GradeSchema.pick({ id: true })),
            streams: z.array(StreamSchema.pick({ id: true, gradeId: true })),
        })
    ),
})
