import { baseApi as api } from "./base-api";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    login: build.mutation<LoginApiResponse, LoginApiArg>({
      query: (queryArg) => ({
        url: `/api/v1/auth/login`,
        method: "POST",
        body: new URLSearchParams({
          username: queryArg.bodyLoginCredential.username,
          password: queryArg.bodyLoginCredential.password,
        }),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }),
    }),
    logout: build.mutation<LogoutApiResponse, LogoutApiArg>({
      query: () => ({ url: `/api/v1/auth/logout`, method: "POST" }),
    }),
    registerNewAdmin: build.mutation<
      RegisterNewAdminApiResponse,
      RegisterNewAdminApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/register/admins`,
        method: "POST",
        body: queryArg.adminSchema,
      }),
    }),
    registerNewStudent: build.mutation<
      RegisterNewStudentApiResponse,
      RegisterNewStudentApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/register/students`,
        method: "POST",
        body: queryArg.studentWithRelatedSchema,
      }),
    }),
    registerNewTeacher: build.mutation<
      RegisterNewTeacherApiResponse,
      RegisterNewTeacherApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/register/teachers`,
        method: "POST",
        body: queryArg.teacherWithRelatedSchema,
      }),
    }),
    getYears: build.query<GetYearsApiResponse, GetYearsApiArg>({
      query: () => ({ url: `/api/v1/years/` }),
    }),
    getYearById: build.query<GetYearByIdApiResponse, GetYearByIdApiArg>({
      query: (queryArg) => ({ url: `/api/v1/years/${queryArg.yearId}` }),
    }),
    getGradesByYearId: build.query<
      GetGradesByYearIdApiResponse,
      GetGradesByYearIdApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/years/${queryArg.yearId}/grades` }),
    }),
    getSubjectsByYearId: build.query<
      GetSubjectsByYearIdApiResponse,
      GetSubjectsByYearIdApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/years/${queryArg.yearId}/subjects`,
      }),
    }),
    getGradeById: build.query<GetGradeByIdApiResponse, GetGradeByIdApiArg>({
      query: (queryArg) => ({ url: `/api/v1/grades/${queryArg.gradeId}` }),
    }),
    getStreamsByGradeId: build.query<
      GetStreamsByGradeIdApiResponse,
      GetStreamsByGradeIdApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/grades/${queryArg.gradeId}/streams`,
      }),
    }),
    getSectionsByGradeId: build.query<
      GetSectionsByGradeIdApiResponse,
      GetSectionsByGradeIdApiArg
    >({
      query: (queryArg) => ({
        url: `/api/v1/grades/${queryArg.gradeId}/sections`,
      }),
    }),
    getSubjectById: build.query<
      GetSubjectByIdApiResponse,
      GetSubjectByIdApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/subjects/${queryArg.subjectId}` }),
    }),
    getStreamById: build.query<GetStreamByIdApiResponse, GetStreamByIdApiArg>({
      query: (queryArg) => ({ url: `/api/v1/streams/${queryArg.streamId}` }),
    }),
    getSectionById: build.query<
      GetSectionByIdApiResponse,
      GetSectionByIdApiArg
    >({
      query: (queryArg) => ({ url: `/api/v1/sections/${queryArg.sectionId}` }),
    }),
    getLoggedInUser: build.query<
      GetLoggedInUserApiResponse,
      GetLoggedInUserApiArg
    >({
      query: () => ({ url: `/api/v1/me/` }),
    }),
    getAdminBasicInfo: build.query<
      GetAdminBasicInfoApiResponse,
      GetAdminBasicInfoApiArg
    >({
      query: () => ({ url: `/api/v1/me/admin` }),
    }),
    getTeacherBasicInfo: build.query<
      GetTeacherBasicInfoApiResponse,
      GetTeacherBasicInfoApiArg
    >({
      query: () => ({ url: `/api/v1/me/teacher` }),
    }),
    getStudentBasicInfo: build.query<
      GetStudentBasicInfoApiResponse,
      GetStudentBasicInfoApiArg
    >({
      query: () => ({ url: `/api/v1/me/student` }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as api };
export type LoginApiResponse = /** status 200 Successful Response */ Token;
export type LoginApiArg = {
  bodyLoginCredential: BodyLoginCredential;
};
export type LogoutApiResponse = /** status 200 Successful Response */ {
  [key: string]: any;
};
export type LogoutApiArg = void;
export type RegisterNewAdminApiResponse =
  /** status 200 Successful Response */ SuccessResponseSchemaRegistrationResponseNoneTypeNoneType;
export type RegisterNewAdminApiArg = {
  adminSchema: AdminSchema;
};
export type RegisterNewStudentApiResponse =
  /** status 200 Successful Response */ SuccessResponseSchemaRegistrationResponseNoneTypeNoneType;
export type RegisterNewStudentApiArg = {
  studentWithRelatedSchema: StudentWithRelatedSchema;
};
export type RegisterNewTeacherApiResponse =
  /** status 200 Successful Response */ SuccessResponseSchemaRegistrationResponseNoneTypeNoneType;
export type RegisterNewTeacherApiArg = {
  teacherWithRelatedSchema: TeacherWithRelatedSchema;
};
export type GetYearsApiResponse =
  /** status 200 Successful Response */ YearWithRelatedSchema[];
export type GetYearsApiArg = void;
export type GetYearByIdApiResponse =
  /** status 200 Successful Response */ YearWithRelatedSchema;
export type GetYearByIdApiArg = {
  yearId: string;
};
export type GetGradesByYearIdApiResponse =
  /** status 200 Successful Response */ GradeWithRelatedSchema[];
export type GetGradesByYearIdApiArg = {
  yearId: string;
};
export type GetSubjectsByYearIdApiResponse =
  /** status 200 Successful Response */ SubjectWithRelatedSchema[];
export type GetSubjectsByYearIdApiArg = {
  yearId: string;
};
export type GetGradeByIdApiResponse =
  /** status 200 Successful Response */ GradeWithRelatedSchema;
export type GetGradeByIdApiArg = {
  gradeId: string;
};
export type GetStreamsByGradeIdApiResponse =
  /** status 200 Successful Response */ StreamWithRelatedSchema[];
export type GetStreamsByGradeIdApiArg = {
  gradeId: string;
};
export type GetSectionsByGradeIdApiResponse =
  /** status 200 Successful Response */ SectionWithRelatedSchema[];
export type GetSectionsByGradeIdApiArg = {
  gradeId: string;
};
export type GetSubjectByIdApiResponse =
  /** status 200 Successful Response */ SubjectWithRelatedSchema;
export type GetSubjectByIdApiArg = {
  subjectId: string;
};
export type GetStreamByIdApiResponse =
  /** status 200 Successful Response */ StreamWithRelatedSchema;
export type GetStreamByIdApiArg = {
  streamId: string;
};
export type GetSectionByIdApiResponse =
  /** status 200 Successful Response */ SectionWithRelatedSchema;
export type GetSectionByIdApiArg = {
  sectionId: string;
};
export type GetLoggedInUserApiResponse =
  /** status 200 Successful Response */ UserSchema;
export type GetLoggedInUserApiArg = void;
export type GetAdminBasicInfoApiResponse =
  /** status 200 Successful Response */ AdminInfo;
export type GetAdminBasicInfoApiArg = void;
export type GetTeacherBasicInfoApiResponse =
  /** status 200 Successful Response */ TeacherInfo;
export type GetTeacherBasicInfoApiArg = void;
export type GetStudentBasicInfoApiResponse =
  /** status 200 Successful Response */ StudentInfo;
export type GetStudentBasicInfoApiArg = void;
export type Token = {
  access_token: string;
  token_type: string;
};
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
};
export type BodyLoginCredential = {
  grant_type?: string | null;
  username: string;
  password: string;
  scope?: string;
  client_id?: string | null;
  client_secret?: string | null;
};
export type RegistrationResponse = {
  id: string;
};
export type SuccessResponseSchemaRegistrationResponseNoneTypeNoneType = {
  data: RegistrationResponse;
  message?: string;
  meta?: null;
  links?: null;
};
export type GenderEnum = "male" | "female";
export type AdminSchema = {
  id?: string | null;
  userId?: string | null;
  firstName: string;
  fatherName: string;
  grandFatherName: string;
  dateOfBirth: string;
  gender: GenderEnum;
  email: string;
  phone: string;
  address: string;
};
export type GradeLevelEnum = "primary" | "middle school" | "high school";
export type GradeSchema = {
  id?: string | null;
  yearId: string;
  grade: string;
  level: GradeLevelEnum;
  hasStream?: boolean;
};
export type RoleEnum = "admin" | "teacher" | "student";
export type UserSchema = {
  id: string;
  identification: string;
  role: RoleEnum;
  imagePath?: string | null;
  createdAt: string;
};
export type StudentTermRecordSchema = {
  id?: string | null;
  studentId: string;
  academicTermId: string;
  gradeId: string;
  sectionId: string;
  streamId?: string | null;
  average?: number | null;
  rank?: number | null;
};
export type StudentYearRecordSchema = {
  id?: string | null;
  studentId: string;
  gradeId: string;
  yearId: string;
  streamId?: string | null;
  finalScore?: number | null;
  rank?: number | null;
};
export type SubjectYearlyAverageSchema = {
  id?: string | null;
  studentId: string;
  yearlySubjectId: string;
  studentYearRecordId?: string | null;
  average?: number | null;
  rank?: number | null;
};
export type AssessmentSchema = {
  id?: string | null;
  studentId: string;
  studentTermRecordId: string;
  yearlySubjectId: string;
  total?: number | null;
  rank?: number | null;
};
export type AcademicTermTypeEnum = "Semester" | "Quarter";
export type AcademicYearStatusEnum =
  | "upcoming"
  | "active"
  | "completed"
  | "archived";
export type YearSchema = {
  id: string;
  calendarType: AcademicTermTypeEnum;
  name: string;
  startDate: string;
  endDate: string;
  status: AcademicYearStatusEnum;
  createdAt: string;
  updatedAt: string;
};
export type AcademicTermEnum =
  | "First Term"
  | "Second Term"
  | "Third Term"
  | "Fourth Term";
export type AcademicTermSchema = {
  id?: string | null;
  yearId: string;
  name: AcademicTermEnum;
  startDate: string;
  endDate: string;
  registrationStart?: string | null;
  registrationEnd?: string | null;
};
export type SubjectSchema = {
  id?: string | null;
  yearId: string;
  name: string;
  code: string;
};
export type SectionSchema = {
  id?: string | null;
  gradeId: string;
  section?: string | null;
};
export type MarkListTypeEnum =
  | "Test"
  | "Quiz"
  | "Assignment"
  | "Midterm"
  | "Final";
export type MarkListSchema = {
  id?: string | null;
  studentId: string;
  studentTermRecordId: string;
  subjectId: string;
  type: MarkListTypeEnum;
  percentage?: number | null;
  score?: number | null;
};
export type BloodTypeEnum =
  | "A+"
  | "A-"
  | "B+"
  | "B-"
  | "AB+"
  | "AB-"
  | "O+"
  | "O-"
  | "unknown";
export type StudentApplicationStatusEnum =
  | "pending"
  | "under-review"
  | "documents-required"
  | "approved"
  | "rejected"
  | "enrolled";
export type StudentWithRelatedSchema = {
  startingGrade?: GradeSchema | null;
  user?: UserSchema | null;
  termRecords?: StudentTermRecordSchema[] | null;
  studentYearRecords?: StudentYearRecordSchema[] | null;
  subjectYearlyAverages?: SubjectYearlyAverageSchema[] | null;
  assessments?: AssessmentSchema[] | null;
  /** List of years the student is associated with. */
  years?: YearSchema[] | null;
  /** List of academic terms the student is associated with. */
  academicTerms?: AcademicTermSchema[] | null;
  /** List of grades the student is associated with. */
  grades?: GradeSchema[] | null;
  /** List of subjects the student is associated with. */
  subjects?: SubjectSchema[] | null;
  /** List of sections the student is associated with. */
  sections?: SectionSchema[] | null;
  /** List of mark lists associated with the student. */
  markLists?: MarkListSchema[] | null;
  id?: string | null;
  firstName: string;
  fatherName: string;
  dateOfBirth: string;
  gender: GenderEnum;
  address: string;
  city: string;
  state: string;
  postalCode: string;
  fatherPhone: string;
  motherPhone: string;
  parentEmail: string;
  grandFatherName?: string | null;
  nationality?: string | null;
  bloodType?: BloodTypeEnum;
  studentPhoto?: string | null;
  previousSchool?: string | null;
  previousGrades?: string | null;
  transportation?: string | null;
  guardianName?: string | null;
  guardianPhone?: string | null;
  guardianRelation?: string | null;
  emergencyContactName?: string | null;
  emergencyContactPhone?: string | null;
  disabilityDetails?: string | null;
  siblingDetails?: string | null;
  medicalDetails?: string | null;
  siblingInSchool?: boolean;
  hasMedicalCondition?: boolean;
  hasDisability?: boolean;
  isTransfer?: boolean;
  status?: StudentApplicationStatusEnum;
  userId?: string | null;
};
export type TeacherTermRecordSchema = {
  id: string;
  teacherId: string;
  academicTermId: string;
  subjectId: string;
  gradeId: string;
  sectionId: string;
  streamId: string | null;
};
export type HighestDegreeEnum = "bachelors" | "masters" | "doctorate";
export type ExperienceYearEnum =
  | "0"
  | "1-2"
  | "3-5"
  | "6-10"
  | "11-15"
  | "16-20"
  | "20+";
export type ScheduleEnum =
  | "full-time"
  | "part-time"
  | "flexible-hours"
  | "substitute";
export type MaritalStatusEnum =
  | "single"
  | "married"
  | "divorced"
  | "widowed"
  | "prefer-not-to-say";
export type TeacherApplicationStatus =
  | "pending"
  | "approved"
  | "rejected"
  | "interview-scheduled"
  | "under-review";
export type TeacherWithRelatedSchema = {
  user?: UserSchema | null;
  sections?: SectionSchema[] | null;
  /** List of years the teacher is associated with. */
  years?: YearSchema[] | null;
  termRecords?: TeacherTermRecordSchema[] | null;
  /** List of academic terms the teacher is associated with. */
  academicTerms?: AcademicTermSchema[] | null;
  /** List of grades the teacher is associated with. */
  grades?: GradeSchema[] | null;
  /** List of subjects the teacher is associated with. */
  subjects?: SubjectSchema[] | null;
  id?: string | null;
  firstName: string;
  fatherName: string;
  grandFatherName: string;
  dateOfBirth: string;
  gender: GenderEnum;
  nationality: string;
  socialSecurityNumber: string;
  address: string;
  city: string;
  state: string;
  postalCode: string;
  country: string;
  primaryPhone: string;
  personalEmail: string;
  emergencyContactName: string;
  emergencyContactRelation: string;
  emergencyContactPhone: string;
  emergencyContactEmail: string;
  highestDegree: HighestDegreeEnum;
  university: string;
  graduationYear: number;
  gpa: number;
  positionApplyingFor: string;
  yearsOfExperience: ExperienceYearEnum;
  preferredSchedule: ScheduleEnum;
  reference1Name: string;
  reference1Title: string;
  reference1Organization: string;
  reference1Phone: string;
  reference1Email: string;
  maritalStatus?: MaritalStatusEnum | null;
  secondaryPhone?: string | null;
  additionalDegrees?: string | null;
  teachingLicense?: boolean | null;
  licenseNumber?: string | null;
  licenseState?: string | null;
  licenseExpirationDate?: string | null;
  certifications?: string | null;
  specializations?: string | null;
  previousSchools?: string | null;
  specialSkills?: string | null;
  professionalDevelopment?: string | null;
  hasConvictions?: boolean;
  convictionDetails?: string | null;
  hasDisciplinaryActions?: boolean;
  disciplinaryDetails?: string | null;
  reference2Name?: string | null;
  reference2Title?: string | null;
  reference2Organization?: string | null;
  reference2Phone?: string | null;
  reference2Email?: string | null;
  reference3Name?: string | null;
  reference3Title?: string | null;
  reference3Organization?: string | null;
  reference3Phone?: string | null;
  reference3Email?: string | null;
  resume?: string | null;
  coverLetter?: string | null;
  transcripts?: string | null;
  teachingCertificate?: string | null;
  backgroundCheck?: string | null;
  teachingPhilosophy?: string | null;
  whyTeaching?: string | null;
  additionalComments?: string | null;
  agreeToTerms?: boolean;
  agreeToBackgroundCheck?: boolean;
  userId?: string | null;
  status?: TeacherApplicationStatus;
};
export type EventPurposeEnum =
  | "academic"
  | "cultural"
  | "sports"
  | "graduation"
  | "administration"
  | "new semester"
  | "other";
export type EventOrganizerEnum =
  | "school"
  | "school administration"
  | "student club"
  | "external organizer";
export type EventLocationEnum =
  | "auditorium"
  | "classroom"
  | "sports field"
  | "online"
  | "other";
export type EventEligibilityEnum =
  | "all"
  | "students only"
  | "faculty only"
  | "invitation only";
export type EventSchema = {
  id?: string | null;
  yearId: string;
  title: string;
  purpose: EventPurposeEnum;
  organizer: EventOrganizerEnum;
  startDate: string;
  endDate: string;
  startTime: string;
  endTime: string;
  location?: EventLocationEnum | null;
  isHybrid?: boolean;
  onlineLink?: string | null;
  eligibility?: EventEligibilityEnum | null;
  hasFee?: boolean;
  feeAmount?: number;
  description?: string | null;
};
export type StudentSchema = {
  id?: string | null;
  firstName: string;
  fatherName: string;
  dateOfBirth: string;
  gender: GenderEnum;
  address: string;
  city: string;
  state: string;
  postalCode: string;
  fatherPhone: string;
  motherPhone: string;
  parentEmail: string;
  grandFatherName?: string | null;
  nationality?: string | null;
  bloodType?: BloodTypeEnum;
  studentPhoto?: string | null;
  previousSchool?: string | null;
  previousGrades?: string | null;
  transportation?: string | null;
  guardianName?: string | null;
  guardianPhone?: string | null;
  guardianRelation?: string | null;
  emergencyContactName?: string | null;
  emergencyContactPhone?: string | null;
  disabilityDetails?: string | null;
  siblingDetails?: string | null;
  medicalDetails?: string | null;
  siblingInSchool?: boolean;
  hasMedicalCondition?: boolean;
  hasDisability?: boolean;
  isTransfer?: boolean;
  status?: StudentApplicationStatusEnum;
  userId?: string | null;
};
export type TeacherSchema = {
  id?: string | null;
  firstName: string;
  fatherName: string;
  grandFatherName: string;
  dateOfBirth: string;
  gender: GenderEnum;
  nationality: string;
  socialSecurityNumber: string;
  address: string;
  city: string;
  state: string;
  postalCode: string;
  country: string;
  primaryPhone: string;
  personalEmail: string;
  emergencyContactName: string;
  emergencyContactRelation: string;
  emergencyContactPhone: string;
  emergencyContactEmail: string;
  highestDegree: HighestDegreeEnum;
  university: string;
  graduationYear: number;
  gpa: number;
  positionApplyingFor: string;
  yearsOfExperience: ExperienceYearEnum;
  preferredSchedule: ScheduleEnum;
  reference1Name: string;
  reference1Title: string;
  reference1Organization: string;
  reference1Phone: string;
  reference1Email: string;
  maritalStatus?: MaritalStatusEnum | null;
  secondaryPhone?: string | null;
  additionalDegrees?: string | null;
  teachingLicense?: boolean | null;
  licenseNumber?: string | null;
  licenseState?: string | null;
  licenseExpirationDate?: string | null;
  certifications?: string | null;
  specializations?: string | null;
  previousSchools?: string | null;
  specialSkills?: string | null;
  professionalDevelopment?: string | null;
  hasConvictions?: boolean;
  convictionDetails?: string | null;
  hasDisciplinaryActions?: boolean;
  disciplinaryDetails?: string | null;
  reference2Name?: string | null;
  reference2Title?: string | null;
  reference2Organization?: string | null;
  reference2Phone?: string | null;
  reference2Email?: string | null;
  reference3Name?: string | null;
  reference3Title?: string | null;
  reference3Organization?: string | null;
  reference3Phone?: string | null;
  reference3Email?: string | null;
  resume?: string | null;
  coverLetter?: string | null;
  transcripts?: string | null;
  teachingCertificate?: string | null;
  backgroundCheck?: string | null;
  teachingPhilosophy?: string | null;
  whyTeaching?: string | null;
  additionalComments?: string | null;
  agreeToTerms?: boolean;
  agreeToBackgroundCheck?: boolean;
  userId?: string | null;
  status?: TeacherApplicationStatus;
};
export type YearWithRelatedSchema = {
  studentYearRecords: StudentYearRecordSchema[];
  events: EventSchema[];
  academicTerms: AcademicTermSchema[];
  grades: GradeSchema[];
  students: StudentSchema[];
  teachers: TeacherSchema[];
  subjects: SubjectSchema[];
  id: string;
  calendarType: AcademicTermTypeEnum;
  name: string;
  startDate: string;
  endDate: string;
  status: AcademicYearStatusEnum;
  createdAt: string;
  updatedAt: string;
};
export type StreamSchema = {
  id?: string | null;
  gradeId: string;
  name: string;
};
export type GradeWithRelatedSchema = {
  year: YearSchema | null;
  teacherTermRecords?: TeacherTermRecordSchema[] | null;
  studentTermRecords?: StudentTermRecordSchema[] | null;
  teachers?: TeacherSchema[];
  streams?: StreamSchema[];
  students?: StudentSchema[];
  sections?: SectionSchema[];
  subjects?: SubjectSchema[];
  id?: string | null;
  yearId: string;
  grade: string;
  level: GradeLevelEnum;
  hasStream?: boolean;
};
export type SubjectWithRelatedSchema = {
  year: YearSchema;
  teacherTermRecords?: TeacherTermRecordSchema[] | null;
  teachers?: TeacherSchema[];
  students?: StudentSchema[];
  markLists?: MarkListSchema[];
  streams?: StreamSchema[];
  grades?: GradeSchema[];
  id?: string | null;
  yearId: string;
  name: string;
  code: string;
};
export type StreamWithRelatedSchema = {
  teacherTermRecords?: TeacherTermRecordSchema[] | null;
  studentTermRecords?: StudentTermRecordSchema[] | null;
  grade?: GradeSchema | null;
  students?: StudentYearRecordSchema[] | null;
  subjects?: SubjectSchema[] | null;
  id?: string | null;
  gradeId: string;
  name: string;
};
export type SectionWithRelatedSchema = {
  teacherTermRecords?: TeacherTermRecordSchema[] | null;
  studentTermRecords?: StudentTermRecordSchema[] | null;
  grade?: GradeSchema | null;
  students?: StudentSchema[] | null;
  teachers?: TeacherSchema[] | null;
  id?: string | null;
  gradeId: string;
  section?: string | null;
};
export type AdminInfo = {
  id: string;
  identification: string;
  role: RoleEnum;
  imagePath?: string | null;
  createdAt: string;
  admin: AdminSchema;
};
export type TeacherInfo = {
  id: string;
  identification: string;
  role: RoleEnum;
  imagePath?: string | null;
  createdAt: string;
  teacher: TeacherSchema;
};
export type StudentInfo = {
  id: string;
  identification: string;
  role: RoleEnum;
  imagePath?: string | null;
  createdAt: string;
  student: StudentSchema;
};
export const {
  useLoginMutation,
  useLogoutMutation,
  useRegisterNewAdminMutation,
  useRegisterNewStudentMutation,
  useRegisterNewTeacherMutation,
  useGetYearsQuery,
  useGetYearByIdQuery,
  useGetGradesByYearIdQuery,
  useGetSubjectsByYearIdQuery,
  useGetGradeByIdQuery,
  useGetStreamsByGradeIdQuery,
  useGetSectionsByGradeIdQuery,
  useGetSubjectByIdQuery,
  useGetStreamByIdQuery,
  useGetSectionByIdQuery,
  useGetLoggedInUserQuery,
  useGetAdminBasicInfoQuery,
  useGetTeacherBasicInfoQuery,
  useGetStudentBasicInfoQuery,
} = injectedRtkApi;
