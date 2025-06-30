"use client"

import { useState, useEffect } from "react"
import { z } from "zod"
import {
    teacherRegistrationSchema,
    teacherStep1Schema,
    teacherStep2Schema,
    teacherStep3Schema,
    teacherStep4Schema,
    teacherStep5Schema,
    teacherStep6Schema,
    type TeacherRegistrationFormData,
} from "@/lib/form-validation"
import { FormField, InputWithError, TextareaWithError, SelectWithError } from "@/components/form-field-with-error"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { SelectItem } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Upload, User, MapPin, GraduationCap, Award, FileText, Shield } from "lucide-react"
import { useTeacherFormPersistence } from "@/hooks/use-teacher-form-persistence"
import FormRestorationDialog from "@/components/form-restoration-dialog"
import AutoSaveIndicator from "@/components/auto-save-indicator"
import { availableGradeLevels, availableSubjects, saveTeacherRegistration } from "@/api/sharedApi"
import { toast } from "sonner"

// undefined fields are optional
const initialFormData: TeacherRegistrationFormData = {
    // Personal Information
    firstName: "",
    fatherName: undefined as any,
    grandFatherName: "",
    dateOfBirth: "",
    gender: undefined as any,
    nationality: "",
    maritalStatus: undefined,
    socialSecurityNumber: undefined,
    profilePhoto: undefined,

    // Contact Information
    address: "",
    city: "",
    state: "",
    postalCode: "",
    country: "",
    primaryPhone: "",
    secondaryPhone: "",
    personalEmail: "",

    // Emergency Contact
    emergencyContactName: "",
    emergencyContactRelation: "",
    emergencyContactPhone: "",

    // Educational Background
    highestDegree: undefined as any,
    university: "",
    graduationYear: "",
    gpa: "",

    // Teaching Certifications & Licenses
    teachingLicense: false,
    licenseNumber: "",
    licenseState: "",
    licenseExpirationDate: "",

    // Teaching Experience
    yearsOfExperience: undefined as any,
    previousSchools: "",
    subjectsToTeach: [],
    gradeLevelsToTeach: [],
    preferredSchedule: undefined,

    // Professional Skills & Qualifications
    specialSkills: "",

    // Employment Information
    positionApplyingFor: "",
    salaryExpectation: "",

    // Background & References
    hasConvictions: false,
    convictionDetails: "",
    hasDisciplinaryActions: false,
    disciplinaryDetails: "",
    reference1Name: "",
    reference1Title: "",
    reference1Organization: "",
    reference1Phone: "",
    reference1Email: "",
    reference2Name: undefined as any,
    reference2Title: undefined as any,
    reference2Organization: undefined as any,
    reference2Phone: undefined as any,
    reference2Email: undefined as any,
    reference3Name: undefined as any,
    reference3Title: undefined as any,
    reference3Organization: undefined as any,
    reference3Phone: undefined as any,
    reference3Email: undefined as any,

    // Documents
    resume: undefined,
    coverLetter: undefined,
    transcripts: undefined,
    teachingCertificate: undefined,
    backgroundCheck: undefined,

    // Additional Information
    teachingPhilosophy: "",
    whyTeaching: "",
    additionalComments: "",
    agreeToTerms: false,
    agreeToBackgroundCheck: false,
}

const stepNames = {
    1: "Personal Information",
    2: "Contact Information",
    3: "Educational Background",
    4: "Teaching Certifications & Experience",
    5: "Background Check & References",
    6: "Documents & Final Information"
}

export default function TeacherRegistrationForm() {
    const [currentStep, setCurrentStep] = useState(1)
    const [currentStepName, setCurrentStepName] = useState(stepNames[currentStep as keyof typeof stepNames] || "Unknown Step")
    const [formData, setFormData] = useState<TeacherRegistrationFormData>(initialFormData)
    const [subjects, setSubjects] = useState<string[]>([])
    const [gradeLevels, setGradeLevels] = useState<string[]>([])
    const [errors, setErrors] = useState<Record<string, string>>({})
    const [touchedFields, setTouchedFields] = useState<Record<string, boolean>>({})
    const [showRestorationDialog, setShowRestorationDialog] = useState(false)
    const [lastSaved, setLastSaved] = useState<Date>()
    const [isOnline, setIsOnline] = useState(true)

    const { saveFormData, loadFormData, clearFormData, hasSavedData } = useTeacherFormPersistence()

    const totalSteps = stepNames ? Object.keys(stepNames).length : 6
    const progress = (currentStep / totalSteps) * 100

    // Handle form restoration on component mount
    useEffect(() => {
        if (hasSavedData()) {
            const savedData = loadFormData()
            if (savedData) {
                setCurrentStep(savedData.step)
                setCurrentStepName(stepNames[savedData.step as keyof typeof stepNames] || "Unknown Step")
            }
            setShowRestorationDialog(true)
        }
    }, [hasSavedData])

    // Monitor online status
    useEffect(() => {
        const handleOnline = () => setIsOnline(true)
        const handleOffline = () => setIsOnline(false)

        window.addEventListener("online", handleOnline)
        window.addEventListener("offline", handleOffline)

        return () => {
            window.removeEventListener("online", handleOnline)
            window.removeEventListener("offline", handleOffline)
        }
    }, [])

    useEffect(() => {
        // load available subjects and grade levels
        const loadSubjectsAndGrades = async () => {
            const subjects = await availableSubjects()
            const grades = await availableGradeLevels()

            setSubjects(subjects)
            setGradeLevels(grades.map((grade) => `Grade ${grade}`))
        }

        loadSubjectsAndGrades()
    }, [])

    // Auto-save form data
    useEffect(() => {
        if (formData.firstName || formData.grandFatherName || formData.personalEmail) {
            saveFormData(formData, currentStep)
            setLastSaved(new Date())
        }
    }, [formData, currentStep, saveFormData])

    const updateFormData = (field: keyof TeacherRegistrationFormData, value: any) => {
        setFormData((prev) => ({ ...prev, [field]: value }))
    }

    const formatPhoneNumber = (value: string) => {
        const cleaned = value.replace(/\D/g, "");

        // Handle 09xxxxxxxx or 07xxxxxxxx
        let match = cleaned.match(/^0([79])(\d{2})(\d{6})$/);
        if (match) {
            return `+(251) ${match[1]}${match[2]}-${match[3]}`;
        }

        // Handle 2519xxxxxxxx or 2517xxxxxxxx
        match = cleaned.match(/^251([79])(\d{2})(\d{6})$/);
        if (match) {
            return `+(251) ${match[1]}${match[2]}-${match[3]}`;
        }

        return value;
    };

    const formatSSN = (value: string) => {
        const cleaned = value.replace(/\D/g, "")
        const match = cleaned.match(/^(\d{3})(\d{2})(\d{4})$/)
        if (match) {
            return `${match[1]}-${match[2]}-${match[3]}`
        }
        return value
    }

    const handleArrayToggle = (field: keyof TeacherRegistrationFormData, value: string) => {
        const currentArray = (formData[field] as string[]) || []
        const updated = currentArray.includes(value)
            ? currentArray.filter((item) => item !== value)
            : [...currentArray, value]
        updateFormData(field, updated)
    }

    const validateStep = (stepNumber: number): boolean => {
        let schema: z.ZodSchema
        let dataToValidate: any

        switch (stepNumber) {
            case 1:
                schema = teacherStep1Schema
                dataToValidate = {
                    firstName: formData.firstName,
                    fatherName: formData.fatherName,
                    grandFatherName: formData.grandFatherName,
                    dateOfBirth: formData.dateOfBirth,
                    gender: formData.gender,
                    nationality: formData.nationality,
                    maritalStatus: formData.maritalStatus,
                    socialSecurityNumber: formData.socialSecurityNumber,
                    profilePhoto: formData.profilePhoto,
                }
                break
            case 2:
                schema = teacherStep2Schema
                dataToValidate = {
                    address: formData.address,
                    city: formData.city,
                    state: formData.state,
                    postalCode: formData.postalCode,
                    country: formData.country,
                    primaryPhone: formData.primaryPhone,
                    secondaryPhone: formData.secondaryPhone,
                    personalEmail: formData.personalEmail,
                    emergencyContactName: formData.emergencyContactName,
                    emergencyContactRelation: formData.emergencyContactRelation,
                    emergencyContactPhone: formData.emergencyContactPhone,
                }
                break
            case 3:
                schema = teacherStep3Schema
                dataToValidate = {
                    highestDegree: formData.highestDegree,
                    university: formData.university,
                    graduationYear: formData.graduationYear,
                    gpa: formData.gpa,
                    specialSkills: formData.specialSkills,
                    positionApplyingFor: formData.positionApplyingFor,
                    salaryExpectation: formData.salaryExpectation,
                }
                break
            case 4:
                schema = teacherStep4Schema
                dataToValidate = {
                    teachingLicense: formData.teachingLicense,
                    licenseNumber: formData.licenseNumber,
                    licenseState: formData.licenseState,
                    licenseExpirationDate: formData.licenseExpirationDate,
                    yearsOfExperience: formData.yearsOfExperience,
                    previousSchools: formData.previousSchools,
                    subjectsToTeach: formData.subjectsToTeach,
                    gradeLevelsToTeach: formData.gradeLevelsToTeach,
                    preferredSchedule: formData.preferredSchedule,
                }
                break
            case 5:
                schema = teacherStep5Schema
                dataToValidate = {
                    hasConvictions: formData.hasConvictions,
                    convictionDetails: formData.convictionDetails,
                    hasDisciplinaryActions: formData.hasDisciplinaryActions,
                    disciplinaryDetails: formData.disciplinaryDetails,
                    reference1Name: formData.reference1Name,
                    reference1Title: formData.reference1Title,
                    reference1Organization: formData.reference1Organization,
                    reference1Phone: formData.reference1Phone,
                    reference1Email: formData.reference1Email,
                    reference2Name: formData.reference2Name,
                    reference2Title: formData.reference2Title,
                    reference2Organization: formData.reference2Organization,
                    reference2Phone: formData.reference2Phone,
                    reference2Email: formData.reference2Email,
                    reference3Name: formData.reference3Name,
                    reference3Title: formData.reference3Title,
                    reference3Organization: formData.reference3Organization,
                    reference3Phone: formData.reference3Phone,
                    reference3Email: formData.reference3Email,
                }
                break
            case 6:
                schema = teacherStep6Schema
                dataToValidate = {
                    resume: formData.resume,
                    coverLetter: formData.coverLetter,
                    transcripts: formData.transcripts,
                    teachingCertificate: formData.teachingCertificate,
                    backgroundCheck: formData.backgroundCheck,
                    teachingPhilosophy: formData.teachingPhilosophy,
                    whyTeaching: formData.whyTeaching,
                    additionalComments: formData.additionalComments,
                    agreeToTerms: formData.agreeToTerms,
                    agreeToBackgroundCheck: formData.agreeToBackgroundCheck,
                }
                break
            default:
                return true
        }

        try {
            schema.parse(dataToValidate)
            const stepErrors = { ...errors }
            Object.keys(dataToValidate).forEach((key) => {
                delete stepErrors[key]
            })
            setErrors(stepErrors)
            return true
        } catch (error) {
            if (error instanceof z.ZodError) {
                const newErrors: Record<string, string> = {}
                error.errors.forEach((err) => {
                    if (err.path.length > 0) {
                        newErrors[err.path[0] as string] = err.message
                    }
                })
                setErrors((prev) => ({ ...prev, ...newErrors }))
            }
            return false
        }
    }

    const validateField = (field: keyof TeacherRegistrationFormData, value: any) => {
        try {
            // Unwrap ZodEffects to access the underlying ZodObject with shape
            let schema: any = teacherRegistrationSchema
            while (schema && typeof schema.innerType === "function") {
                schema = schema.innerType()
            }
            const fieldSchema = schema.shape[field]
            if (fieldSchema) {
                fieldSchema.parse(value)
                setErrors((prev) => {
                    const newErrors = { ...prev }
                    delete newErrors[field]
                    return newErrors
                })
            }
        } catch (error) {
            if (error instanceof z.ZodError) {
                setErrors((prev) => ({
                    ...prev,
                    [field]: error.errors[0]?.message || "Invalid input",
                }))
            }
        }
    }

    const handleFieldChange = (field: keyof TeacherRegistrationFormData, value: any) => {
        value = value === "" ? undefined : value // Handle empty strings
        updateFormData(field, value)
        setTouchedFields((prev) => ({ ...prev, [field]: true }))

        // Validate field after a short delay to avoid validating while typing
        setTimeout(() => {
            validateField(field, value)
        }, 300)
    }

    const nextStep = () => {
        if (validateStep(currentStep) && currentStep < totalSteps) {
            setCurrentStep(currentStep + 1)
            setCurrentStepName(stepNames[currentStep + 1 as keyof typeof stepNames] || "Unknown Step")
        }
    }

    const prevStep = () => {
        if (currentStep > 1) {
            setCurrentStep(currentStep - 1)
            setCurrentStepName(stepNames[currentStep - 1 as keyof typeof stepNames] || "Unknown Step")
        }
    }

    const handleRestoreForm = () => {
        const savedData = loadFormData()
        if (savedData) {
            setFormData((prev) => ({ ...prev, ...savedData.data }))
            setCurrentStep(savedData.step)
            setCurrentStepName(stepNames[savedData.step as keyof typeof stepNames] || "Unknown Step")
        }
        setShowRestorationDialog(false)
    }

    const handleStartFresh = () => {
        clearFormData()
        setFormData(initialFormData)
        setCurrentStep(1)
        setShowRestorationDialog(false)
    }

    const handleFinalSubmit = async () => {
        try {
            const validatedData = teacherRegistrationSchema.parse(formData)
            clearFormData()
            const response = await saveTeacherRegistration(validatedData)
            toast.success(response.message, {
                style: { color: "green" },
            })
            alert("Registration successful! Your application has been submitted.")
            // setFormData(initialFormData) // Reset form after successful submission
            // setCurrentStep(1)
        } catch (error) {
            if (error instanceof z.ZodError) {
                const newErrors: Record<string, string> = {}
                error.errors.forEach((err) => {
                    if (err.path.length > 0) {
                        newErrors[err.path[0] as string] = err.message
                    }
                })
                setErrors(newErrors)
                alert("Please fix the errors before submitting.")
            }
        }
    }

    const renderStep = () => {
        switch (currentStep) {
            case 1:
                return (
                    <div className="space-y-6">
                        <div className="flex items-center gap-2 mb-4">
                            <User className="h-5 w-5 text-blue-600" />
                            <h3 className="text-lg font-semibold">{currentStepName}</h3>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <FormField
                                label="First Name"
                                id="firstName"
                                required
                                error={errors.firstName}
                                success={!errors.firstName && touchedFields.firstName}
                            >
                                <InputWithError
                                    id="firstName"
                                    value={formData.firstName}
                                    onChange={(e) => handleFieldChange("firstName", e.target.value)}
                                    placeholder="Enter first name"
                                    error={errors.firstName}
                                />
                            </FormField>
                            <FormField
                                label="Middle Name"
                                id="fatherName"
                                error={errors.fatherName}
                                success={!errors.fatherName && touchedFields.fatherName}
                            >
                                <InputWithError
                                    id="fatherName"
                                    value={formData.fatherName}
                                    onChange={(e) => handleFieldChange("fatherName", e.target.value)}
                                    placeholder="Enter middle name"
                                    error={errors.fatherName}
                                />
                            </FormField>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <FormField
                                label="Last Name"
                                id="grandFatherName"
                                required
                                error={errors.grandFatherName}
                                success={!errors.grandFatherName && touchedFields.grandFatherName}
                            >
                                <InputWithError
                                    id="grandFatherName"
                                    value={formData.grandFatherName}
                                    onChange={(e) => handleFieldChange("grandFatherName", e.target.value)}
                                    placeholder="Enter last name"
                                    error={errors.grandFatherName}
                                />
                            </FormField>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <FormField
                                label="Date of Birth"
                                id="dateOfBirth"
                                required
                                error={errors.dateOfBirth}
                                success={!errors.dateOfBirth && touchedFields.dateOfBirth}
                            >
                                <InputWithError
                                    id="dateOfBirth"
                                    type="date"
                                    value={formData.dateOfBirth}
                                    onChange={(e) => handleFieldChange("dateOfBirth", e.target.value)}
                                    error={errors.dateOfBirth}
                                />
                            </FormField>
                            <div className="space-y-2">
                                <Label>Gender *</Label>
                                <RadioGroup
                                    value={formData.gender}
                                    onValueChange={(value) => handleFieldChange("gender", value)}
                                    className="flex gap-4 w-14"
                                >
                                    <div className="flex items-center space-x-2">
                                        <RadioGroupItem value="male" id="male" />
                                        <Label htmlFor="male">Male</Label>
                                    </div>
                                    <div className="flex items-center space-x-2">
                                        <RadioGroupItem value="female" id="female" />
                                        <Label htmlFor="female">Female</Label>
                                    </div>
                                </RadioGroup>
                                {errors.gender && <p className="text-red-500 text-sm">{errors.gender}</p>}
                            </div>
                            <FormField
                                label="Nationality"
                                id="nationality"
                                required
                                error={errors.nationality}
                                success={!errors.nationality && touchedFields.nationality}
                            >
                                <InputWithError
                                    id="nationality"
                                    value={formData.nationality}
                                    onChange={(e) => handleFieldChange("nationality", e.target.value)}
                                    placeholder="Enter nationality"
                                    error={errors.nationality}
                                />
                            </FormField>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="maritalStatus">Marital Status</Label>
                                <SelectWithError
                                    placeholder="Select marital status"
                                    value={formData.maritalStatus}
                                    onValueChange={(value) => handleFieldChange("maritalStatus", value)}
                                    error={errors.maritalStatus}
                                >
                                    <SelectItem value="single">Single</SelectItem>
                                    <SelectItem value="married">Married</SelectItem>
                                    <SelectItem value="divorced">Divorced</SelectItem>
                                    <SelectItem value="widowed">Widowed</SelectItem>
                                    <SelectItem value="prefer-not-to-say">Prefer not to say</SelectItem>
                                </SelectWithError>
                            </div>
                            <FormField
                                label="Social Security Number"
                                id="socialSecurityNumber"
                                error={errors.socialSecurityNumber}
                                success={
                                    !errors.socialSecurityNumber &&
                                    touchedFields.socialSecurityNumber
                                }
                            >
                                <InputWithError
                                    id="socialSecurityNumber"
                                    value={formData.socialSecurityNumber}
                                    onChange={(e) => handleFieldChange("socialSecurityNumber", formatSSN(e.target.value))}
                                    placeholder="123-45-6789"
                                    error={errors.socialSecurityNumber}
                                />
                            </FormField>
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="profilePhoto">Profile Photo</Label>
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                                <div className="mt-2">
                                    <Label htmlFor="profilePhoto" className="cursor-pointer">
                                        <span className="text-blue-600 hover:text-blue-500">Upload a photo</span>
                                        <Input
                                            id="profilePhoto"
                                            type="file"
                                            accept="image/*,.pdf"
                                            className="hidden"
                                            onChange={(e) => updateFormData("profilePhoto", e.target.files?.[0] || undefined)}
                                        />
                                    </Label>
                                </div>
                                <p className="text-xs text-gray-500">PDF, PNG, JPG up to 5MB</p>
                            </div>
                        </div>
                    </div>
                )

            case 2:
                return (
                    <div className="space-y-6">
                        <div className="flex items-center gap-2 mb-4">
                            <MapPin className="h-5 w-5 text-purple-600" />
                            <h3 className="text-lg font-semibold">{currentStepName}</h3>
                        </div>

                        <FormField
                            label="Street Address"
                            id="address"
                            required
                            error={errors.address}
                            success={!errors.address && touchedFields.address}
                        >
                            <InputWithError
                                id="address"
                                value={formData.address}
                                onChange={(e) => handleFieldChange("address", e.target.value)}
                                placeholder="Enter street address"
                                error={errors.address}
                            />
                        </FormField>

                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <FormField
                                label="City"
                                id="city"
                                required
                                error={errors.city}
                                success={!errors.city && touchedFields.city}
                            >
                                <InputWithError
                                    id="city"
                                    value={formData.city}
                                    onChange={(e) => handleFieldChange("city", e.target.value)}
                                    placeholder="Enter city"
                                    error={errors.city}
                                />
                            </FormField>
                            <FormField
                                label="State/Province"
                                id="state"
                                required
                                error={errors.state}
                                success={!errors.state && touchedFields.state}
                            >
                                <InputWithError
                                    id="state"
                                    value={formData.state}
                                    onChange={(e) => handleFieldChange("state", e.target.value)}
                                    placeholder="Enter state"
                                    error={errors.state}
                                />
                            </FormField>
                            <FormField
                                label="Postal Code"
                                id="postalCode"
                                required
                                error={errors.postalCode}
                                success={!errors.postalCode && touchedFields.postalCode}
                            >
                                <InputWithError
                                    id="postalCode"
                                    value={formData.postalCode}
                                    onChange={(e) => handleFieldChange("postalCode", e.target.value)}
                                    placeholder="Enter postal code"
                                    error={errors.postalCode}
                                />
                            </FormField>
                            <FormField
                                label="Country"
                                id="country"
                                required
                                error={errors.country}
                                success={!errors.country && touchedFields.country}
                            >
                                <InputWithError
                                    id="country"
                                    value={formData.country}
                                    onChange={(e) => handleFieldChange("country", e.target.value)}
                                    placeholder="Enter country"
                                    error={errors.country}
                                />
                            </FormField>
                        </div>

                        <Separator />

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <FormField
                                label="Primary Phone Number"
                                id="primaryPhone"
                                required
                                error={errors.primaryPhone}
                                success={!errors.primaryPhone && touchedFields.primaryPhone}
                            >
                                <InputWithError
                                    id="primaryPhone"
                                    value={formData.primaryPhone}
                                    onChange={(e) => handleFieldChange("primaryPhone", formatPhoneNumber(e.target.value))}
                                    placeholder="(123) 456-7890"
                                    error={errors.primaryPhone}
                                />
                            </FormField>
                            <FormField
                                label="Secondary Phone Number"
                                id="secondaryPhone"
                                error={errors.secondaryPhone}
                                success={!errors.secondaryPhone && touchedFields.secondaryPhone}
                            >
                                <InputWithError
                                    id="secondaryPhone"
                                    value={formData.secondaryPhone}
                                    onChange={(e) => handleFieldChange("secondaryPhone", formatPhoneNumber(e.target.value))}
                                    placeholder="(123) 456-7890"
                                    error={errors.secondaryPhone}
                                />
                            </FormField>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <FormField
                                label="Personal Email"
                                id="personalEmail"
                                required
                                error={errors.personalEmail}
                                success={!errors.personalEmail && touchedFields.personalEmail}
                            >
                                <InputWithError
                                    id="personalEmail"
                                    type="email"
                                    value={formData.personalEmail}
                                    onChange={(e) => handleFieldChange("personalEmail", e.target.value)}
                                    placeholder="personal@example.com"
                                    error={errors.personalEmail}
                                />
                            </FormField>
                        </div>

                        <Separator />

                        <div className="space-y-4">
                            <h4 className="font-medium text-red-600">Emergency Contact</h4>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <FormField
                                    label="Emergency Contact Name"
                                    id="emergencyContactName"
                                    required
                                    error={errors.emergencyContactName}
                                    success={
                                        !errors.emergencyContactName &&
                                        touchedFields.emergencyContactName &&
                                        formData.emergencyContactName.length > 0
                                    }
                                >
                                    <InputWithError
                                        id="emergencyContactName"
                                        value={formData.emergencyContactName}
                                        onChange={(e) => handleFieldChange("emergencyContactName", e.target.value)}
                                        placeholder="Enter emergency contact name"
                                        error={errors.emergencyContactName}
                                    />
                                </FormField>
                                <FormField
                                    label="Relationship"
                                    id="emergencyContactRelation"
                                    required
                                    error={errors.emergencyContactRelation}
                                    success={
                                        !errors.emergencyContactRelation &&
                                        touchedFields.emergencyContactRelation &&
                                        formData.emergencyContactRelation.length > 0
                                    }
                                >
                                    <InputWithError
                                        id="emergencyContactRelation"
                                        value={formData.emergencyContactRelation}
                                        onChange={(e) => handleFieldChange("emergencyContactRelation", e.target.value)}
                                        placeholder="e.g., Spouse, Parent, Sibling"
                                        error={errors.emergencyContactRelation}
                                    />
                                </FormField>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <FormField
                                    label="Emergency Contact Phone"
                                    id="emergencyContactPhone"
                                    required
                                    error={errors.emergencyContactPhone}
                                    success={
                                        !errors.emergencyContactPhone &&
                                        touchedFields.emergencyContactPhone &&
                                        formData.emergencyContactPhone.length > 0
                                    }
                                >
                                    <InputWithError
                                        id="emergencyContactPhone"
                                        value={formData.emergencyContactPhone}
                                        onChange={(e) => handleFieldChange("emergencyContactPhone", formatPhoneNumber(e.target.value))}
                                        placeholder="(123) 456-7890"
                                        error={errors.emergencyContactPhone}
                                    />
                                </FormField>
                            </div>
                        </div>
                    </div>
                )

            case 3:
                return (
                    <div className="space-y-6">
                        <div className="flex items-center gap-2 mb-4">
                            <GraduationCap className="h-5 w-5 text-green-600" />
                            <h3 className="text-lg font-semibold">{currentStepName}</h3>
                        </div>


                        <Separator />

                        <div className="grid grid-cols-2 md:grid-cols-2 gap-4">
                            <FormField
                                label="Position Applying For"
                                id="positionApplyingFor"
                                required
                                error={errors.positionApplyingFor}
                                success={
                                    !errors.positionApplyingFor &&
                                    touchedFields.positionApplyingFor &&
                                    formData.positionApplyingFor.length > 0
                                }
                            >
                                <InputWithError
                                    id="positionApplyingFor"
                                    value={formData.positionApplyingFor}
                                    onChange={(e) => handleFieldChange("positionApplyingFor", e.target.value)}
                                    placeholder="e.g., Elementary Teacher, Math Teacher"
                                    error={errors.positionApplyingFor}
                                />
                            </FormField>

                            <FormField
                                label="Salary Expectation"
                                id="salaryExpectation"
                                required
                                error={errors.salaryExpectation}
                                success={
                                    !errors.salaryExpectation && touchedFields.salaryExpectation
                                }
                            >
                                <InputWithError
                                    id="salaryExpectation"
                                    value={formData.salaryExpectation}
                                    onChange={(e) => handleFieldChange("salaryExpectation", e.target.value)}
                                    placeholder="$50,000"
                                    error={errors.salaryExpectation}
                                />
                            </FormField>
                        </div>

                        <Separator />

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="highestDegree">Highest Degree *</Label>
                                <SelectWithError
                                    placeholder="Select highest degree"
                                    value={formData.highestDegree}
                                    onValueChange={(value) => handleFieldChange("highestDegree", value)}
                                    error={errors.highestDegree}
                                >
                                    <SelectItem value="bachelors">Bachelor's Degree</SelectItem>
                                    <SelectItem value="masters">Master's Degree</SelectItem>
                                    <SelectItem value="doctorate">Doctorate/PhD</SelectItem>
                                    <SelectItem value="other">Other</SelectItem>
                                </SelectWithError>
                                {errors.highestDegree && <p className="text-red-500 text-sm">{errors.highestDegree}</p>}
                            </div>

                            <FormField
                                label="University/College"
                                id="university"
                                required
                                error={errors.university}
                                success={!errors.university && touchedFields.university}
                            >
                                <InputWithError
                                    id="university"
                                    value={formData.university}
                                    onChange={(e) => handleFieldChange("university", e.target.value)}
                                    placeholder="Enter university name"
                                    error={errors.university}
                                />
                            </FormField>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <FormField
                                label="Graduation Year"
                                id="graduationYear"
                                required
                                error={errors.graduationYear}
                                success={!errors.graduationYear && touchedFields.graduationYear}
                            >
                                <InputWithError
                                    id="graduationYear"
                                    type="number"
                                    min="1950"
                                    max={new Date().getFullYear()}
                                    value={formData.graduationYear}
                                    onChange={(e) => handleFieldChange("graduationYear", e.target.value)}
                                    placeholder="2020"
                                    error={errors.graduationYear}
                                />
                            </FormField>
                            <FormField
                                label="GPA"
                                id="gpa"
                                error={errors.gpa}
                                success={!errors.gpa && touchedFields.gpa}
                            >
                                <InputWithError
                                    id="gpa"
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    max="4"
                                    value={formData.gpa}
                                    onChange={(e) => handleFieldChange("gpa", e.target.value)}
                                    placeholder="3.50"
                                    error={errors.gpa}
                                />
                            </FormField>
                        </div>
                        <FormField
                            label="Special Skills & Abilities"
                            id="specialSkills"
                            error={errors.specialSkills}
                            success={!errors.specialSkills && touchedFields.specialSkills}
                        >
                            <TextareaWithError
                                id="specialSkills"
                                value={formData.specialSkills}
                                onChange={(e) => handleFieldChange("specialSkills", e.target.value)}
                                placeholder="Describe any special skills, talents, or abilities that would benefit your teaching"
                                rows={3}
                                error={errors.specialSkills}
                            />
                        </FormField>
                    </div>
                )

            case 4:
                return (
                    <div className="space-y-6">
                        <div className="flex items-center gap-2 mb-4">
                            <Award className="h-5 w-5 text-yellow-600" />
                            <h3 className="text-lg font-semibold">{currentStepName}</h3>
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="teachingLicense"
                                    checked={formData.teachingLicense}
                                    onCheckedChange={(checked) => handleFieldChange("teachingLicense", checked)}
                                />
                                <Label htmlFor="teachingLicense">Do you have a valid teaching license?</Label>
                            </div>

                            {formData.teachingLicense && (
                                <div className="ml-6 space-y-4 p-4 bg-yellow-50 rounded-lg">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <FormField
                                            label="License Number"
                                            id="licenseNumber"
                                            required
                                            error={errors.licenseNumber}
                                            success={
                                                !errors.licenseNumber && touchedFields.licenseNumber
                                            }
                                        >
                                            <InputWithError
                                                id="licenseNumber"
                                                value={formData.licenseNumber}
                                                onChange={(e) => handleFieldChange("licenseNumber", e.target.value)}
                                                placeholder="Enter license number"
                                                error={errors.licenseNumber}
                                            />
                                        </FormField>
                                        <FormField
                                            label="License State"
                                            id="licenseState"
                                            required
                                            error={errors.licenseState}
                                            success={!errors.licenseState && touchedFields.licenseState}
                                        >
                                            <InputWithError
                                                id="licenseState"
                                                value={formData.licenseState}
                                                onChange={(e) => handleFieldChange("licenseState", e.target.value)}
                                                placeholder="State where license was issued"
                                                error={errors.licenseState}
                                            />
                                        </FormField>
                                    </div>
                                    <FormField
                                        label="License Expiration Date"
                                        id="licenseExpirationDate"
                                        required
                                        error={errors.licenseExpirationDate}
                                        success={!errors.licenseExpirationDate && touchedFields.licenseExpirationDate}
                                    >
                                        <InputWithError
                                            id="licenseExpirationDate"
                                            type="date"
                                            value={formData.licenseExpirationDate}
                                            onChange={(e) => handleFieldChange("licenseExpirationDate", e.target.value)}
                                            error={errors.licenseExpirationDate}
                                        />
                                    </FormField>
                                </div>
                            )}
                        </div>

                        <Separator />

                        <div className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="yearsOfExperience">Years of Teaching Experience *</Label>
                                <SelectWithError
                                    placeholder="Select years of experience"
                                    value={formData.yearsOfExperience}
                                    onValueChange={(value) => handleFieldChange("yearsOfExperience", value)}
                                    error={errors.yearsOfExperience}
                                >
                                    <SelectItem value="0">No experience</SelectItem>
                                    <SelectItem value="1-2">1-2 years</SelectItem>
                                    <SelectItem value="3-5">3-5 years</SelectItem>
                                    <SelectItem value="6-10">6-10 years</SelectItem>
                                    <SelectItem value="11-15">11-15 years</SelectItem>
                                    <SelectItem value="16-20">16-20 years</SelectItem>
                                    <SelectItem value="20+">20+ years</SelectItem>
                                </SelectWithError>
                                {errors.yearsOfExperience && <p className="text-red-500 text-sm">{errors.yearsOfExperience}</p>}
                            </div>
                        </div>

                        <FormField
                            label="Previous Schools/Institutions"
                            id="previousSchools"
                            error={errors.previousSchools}
                            success={!errors.previousSchools && touchedFields.previousSchools}
                        >
                            <TextareaWithError
                                id="previousSchools"
                                value={formData.previousSchools}
                                onChange={(e) => handleFieldChange("previousSchools", e.target.value)}
                                placeholder="List previous schools where you have taught, including dates and positions"
                                rows={3}
                                error={errors.previousSchools}
                            />
                        </FormField>

                        <div className="space-y-4">
                            <div className="space-y-2">
                                <Label>Subjects You Can Teach *</Label>
                                <p className="text-sm text-gray-600">Select all subjects you are qualified to teach:</p>
                                <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                                    {subjects.map((subject) => (
                                        <div key={subject} className="flex items-center space-x-2">
                                            <Checkbox
                                                id={subject}
                                                checked={(formData.subjectsToTeach || []).includes(subject)}
                                                onCheckedChange={() => handleArrayToggle("subjectsToTeach", subject)}
                                            />
                                            <Label htmlFor={subject} className="text-sm">
                                                {subject}
                                            </Label>
                                        </div>
                                    ))}
                                </div>
                                {(formData.subjectsToTeach || []).length > 0 && (
                                    <div className="flex flex-wrap gap-1 mt-2">
                                        {(formData.subjectsToTeach || []).map((subject) => (
                                            <Badge key={subject} variant="secondary">
                                                {subject}
                                            </Badge>
                                        ))}
                                    </div>
                                )}
                                {errors.subjectsToTeach && <p className="text-red-500 text-sm">{errors.subjectsToTeach}</p>}
                            </div>
                        </div>

                        <div className="space-y-4">
                            <div className="space-y-2">
                                <Label>Grade Levels You Can Teach *</Label>
                                <p className="text-sm text-gray-600">Select all grade levels you are qualified to teach:</p>
                                <div className="grid grid-cols-3 md:grid-cols-5 gap-2">
                                    {gradeLevels.map((grade) => (
                                        <div key={grade} className="flex items-center space-x-2">
                                            <Checkbox
                                                id={grade}
                                                checked={(formData.gradeLevelsToTeach || []).includes(grade)}
                                                onCheckedChange={() => handleArrayToggle("gradeLevelsToTeach", grade)}
                                            />
                                            <Label htmlFor={grade} className="text-sm">
                                                {grade}
                                            </Label>
                                        </div>
                                    ))}
                                </div>
                                {(formData.gradeLevelsToTeach || []).length > 0 && (
                                    <div className="flex flex-wrap gap-1 mt-2">
                                        {(formData.gradeLevelsToTeach || []).map((grade) => (
                                            <Badge key={grade} variant="secondary">
                                                {grade}
                                            </Badge>
                                        ))}
                                    </div>
                                )}
                                {errors.gradeLevelsToTeach && <p className="text-red-500 text-sm">{errors.gradeLevelsToTeach}</p>}
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="preferredSchedule">Preferred Schedule</Label>
                            <SelectWithError
                                placeholder="Select preferred schedule"
                                value={formData.preferredSchedule}
                                onValueChange={(value) => handleFieldChange("preferredSchedule", value)}
                                error={errors.preferredSchedule}
                            >
                                <SelectItem value="full-time">Full-time</SelectItem>
                                <SelectItem value="part-time">Part-time</SelectItem>
                                <SelectItem value="substitute">Substitute</SelectItem>
                                <SelectItem value="flexible">Flexible</SelectItem>
                            </SelectWithError>
                        </div>
                    </div>
                )

            case 5:
                return (
                    <div className="space-y-6">
                        <div className="flex items-center gap-2 mb-4">
                            <Shield className="h-5 w-5 text-red-600" />
                            <h3 className="text-lg font-semibold">{currentStepName}</h3>
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="hasConvictions"
                                    checked={formData.hasConvictions}
                                    onCheckedChange={(checked) => handleFieldChange("hasConvictions", checked)}
                                />
                                <Label htmlFor="hasConvictions">
                                    Have you ever been convicted of a crime (excluding minor traffic violations)?
                                </Label>
                            </div>

                            {formData.hasConvictions && (
                                <div className="ml-6 space-y-2 p-4 bg-red-50 rounded-lg">
                                    <FormField
                                        label="Conviction Details"
                                        id="convictionDetails"
                                        required
                                        error={errors.convictionDetails}
                                        success={!errors.convictionDetails && touchedFields.convictionDetails}
                                    >
                                        <TextareaWithError
                                            id="convictionDetails"
                                            value={formData.convictionDetails}
                                            onChange={(e) => handleFieldChange("convictionDetails", e.target.value)}
                                            placeholder="Please provide details about the conviction(s)"
                                            rows={3}
                                            error={errors.convictionDetails}
                                        />
                                    </FormField>
                                </div>
                            )}
                        </div>

                        <div className="space-y-4">
                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="hasDisciplinaryActions"
                                    checked={formData.hasDisciplinaryActions}
                                    onCheckedChange={(checked) => handleFieldChange("hasDisciplinaryActions", checked)}
                                />
                                <Label htmlFor="hasDisciplinaryActions">
                                    Have you ever been subject to disciplinary action in any previous employment?
                                </Label>
                            </div>

                            {formData.hasDisciplinaryActions && (
                                <div className="ml-6 space-y-2 p-4 bg-orange-50 rounded-lg">
                                    <FormField
                                        label="Disciplinary Action Details"
                                        id="disciplinaryDetails"
                                        required
                                        error={errors.disciplinaryDetails}
                                        success={!errors.disciplinaryDetails && touchedFields.disciplinaryDetails}
                                    >
                                        <TextareaWithError
                                            id="disciplinaryDetails"
                                            value={formData.disciplinaryDetails}
                                            onChange={(e) => handleFieldChange("disciplinaryDetails", e.target.value)}
                                            placeholder="Please provide details about the disciplinary action(s)"
                                            rows={3}
                                            error={errors.disciplinaryDetails}
                                        />
                                    </FormField>
                                </div>
                            )}
                        </div>

                        <Separator />

                        <div className="space-y-6">
                            <h4 className="font-medium text-blue-600">Professional References</h4>

                            <div className="space-y-4 p-4 bg-blue-50 rounded-lg">
                                <h5 className="font-medium">Reference 1 (Required)</h5>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <FormField
                                        label="Name"
                                        id="reference1Name"
                                        required
                                        error={errors.reference1Name}
                                        success={
                                            !errors.reference1Name && touchedFields.reference1Name
                                        }
                                    >
                                        <InputWithError
                                            id="reference1Name"
                                            value={formData.reference1Name}
                                            onChange={(e) => handleFieldChange("reference1Name", e.target.value)}
                                            placeholder="Enter reference name"
                                            error={errors.reference1Name}
                                        />
                                    </FormField>
                                    <FormField
                                        label="Title/Position"
                                        id="reference1Title"
                                        required
                                        error={errors.reference1Title}
                                        success={
                                            !errors.reference1Title && touchedFields.reference1Title
                                        }
                                    >
                                        <InputWithError
                                            id="reference1Title"
                                            value={formData.reference1Title}
                                            onChange={(e) => handleFieldChange("reference1Title", e.target.value)}
                                            placeholder="e.g., Principal, Department Head"
                                            error={errors.reference1Title}
                                        />
                                    </FormField>
                                </div>
                                <FormField
                                    label="Organization"
                                    id="reference1Organization"
                                    required
                                    error={errors.reference1Organization}
                                    success={
                                        !errors.reference1Organization &&
                                        touchedFields.reference1Organization &&
                                        formData.reference1Organization.length > 0
                                    }
                                >
                                    <InputWithError
                                        id="reference1Organization"
                                        value={formData.reference1Organization}
                                        onChange={(e) => handleFieldChange("reference1Organization", e.target.value)}
                                        placeholder="School or organization name"
                                        error={errors.reference1Organization}
                                    />
                                </FormField>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <FormField
                                        label="Phone Number"
                                        id="reference1Phone"
                                        required
                                        error={errors.reference1Phone}
                                        success={
                                            !errors.reference1Phone && touchedFields.reference1Phone
                                        }
                                    >
                                        <InputWithError
                                            id="reference1Phone"
                                            value={formData.reference1Phone}
                                            onChange={(e) => handleFieldChange("reference1Phone", formatPhoneNumber(e.target.value))}
                                            placeholder="(123) 456-7890"
                                            error={errors.reference1Phone}
                                        />
                                    </FormField>
                                    <FormField
                                        label="Email"
                                        id="reference1Email"
                                        required
                                        error={errors.reference1Email}
                                        success={
                                            !errors.reference1Email && touchedFields.reference1Email
                                        }
                                    >
                                        <InputWithError
                                            id="reference1Email"
                                            type="email"
                                            value={formData.reference1Email}
                                            onChange={(e) => handleFieldChange("reference1Email", e.target.value)}
                                            placeholder="reference@example.com"
                                            error={errors.reference1Email}
                                        />
                                    </FormField>
                                </div>
                            </div>

                            <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
                                <h5 className="font-medium">Reference 2 (Optional)</h5>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <FormField
                                        label="Name"
                                        id="reference2Name"
                                        error={errors.reference2Name}
                                        success={!errors.reference2Name && touchedFields.reference2Name}
                                    >
                                        <InputWithError
                                            id="reference2Name"
                                            value={formData.reference2Name}
                                            onChange={(e) => handleFieldChange("reference2Name", e.target.value)}
                                            placeholder="Enter reference name"
                                            error={errors.reference2Name}
                                        />
                                    </FormField>
                                    <FormField
                                        label="Title/Position"
                                        id="reference2Title"
                                        error={errors.reference2Title}
                                        success={!errors.reference2Title && touchedFields.reference2Title}
                                    >
                                        <InputWithError
                                            id="reference2Title"
                                            value={formData.reference2Title}
                                            onChange={(e) => handleFieldChange("reference2Title", e.target.value)}
                                            placeholder="e.g., Principal, Department Head"
                                            error={errors.reference2Title}
                                        />
                                    </FormField>
                                </div>
                                <FormField
                                    label="Organization"
                                    id="reference2Organization"
                                    error={errors.reference2Organization}
                                    success={!errors.reference2Organization && touchedFields.reference2Organization}
                                >
                                    <InputWithError
                                        id="reference2Organization"
                                        value={formData.reference2Organization}
                                        onChange={(e) => handleFieldChange("reference2Organization", e.target.value)}
                                        placeholder="School or organization name"
                                        error={errors.reference2Organization}
                                    />
                                </FormField>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <FormField
                                        label="Phone Number"
                                        id="reference2Phone"
                                        error={errors.reference2Phone}
                                        success={
                                            !errors.reference2Phone && touchedFields.reference2Phone
                                        }
                                    >
                                        <InputWithError
                                            id="reference2Phone"
                                            value={formData.reference2Phone}
                                            onChange={(e) => handleFieldChange("reference2Phone", formatPhoneNumber(e.target.value))}
                                            placeholder="(123) 456-7890"
                                            error={errors.reference2Phone}
                                        />
                                    </FormField>
                                    <FormField
                                        label="Email"
                                        id="reference2Email"
                                        error={errors.reference2Email}
                                        success={
                                            !errors.reference2Email && touchedFields.reference2Email
                                        }
                                    >
                                        <InputWithError
                                            id="reference2Email"
                                            type="email"
                                            value={formData.reference2Email}
                                            onChange={(e) => handleFieldChange("reference2Email", e.target.value)}
                                            placeholder="reference@example.com"
                                            error={errors.reference2Email}
                                        />
                                    </FormField>
                                </div>
                            </div>

                            <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
                                <h5 className="font-medium">Reference 3 (Optional)</h5>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <FormField
                                        label="Name"
                                        id="reference3Name"
                                        error={errors.reference3Name}
                                        success={
                                            !errors.reference3Name && touchedFields.reference3Name
                                        }
                                    >
                                        <InputWithError
                                            id="reference3Name"
                                            value={formData.reference3Name}
                                            onChange={(e) => handleFieldChange("reference3Name", e.target.value)}
                                            placeholder="Enter reference name"
                                            error={errors.reference3Name}
                                        />
                                    </FormField>
                                    <FormField
                                        label="Title/Position"
                                        id="reference3Title"
                                        error={errors.reference3Title}
                                        success={
                                            !errors.reference3Title && touchedFields.reference3Title
                                        }
                                    >
                                        <InputWithError
                                            id="reference3Title"
                                            value={formData.reference3Title}
                                            onChange={(e) => handleFieldChange("reference3Title", e.target.value)}
                                            placeholder="e.g., Principal, Department Head"
                                            error={errors.reference3Title}
                                        />
                                    </FormField>
                                </div>
                                <FormField
                                    label="Organization"
                                    id="reference3Organization"
                                    error={errors.reference3Organization}
                                    success={!errors.reference3Organization && touchedFields.reference3Organization}
                                >
                                    <InputWithError
                                        id="reference3Organization"
                                        value={formData.reference3Organization}
                                        onChange={(e) => handleFieldChange("reference3Organization", e.target.value)}
                                        placeholder="School or organization name"
                                        error={errors.reference3Organization}
                                    />
                                </FormField>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <FormField
                                        label="Phone Number"
                                        id="reference3Phone"
                                        error={errors.reference3Phone}
                                        success={
                                            !errors.reference3Phone && touchedFields.reference3Phone
                                        }
                                    >
                                        <InputWithError
                                            id="reference3Phone"
                                            value={formData.reference3Phone}
                                            onChange={(e) => handleFieldChange("reference3Phone", formatPhoneNumber(e.target.value))}
                                            placeholder="(123) 456-7890"
                                            error={errors.reference3Phone}
                                        />
                                    </FormField>
                                    <FormField
                                        label="Email"
                                        id="reference3Email"
                                        error={errors.reference3Email}
                                        success={!errors.reference3Email && touchedFields.reference3Email}
                                    >
                                        <InputWithError
                                            id="reference3Email"
                                            type="email"
                                            value={formData.reference3Email}
                                            onChange={(e) => handleFieldChange("reference3Email", e.target.value)}
                                            placeholder="reference@example.com"
                                            error={errors.reference3Email}
                                        />
                                    </FormField>
                                </div>
                            </div>
                        </div>
                    </div>
                )

            case 6:
                return (
                    <div className="space-y-6">
                        <div className="flex items-center gap-2 mb-4">
                            <FileText className="h-5 w-5 text-green-600" />
                            <h3 className="text-lg font-semibold">{currentStepName}</h3>
                        </div>

                        <div className="space-y-6">
                            <h4 className="font-medium text-blue-600">Required Documents</h4>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="resume">Resume/CV *</Label>
                                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                                        <Upload className="mx-auto h-8 w-8 text-gray-400" />
                                        <div className="mt-2">
                                            <Label htmlFor="resume" className="cursor-pointer">
                                                <span className="text-blue-600 hover:text-blue-500">Upload Resume</span>
                                                <Input
                                                    id="resume"
                                                    type="file"
                                                    accept=".pdf,.doc,.docx"
                                                    className="hidden"
                                                    onChange={(e) => updateFormData("resume", e.target.files?.[0] || undefined)}
                                                />
                                            </Label>
                                        </div>
                                        <p className="text-xs text-gray-500">PDF, DOC, DOCX up to 5MB</p>
                                    </div>
                                    {formData.resume && <p className="text-sm text-green-600">✓ {formData.resume.name}</p>}
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="coverLetter">Cover Letter</Label>
                                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                                        <Upload className="mx-auto h-8 w-8 text-gray-400" />
                                        <div className="mt-2">
                                            <Label htmlFor="coverLetter" className="cursor-pointer">
                                                <span className="text-blue-600 hover:text-blue-500">Upload Cover Letter</span>
                                                <Input
                                                    id="coverLetter"
                                                    type="file"
                                                    accept=".pdf,.doc,.docx"
                                                    className="hidden"
                                                    onChange={(e) => updateFormData("coverLetter", e.target.files?.[0] || undefined)}
                                                />
                                            </Label>
                                        </div>
                                        <p className="text-xs text-gray-500">PDF, DOC, DOCX up to 5MB</p>
                                    </div>
                                    {formData.coverLetter && <p className="text-sm text-green-600">✓ {formData.coverLetter.name}</p>}
                                </div>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="transcripts">Official Transcripts</Label>
                                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                                        <Upload className="mx-auto h-8 w-8 text-gray-400" />
                                        <div className="mt-2">
                                            <Label htmlFor="transcripts" className="cursor-pointer">
                                                <span className="text-blue-600 hover:text-blue-500">Upload Transcripts</span>
                                                <Input
                                                    id="transcripts"
                                                    type="file"
                                                    accept=".pdf"
                                                    className="hidden"
                                                    onChange={(e) => updateFormData("transcripts", e.target.files?.[0] || undefined)}
                                                />
                                            </Label>
                                        </div>
                                        <p className="text-xs text-gray-500">PDF up to 5MB</p>
                                    </div>
                                    {formData.transcripts && <p className="text-sm text-green-600">✓ {formData.transcripts.name}</p>}
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="teachingCertificate">Teaching Certificate/License</Label>
                                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                                        <Upload className="mx-auto h-8 w-8 text-gray-400" />
                                        <div className="mt-2">
                                            <Label htmlFor="teachingCertificate" className="cursor-pointer">
                                                <span className="text-blue-600 hover:text-blue-500">Upload Certificate</span>
                                                <Input
                                                    id="teachingCertificate"
                                                    type="file"
                                                    accept=".pdf,.jpg,.png"
                                                    className="hidden"
                                                    onChange={(e) => updateFormData("teachingCertificate", e.target.files?.[0] || undefined)}
                                                />
                                            </Label>
                                        </div>
                                        <p className="text-xs text-gray-500">PDF, JPG, PNG up to 5MB</p>
                                    </div>
                                    {formData.teachingCertificate && (
                                        <p className="text-sm text-green-600">✓ {formData.teachingCertificate.name}</p>
                                    )}
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="backgroundCheck">Background Check Authorization</Label>
                                <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
                                    <Upload className="mx-auto h-8 w-8 text-gray-400" />
                                    <div className="mt-2">
                                        <Label htmlFor="backgroundCheck" className="cursor-pointer">
                                            <span className="text-blue-600 hover:text-blue-500">Upload Background Check Form</span>
                                            <Input
                                                id="backgroundCheck"
                                                type="file"
                                                accept=".pdf"
                                                className="hidden"
                                                onChange={(e) => updateFormData("backgroundCheck", e.target.files?.[0] || undefined)}
                                            />
                                        </Label>
                                    </div>
                                    <p className="text-xs text-gray-500">PDF up to 5MB</p>
                                </div>
                                {formData.backgroundCheck && (
                                    <p className="text-sm text-green-600">✓ {formData.backgroundCheck.name}</p>
                                )}
                            </div>
                        </div>

                        <Separator />

                        <div className="space-y-6">
                            <h4 className="font-medium text-purple-600">Additional Information</h4>

                            <FormField
                                label="Teaching Philosophy"
                                id="teachingPhilosophy"
                                description="Describe your teaching philosophy and approach to education (max 1000 characters)"
                                error={errors.teachingPhilosophy}
                                success={!errors.teachingPhilosophy && touchedFields.teachingPhilosophy}
                            >
                                <TextareaWithError
                                    id="teachingPhilosophy"
                                    value={formData.teachingPhilosophy}
                                    onChange={(e) => handleFieldChange("teachingPhilosophy", e.target.value)}
                                    placeholder="Describe your teaching philosophy, methods, and what you believe makes effective education..."
                                    rows={4}
                                    maxLength={1000}
                                    error={errors.teachingPhilosophy}
                                />
                                <p className="text-xs text-gray-500 mt-1">{formData.teachingPhilosophy ? formData.teachingPhilosophy.length : 0}/1000 characters</p>
                            </FormField>

                            <FormField
                                label="Why do you want to teach?"
                                id="whyTeaching"
                                description="What motivates you to pursue a career in teaching? (max 500 characters)"
                                error={errors.whyTeaching}
                                success={!errors.whyTeaching && touchedFields.whyTeaching}
                            >
                                <TextareaWithError
                                    id="whyTeaching"
                                    value={formData.whyTeaching}
                                    onChange={(e) => handleFieldChange("whyTeaching", e.target.value)}
                                    placeholder="Share your motivation and passion for teaching..."
                                    rows={3}
                                    maxLength={500}
                                    error={errors.whyTeaching}
                                />
                                <p className="text-xs text-gray-500 mt-1">{formData.whyTeaching ? formData.whyTeaching.length : 0}/500 characters</p>
                            </FormField>

                            <FormField
                                label="Additional Comments"
                                id="additionalComments"
                                description="Any additional information you'd like to share (max 500 characters)"
                                error={errors.additionalComments}
                                success={!errors.additionalComments && touchedFields.additionalComments}
                            >
                                <TextareaWithError
                                    id="additionalComments"
                                    value={formData.additionalComments}
                                    onChange={(e) => handleFieldChange("additionalComments", e.target.value)}
                                    placeholder="Any other information that would support your application..."
                                    rows={3}
                                    maxLength={500}
                                    error={errors.additionalComments}
                                />
                                <p className="text-xs text-gray-500 mt-1">{formData.additionalComments ? formData.additionalComments.length : 0}/500 characters</p>
                            </FormField>
                        </div>

                        <Separator />

                        <div className="space-y-4">
                            <h4 className="font-medium text-red-600">Terms and Agreements</h4>

                            <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
                                <div className="flex items-start space-x-2">
                                    <Checkbox
                                        id="agreeToTerms"
                                        checked={formData.agreeToTerms}
                                        onCheckedChange={(checked) => handleFieldChange("agreeToTerms", checked)}
                                    />
                                    <Label htmlFor="agreeToTerms" className="text-sm leading-relaxed">
                                        I agree to the terms and conditions of employment and understand that all information provided is
                                        accurate and complete. I understand that any false information may result in rejection of my
                                        application or termination of employment.
                                    </Label>
                                </div>
                                {errors.agreeToTerms && <p className="text-red-500 text-sm">{errors.agreeToTerms}</p>}

                                <div className="flex items-start space-x-2">
                                    <Checkbox
                                        id="agreeToBackgroundCheck"
                                        checked={formData.agreeToBackgroundCheck}
                                        onCheckedChange={(checked) => handleFieldChange("agreeToBackgroundCheck", checked)}
                                    />
                                    <Label htmlFor="agreeToBackgroundCheck" className="text-sm leading-relaxed">
                                        I authorize the school district to conduct a comprehensive background check, including criminal
                                        history, employment verification, and reference checks. I understand this is required for all
                                        teaching positions.
                                    </Label>
                                </div>
                                {errors.agreeToBackgroundCheck && (
                                    <p className="text-red-500 text-sm">{errors.agreeToBackgroundCheck}</p>
                                )}
                            </div>
                        </div>

                        <div className="bg-blue-50 p-4 rounded-lg">
                            <p className="text-sm text-blue-800">
                                <strong>Note:</strong> Please review all information carefully before submitting. After submission, you
                                will receive a confirmation email and our HR team will contact you within 5-7 business days regarding
                                the next steps in the hiring process.
                            </p>
                        </div>
                    </div>
                )

            default:
                return null
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 p-4">
            <div className="max-w-5xl mx-auto">
                <Card className="shadow-xl">
                    <CardHeader className="text-center">
                        <CardTitle className="text-3xl font-bold text-gray-800">Teacher Registration Form</CardTitle>
                        <CardDescription className="text-lg">
                            Complete all steps to apply for a teaching position at our school
                        </CardDescription>
                        <div className="mt-4">
                            <Progress value={progress} className="w-full" />
                            <p className="text-sm text-gray-600 mt-2">
                                Step {currentStep} of {totalSteps}
                            </p>
                        </div>
                        <div className="mt-2 flex justify-center">
                            <AutoSaveIndicator lastSaved={lastSaved} isOnline={isOnline} />
                        </div>
                    </CardHeader>

                    <CardContent className="p-8">
                        <div className="min-h-[600px]">{renderStep()}</div>

                        <div className="flex justify-between mt-8 pt-6 border-t">
                            <Button variant="outline" onClick={prevStep} disabled={currentStep === 1} className="px-8">
                                Previous
                            </Button>

                            {currentStep < totalSteps ? (
                                <Button onClick={nextStep} className="px-8">
                                    Next Step
                                </Button>
                            ) : (
                                <Button onClick={handleFinalSubmit} className="px-8 bg-green-600 hover:bg-green-700">
                                    Submit Application
                                </Button>
                            )}
                        </div>
                    </CardContent>
                </Card>

                <FormRestorationDialog
                    isOpen={showRestorationDialog}
                    onRestore={handleRestoreForm}
                    onStartFresh={handleStartFresh}
                    savedStep={currentStep}
                    savedStepName={currentStepName}
                    lastSaved={lastSaved}
                />
            </div>
        </div>
    )
}
