import { z } from "zod"
import { ExperienceYearEnum, GenderEnum, HighestDegreeEnum, MaritalStatusEnum, ScheduleEnum } from "./enums"

// Phone number validation regex
const phoneRegex = /^\+\(251\) [79]\d{2}-\d{6}$/

// Email validation
const emailSchema = z.string().email("Please enter a valid email address")

// Name validation (letters, spaces, hyphens, apostrophes only)
const nameSchema = z
    .string()
    .min(2, "Name must be at least 2 characters")
    .max(50, "Name must be less than 50 characters")
    .regex(/^[a-zA-Z\s'-]+$/, "Name can only contain letters, spaces, hyphens, and apostrophes")

// Phone validation
const phoneSchema = z
    .string()
    .regex(phoneRegex, "Phone number must be in format +251 9/7")
    .or(z.string().length(0))

// Required phone validation
const requiredPhoneSchema = z
    .string()
    .min(1, "Phone number is required")
    .regex(phoneRegex, "Phone number must be in format +251 9/7")

// Date validation (must be in the past and reasonable age range)
const dateOfBirthSchema = z
    .string()
    .min(1, "Date of birth is required")
    .refine((date) => {
        const birthDate = new Date(date)
        const today = new Date()
        const age = today.getFullYear() - birthDate.getFullYear()
        return age >= 3 && age <= 25
    }, "Student must be between 3 and 25 years old")

// Postal code validation (flexible for different countries)
const postalCodeSchema = z
    .string()
    .min(3, "Postal code must be at least 3 characters")
    .max(10, "Postal code must be less than 10 characters")
    .regex(/^[A-Za-z0-9\s-]+$/, "Invalid postal code format")

// File validation for student photo
const photoSchema = z
    .instanceof(File)
    .refine((file) => file.size <= 2 * 1024 * 1024, "File size must be less than 2MB")
    .refine(
        (file) => ["image/jpeg", "image/jpg", "image/png", "image/webp"].includes(file.type),
        "Only JPEG, PNG, and WebP images are allowed",
    )
    .optional()

// Main form schema
export const studentRegistrationSchema = z
    .object({
        // Personal Information
        firstName: nameSchema.min(1, "First name is required"),
        lastName: nameSchema.min(1, "Last name is required"),
        fatherName: nameSchema.min(1, "Father's name is required"),
        grandFatherName: nameSchema.optional(),
        dateOfBirth: dateOfBirthSchema,
        gender: GenderEnum,
        nationality: z
            .string()
            .min(2, "Nationality must be at least 2 characters")
            .max(50, "Nationality must be less than 50 characters")
            .regex(/^[a-zA-Z\s]+$/, "Nationality can only contain letters and spaces"),
        bloodType: z.enum(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]).optional(),
        studentPhoto: photoSchema,

        // Academic Information
        grade: z.enum(
            [
                "KG",
                "Grade 1",
                "Grade 2",
                "Grade 3",
                "Grade 4",
                "Grade 5",
                "Grade 6",
                "Grade 7",
                "Grade 8",
                "Grade 9",
                "Grade 10",
                "Grade 11",
                "Grade 12",
            ],
            {
                required_error: "Please select a grade level",
            },
        ),
        academicYear: z.enum(["2024-2025", "2025-2026", "2026-2027"], {
            required_error: "Please select an academic year",
        }),
        isTransfer: z.boolean(),
        previousSchool: z.string().optional(),
        previousGrades: z.string().optional(),

        // Contact Information
        address: z
            .string()
            .min(5, "Address must be at least 5 characters")
            .max(200, "Address must be less than 200 characters"),
        city: z
            .string()
            .min(2, "City must be at least 2 characters")
            .max(50, "City must be less than 50 characters")
            .regex(/^[a-zA-Z\s'-]+$/, "City can only contain letters, spaces, hyphens, and apostrophes"),
        state: z
            .string()
            .min(2, "State must be at least 2 characters")
            .max(50, "State must be less than 50 characters")
            .regex(/^[a-zA-Z\s'-]+$/, "State can only contain letters, spaces, hyphens, and apostrophes"),
        postalCode: postalCodeSchema,
        fatherPhone: requiredPhoneSchema,
        motherPhone: requiredPhoneSchema,
        parentEmail: emailSchema,

        // Guardian Information
        guardianName: nameSchema.optional(),
        guardianPhone: phoneSchema,
        guardianRelation: z.enum(["parent", "grandparent", "aunt-uncle", "sibling", "family-friend", "other"]),
        emergencyContactName: nameSchema.optional(),
        emergencyContactPhone: phoneSchema.optional(),

        // Medical Information
        hasMedicalCondition: z.boolean(),
        medicalDetails: z.string().optional(),
        hasDisability: z.boolean(),
        disabilityDetails: z.string().optional(),
        requiresAccommodation: z.boolean(),
        accommodationDetails: z.string().optional(),
        allergies: z.string().max(500, "Allergies description must be less than 500 characters").optional(),

        // Additional Information
        languageAtHome: z
            .string()
            .max(50, "Language must be less than 50 characters")
            .regex(/^[a-zA-Z\s,]+$/, "Language can only contain letters, spaces, and commas")
            .optional(),
        transportation: z.enum(["school-bus", "parent-drop", "walk", "bicycle", "other"]).optional(),
        lunchProgram: z.boolean(),
        extracurriculars: z.array(z.string()).optional(),
        siblingInSchool: z.boolean(),
        siblingDetails: z.string().max(300, "Sibling details must be less than 300 characters").optional(),
    })
    .refine(
        (data) => {
            if (data.isTransfer && !data.previousSchool) {
                return false
            }
            return true
        },
        {
            message: "Previous school name is required for transfer students",
            path: ["previousSchool"],
        },
    )
    .refine(
        (data) => {
            if (data.hasMedicalCondition && (!data.medicalDetails || data.medicalDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Medical condition details are required when medical condition is selected",
            path: ["medicalDetails"],
        },
    )
    .refine(
        (data) => {
            if (data.hasDisability && (!data.disabilityDetails || data.disabilityDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Disability details are required when disability is selected",
            path: ["disabilityDetails"],
        },
    )
    .refine(
        (data) => {
            if (data.requiresAccommodation && (!data.accommodationDetails || data.accommodationDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Accommodation details are required when special accommodation is selected",
            path: ["accommodationDetails"],
        },
    )
    .refine(
        (data) => {
            if (data.siblingInSchool && (!data.siblingDetails || data.siblingDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Sibling details are required when sibling in school is selected",
            path: ["siblingDetails"],
        },
    )

export type StudentRegistrationFormData = z.infer<typeof studentRegistrationSchema>

// Individual field schemas for step-by-step validation
export const step1Schema = z.object({
    firstName: nameSchema.min(1, "First name is required"),
    lastName: nameSchema.min(1, "Last name is required"),
    fatherName: nameSchema.min(1, "Father's name is required"),
    grandFatherName: nameSchema.optional(),
    dateOfBirth: dateOfBirthSchema,
    gender: GenderEnum,
    nationality: z
        .string()
        .min(2, "Nationality must be at least 2 characters")
        .max(50, "Nationality must be less than 50 characters")
        .regex(/^[a-zA-Z\s]+$/, "Nationality can only contain letters and spaces")
        .optional(),
    bloodType: z.enum(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]).optional(),
    languageAtHome: z
        .string()
        .max(50, "Language must be less than 50 characters")
        .regex(/^[a-zA-Z\s,]+$/, "Language can only contain letters, spaces, and commas")
        .optional(),
    studentPhoto: photoSchema,
})

export const step2Schema = z
    .object({
        grade: z.enum(
            [
                "KG",
                "Grade 1",
                "Grade 2",
                "Grade 3",
                "Grade 4",
                "Grade 5",
                "Grade 6",
                "Grade 7",
                "Grade 8",
                "Grade 9",
                "Grade 10",
                "Grade 11",
                "Grade 12",
            ],
            {
                required_error: "Please select a grade level",
            },
        ),
        academicYear: z.enum(["2024-2025", "2025-2026", "2026-2027"], {
            required_error: "Please select an academic year",
        }),
        isTransfer: z.boolean(),
        previousSchool: z.string().optional(),
        previousGrades: z.string().optional(),
        transportation: z.enum(["school-bus", "parent-drop", "walk", "bicycle", "other"]).optional(),
        lunchProgram: z.boolean(),
    })
    .refine(
        (data) => {
            if (data.isTransfer && !data.previousSchool) {
                return false
            }
            return true
        },
        {
            message: "Previous school name is required for transfer students",
            path: ["previousSchool"],
        },
    )

export const step3Schema = z.object({
    address: z
        .string()
        .min(5, "Address must be at least 5 characters")
        .max(200, "Address must be less than 200 characters"),
    city: z
        .string()
        .min(2, "City must be at least 2 characters")
        .max(50, "City must be less than 50 characters")
        .regex(/^[a-zA-Z\s'-]+$/, "City can only contain letters, spaces, hyphens, and apostrophes"),
    state: z
        .string()
        .min(2, "State must be at least 2 characters")
        .max(50, "State must be less than 50 characters")
        .regex(/^[a-zA-Z\s'-]+$/, "State can only contain letters, spaces, hyphens, and apostrophes"),
    postalCode: postalCodeSchema,
    fatherPhone: requiredPhoneSchema,
    motherPhone: requiredPhoneSchema,
    parentEmail: emailSchema,
})

export const step4Schema = z
    .object({
        guardianName: nameSchema.optional(),
        guardianPhone: phoneSchema,
        guardianRelation: z.enum(["parent", "grandparent", "aunt-uncle", "sibling", "family-friend", "other"]),
        emergencyContactName: nameSchema.optional(),
        emergencyContactPhone: phoneSchema.optional(),
        siblingInSchool: z.boolean(),
        siblingDetails: z.string().max(300, "Sibling details must be less than 300 characters").optional(),
    })
    .refine(
        (data) => {
            if (data.siblingInSchool && (!data.siblingDetails || data.siblingDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Sibling details are required when sibling in school is selected",
            path: ["siblingDetails"],
        },
    )

export const step5Schema = z
    .object({
        hasMedicalCondition: z.boolean(),
        medicalDetails: z.string().optional(),
        hasDisability: z.boolean(),
        disabilityDetails: z.string().optional(),
        requiresAccommodation: z.boolean(),
        accommodationDetails: z.string().optional(),
        allergies: z.string().max(500, "Allergies description must be less than 500 characters").optional(),
    })
    .refine(
        (data) => {
            if (data.hasMedicalCondition && (!data.medicalDetails || data.medicalDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Medical condition details are required when medical condition is selected",
            path: ["medicalDetails"],
        },
    )
    .refine(
        (data) => {
            if (data.hasDisability && (!data.disabilityDetails || data.disabilityDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Disability details are required when disability is selected",
            path: ["disabilityDetails"],
        },
    )
    .refine(
        (data) => {
            if (data.requiresAccommodation && (!data.accommodationDetails || data.accommodationDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Accommodation details are required when special accommodation is selected",
            path: ["accommodationDetails"],
        },
    )

export const step6Schema = z.object({
    extracurriculars: z.array(z.string()).optional(),
})


/************************************* TEACHER REGISTRATION Schema ********************************************/



// File validation
const documentSchema = z
    .instanceof(File)
    .refine((file) => file.size <= 5 * 1024 * 1024, "File size must be less than 5MB")
    .refine(
        (file) => ["application/pdf", "image/jpeg", "image/jpg", "image/png"].includes(file.type),
        "Only PDF, JPEG, and PNG files are allowed",
    )
    .optional()

// GPA validation
const gpaSchema = z
    .string()
    .refine((val) => {
        const num = Number.parseFloat(val)
        return !isNaN(num) && num >= 0 && num <= 4.0
    }, "GPA must be between 0.0 and 4.0")
    .optional()

// Salary expectation validation
const salarySchema = z
    .string()
    .refine((val) => {
        const num = Number.parseFloat(val.replace(/[,$]/g, ""))
        return !isNaN(num) && num >= 0 && num <= 200000
    }, "Please enter a valid salary amount")
    .optional()

// Main teacher registration schema
export const teacherRegistrationSchema = z
    .object({
        // Personal Information
        firstName: nameSchema.min(1, "First name is required"),
        fatherName: nameSchema.optional(),
        grandFatherName: nameSchema.min(1, "Last name is required"),
        dateOfBirth: dateOfBirthSchema,
        gender: GenderEnum,
        nationality: z
            .string()
            .min(2, "Nationality must be at least 2 characters")
            .max(50, "Nationality must be less than 50 characters")
            .regex(/^[a-zA-Z\s]+$/, "Nationality can only contain letters and spaces"),
        maritalStatus: MaritalStatusEnum.optional(),
        socialSecurityNumber: z
            .string()
            .regex(/^\d{3}-\d{2}-\d{4}$/, "SSN must be in format 123-45-6789")
            .optional(),
        profilePhoto: documentSchema,

        // Contact Information
        address: z
            .string()
            .min(5, "Address must be at least 5 characters")
            .max(200, "Address must be less than 200 characters"),
        city: z
            .string()
            .min(2, "City must be at least 2 characters")
            .max(50, "City must be less than 50 characters")
            .regex(/^[a-zA-Z\s'-]+$/, "City can only contain letters, spaces, hyphens, and apostrophes"),
        state: z
            .string()
            .min(2, "State must be at least 2 characters")
            .max(50, "State must be less than 50 characters")
            .regex(/^[a-zA-Z\s'-]+$/, "State can only contain letters, spaces, hyphens, and apostrophes"),
        postalCode: postalCodeSchema,
        country: z.string().min(2, "Country is required"),
        primaryPhone: requiredPhoneSchema,
        secondaryPhone: phoneSchema.optional(),
        personalEmail: emailSchema,

        // Emergency Contact
        emergencyContactName: nameSchema.min(1, "Emergency contact name is required"),
        emergencyContactRelation: z.string().min(1, "Relationship is required"),
        emergencyContactPhone: requiredPhoneSchema,

        // Educational Background
        highestDegree: HighestDegreeEnum,
        university: z.string().min(1, "University name is required"),
        graduationYear: z.string().refine((year) => {
            const num = Number.parseInt(year)
            const currentYear = new Date().getFullYear()
            return num >= 1950 && num <= currentYear
        }, "Please enter a valid graduation year"),
        gpa: gpaSchema,

        // Teaching Certifications & Licenses
        teachingLicense: z.boolean(),
        licenseNumber: z.string().optional(),
        licenseState: z.string().optional(),
        licenseExpirationDate: z.string().optional(),

        // Teaching Experience
        yearsOfExperience: ExperienceYearEnum,
        previousSchools: z.string().optional(),
        subjectsToTeach: z.array(z.string()).min(1, "Please select at least one subject to teach"),
        gradeLevelsToTeach: z.array(z.string()).min(1, "Please select at least one grade level"),
        preferredSchedule: ScheduleEnum.optional(),

        // Professional Skills & Qualifications
        specialSkills: z.string().optional(),

        // Employment Information
        positionApplyingFor: z.string().min(1, "Position is required"),
        salaryExpectation: salarySchema,

        // Background & References
        hasConvictions: z.boolean(),
        convictionDetails: z.string().optional(),
        hasDisciplinaryActions: z.boolean(),
        disciplinaryDetails: z.string().optional(),

        reference1Name: nameSchema.min(1, "First reference name is required"),
        reference1Title: z.string().min(1, "First reference title is required"),
        reference1Organization: z.string().min(1, "First reference organization is required"),
        reference1Phone: requiredPhoneSchema,
        reference1Email: emailSchema,
        reference2Name: nameSchema.optional(),
        reference2Title: z.string().optional(),
        reference2Organization: z.string().optional(),
        reference2Phone: phoneSchema.optional(),
        reference2Email: emailSchema.optional(),
        reference3Name: nameSchema.optional(),
        reference3Title: z.string().optional(),
        reference3Organization: z.string().optional(),
        reference3Phone: phoneSchema.optional(),
        reference3Email: emailSchema.optional(),

        // Documents
        resume: documentSchema,
        coverLetter: documentSchema,
        transcripts: documentSchema,
        teachingCertificate: documentSchema,
        backgroundCheck: documentSchema,

        // Additional Information
        teachingPhilosophy: z.string().max(1000, "Teaching philosophy must be less than 1000 characters").optional(),
        whyTeaching: z.string().max(500, "Response must be less than 500 characters").optional(),
        additionalComments: z.string().max(500, "Comments must be less than 500 characters").optional(),
        agreeToTerms: z.boolean().refine((val) => val === true, "You must agree to the terms and conditions"),
        agreeToBackgroundCheck: z.boolean().refine((val) => val === true, "You must agree to background check"),
    })
    .refine(
        (data) => {
            if (data.teachingLicense && !data.licenseNumber) {
                return false
            }
            return true
        },
        {
            message: "License number is required when you have a teaching license",
            path: ["licenseNumber"],
        },
    )
    .refine(
        (data) => {
            if (data.teachingLicense && !data.licenseState) {
                return false
            }
            return true
        },
        {
            message: "License state is required when you have a teaching license",
            path: ["licenseState"],
        },
    )
    .refine(
        (data) => {
            if (data.teachingLicense && !data.licenseExpirationDate) {
                return false
            }
            return true
        },
        {
            message: "License expiration date is required when you have a teaching license",
            path: ["licenseExpirationDate"],
        },
    )
    .refine(
        (data) => {
            if (data.hasConvictions && (!data.convictionDetails || data.convictionDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Conviction details are required when you have criminal convictions",
            path: ["convictionDetails"],
        },
    )
    .refine(
        (data) => {
            if (data.hasDisciplinaryActions && (!data.disciplinaryDetails || data.disciplinaryDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Disciplinary action details are required",
            path: ["disciplinaryDetails"],
        },
    )

export type TeacherRegistrationFormData = z.infer<typeof teacherRegistrationSchema>

// Step schemas for validation
export const teacherStep1Schema = z.object({
    firstName: nameSchema.min(1, "First name is required"),
    fatherName: nameSchema.optional(),
    grandFatherName: nameSchema.min(1, "Last name is required"),
    dateOfBirth: dateOfBirthSchema,
    gender: GenderEnum,
    nationality: z
        .string()
        .min(2, "Nationality must be at least 2 characters")
        .max(50, "Nationality must be less than 50 characters")
        .regex(/^[a-zA-Z\s]+$/, "Nationality can only contain letters and spaces"),
    maritalStatus: MaritalStatusEnum.optional(),
    socialSecurityNumber: z
        .string()
        .regex(/^\d{3}-\d{2}-\d{4}$/, "SSN must be in format 123-45-6789")
        .optional(),
    profilePhoto: documentSchema,
})

export const teacherStep2Schema = z.object({
    address: z
        .string()
        .min(5, "Address must be at least 5 characters")
        .max(200, "Address must be less than 200 characters"),
    city: z
        .string()
        .min(2, "City must be at least 2 characters")
        .max(50, "City must be less than 50 characters")
        .regex(/^[a-zA-Z\s'-]+$/, "City can only contain letters, spaces, hyphens, and apostrophes"),
    state: z
        .string()
        .min(2, "State must be at least 2 characters")
        .max(50, "State must be less than 50 characters")
        .regex(/^[a-zA-Z\s'-]+$/, "State can only contain letters, spaces, hyphens, and apostrophes"),
    postalCode: postalCodeSchema,
    country: z.string().min(2, "Country is required"),
    primaryPhone: requiredPhoneSchema,
    secondaryPhone: phoneSchema.optional(),
    personalEmail: emailSchema,
    emergencyContactName: nameSchema.min(1, "Emergency contact name is required"),
    emergencyContactRelation: z.string().min(1, "Relationship is required"),
    emergencyContactPhone: requiredPhoneSchema,
})

export const teacherStep3Schema = z.object({
    highestDegree: z.enum(["bachelors", "masters", "doctorate", "other"], {
        required_error: "Please select highest degree",
    }),
    university: z.string().min(1, "University name is required"),
    graduationYear: z.string().refine((year) => {
        const num = Number.parseInt(year)
        const currentYear = new Date().getFullYear()
        return num >= 1950 && num <= currentYear
    }, "Please enter a valid graduation year"),
    gpa: gpaSchema,
    specialSkills: z.string().optional(),
    positionApplyingFor: z.string().min(1, "Position is required"),
    salaryExpectation: salarySchema,
})

export const teacherStep4Schema = z
    .object({
        teachingLicense: z.boolean(),
        licenseNumber: z.string().optional(),
        licenseState: z.string().optional(),
        licenseExpirationDate: z.string().optional(),
        yearsOfExperience: ExperienceYearEnum,
        previousSchools: z.string().optional(),
        subjectsToTeach: z.array(z.string()).min(1, "Please select at least one subject to teach"),
        gradeLevelsToTeach: z.array(z.string()).min(1, "Please select at least one grade level"),
        preferredSchedule: ScheduleEnum.optional(),
    })
    .refine(
        (data) => {
            if (data.teachingLicense && !data.licenseNumber) {
                return false
            }
            return true
        },
        {
            message: "License number is required when you have a teaching license",
            path: ["licenseNumber"],
        },
    )
    .refine(
        (data) => {
            if (data.teachingLicense && !data.licenseState) {
                return false
            }
            return true
        },
        {
            message: "License state is required when you have a teaching license",
            path: ["licenseState"],
        },
    )
    .refine(
        (data) => {
            if (data.teachingLicense && !data.licenseExpirationDate) {
                return false
            }
            return true
        },
        {
            message: "License expiration date is required when you have a teaching license",
            path: ["licenseExpirationDate"],
        },
    )

export const teacherStep5Schema = z
    .object({
        hasConvictions: z.boolean(),
        convictionDetails: z.string().optional(),
        hasDisciplinaryActions: z.boolean(),
        disciplinaryDetails: z.string().optional(),
        reference1Name: nameSchema.min(1, "First reference name is required"),
        reference1Title: z.string().min(1, "First reference title is required"),
        reference1Organization: z.string().min(1, "First reference organization is required"),
        reference1Phone: requiredPhoneSchema,
        reference1Email: emailSchema,
        reference2Name: nameSchema.optional(),
        reference2Title: z.string().optional(),
        reference2Organization: z.string().optional(),
        reference2Phone: phoneSchema.optional(),
        reference2Email: emailSchema.optional(),
        reference3Name: nameSchema.optional(),
        reference3Title: z.string().optional(),
        reference3Organization: z.string().optional(),
        reference3Phone: phoneSchema.optional(),
        reference3Email: emailSchema.optional(),
    })
    .refine(
        (data) => {
            if (data.hasConvictions && (!data.convictionDetails || data.convictionDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Conviction details are required when you have criminal convictions",
            path: ["convictionDetails"],
        },
    )
    .refine(
        (data) => {
            if (data.hasDisciplinaryActions && (!data.disciplinaryDetails || data.disciplinaryDetails.trim().length === 0)) {
                return false
            }
            return true
        },
        {
            message: "Disciplinary action details are required",
            path: ["disciplinaryDetails"],
        },
    )

export const teacherStep6Schema = z.object({
    resume: documentSchema,
    coverLetter: documentSchema,
    transcripts: documentSchema,
    teachingCertificate: documentSchema,
    backgroundCheck: documentSchema,
    teachingPhilosophy: z.string().max(1000, "Teaching philosophy must be less than 1000 characters").optional(),
    whyTeaching: z.string().max(500, "Response must be less than 500 characters").optional(),
    additionalComments: z.string().max(500, "Comments must be less than 500 characters").optional(),
    agreeToTerms: z.boolean().refine((val) => val === true, "You must agree to the terms and conditions"),
    agreeToBackgroundCheck: z.boolean().refine((val) => val === true, "You must agree to background check"),
})
