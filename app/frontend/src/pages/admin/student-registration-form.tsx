"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { SelectItem } from "@/components/ui/select";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  studentRegistrationSchema,
  step1Schema,
  step2Schema,
  step3Schema,
  step4Schema,
  step5Schema,
  step6Schema,
  type StudentRegistrationFormData,
} from "@/lib/form-validation";
import {
  FormField,
  InputWithError,
  TextareaWithError,
  SelectWithError,
} from "@/components/form-field-with-error";
import {
  Upload,
  User,
  GraduationCap,
  Heart,
  MapPin,
  Users,
  FileText,
} from "lucide-react";
import { z } from "zod";
import { useFormPersistence } from "@/hooks/use-form-persistence";
import FormRestorationDialog from "@/components/form-restoration-dialog";
import AutoSaveIndicator from "@/components/auto-save-indicator";
import { Checkbox } from "@/components/ui/checkbox";

// undefined fields are optional
const initialFormData: StudentRegistrationFormData = {
  firstName: "",
  lastName: "",
  fatherName: "",
  grandFatherName: undefined as any,
  dateOfBirth: "",
  gender: undefined as any,
  nationality: "",
  bloodType: undefined,
  studentPhoto: undefined,
  grade: undefined as any,
  academicYear: undefined as any,
  isTransfer: false,
  previousSchool: "",
  previousGrades: "",
  address: "",
  city: "",
  state: "",
  postalCode: "",
  fatherPhone: "",
  motherPhone: "",
  parentEmail: "",
  guardianName: "",
  guardianPhone: "",
  guardianRelation: undefined as any,
  emergencyContactName: undefined,
  emergencyContactPhone: undefined,
  hasMedicalCondition: false,
  medicalDetails: "",
  hasDisability: false,
  disabilityDetails: "",
  requiresAccommodation: false,
  accommodationDetails: "",
  allergies: "",
  languageAtHome: undefined,
  transportation: undefined,
  lunchProgram: false,
  extracurriculars: [],
  siblingInSchool: false,
  siblingDetails: "",
};

const grades = [
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
];
const bloodTypes = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];
const extracurricularOptions = [
  "Sports",
  "Music",
  "Art",
  "Drama",
  "Science Club",
  "Math Club",
  "Chess",
  "Debate",
  "Photography",
  "Dance",
];

const stepNames = {
  1: "Personal Information",
  2: "Academic Information",
  3: "Address & Contact",
  4: "Guardian & Emergency Contact",
  5: "Medical Information",
  6: "Additional Information & Review",
};

export default function StudentRegistrationForm() {
  const [currentStep, setCurrentStep] = useState(1);
  const [currentStepName, setCurrentStepName] = useState(
    stepNames[currentStep as keyof typeof stepNames] || "Unknown Step",
  );
  const [formData, setFormData] =
    useState<StudentRegistrationFormData>(initialFormData);
  const [selectedExtracurriculars, setSelectedExtracurriculars] = useState<
    string[]
  >([]);

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touchedFields, setTouchedFields] = useState<Record<string, boolean>>(
    {},
  );

  const [showRestorationDialog, setShowRestorationDialog] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date>();
  const [isOnline, setIsOnline] = useState(true);
  const { saveFormData, loadFormData, clearFormData, hasSavedData } =
    useFormPersistence();

  // Handle form restoration on component mount
  useEffect(() => {
    if (hasSavedData()) {
      const savedData = loadFormData();
      if (savedData) {
        setCurrentStep(savedData.step);
        setCurrentStepName(
          stepNames[savedData.step as keyof typeof stepNames] || "Unknown Step",
        );
      }
      setShowRestorationDialog(true);
    }
  }, [hasSavedData]);

  // Monitor online status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  // Auto-save form data whenever it changes
  useEffect(() => {
    if (formData.firstName || formData.lastName || formData.fatherName) {
      // Only save if form has some data
      saveFormData(formData, currentStep);
      setLastSaved(new Date());
    }
  }, [formData, currentStep, saveFormData]);

  const totalSteps = 6;
  const progress = (currentStep / totalSteps) * 100;

  const updateFormData = (
    field: keyof StudentRegistrationFormData,
    value: any,
  ) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

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

  const handleExtracurricularToggle = (activity: string) => {
    const updated = selectedExtracurriculars.includes(activity)
      ? selectedExtracurriculars.filter((item) => item !== activity)
      : [...selectedExtracurriculars, activity];
    setSelectedExtracurriculars(updated);
    updateFormData("extracurriculars", updated);
  };

  const validateStep = (stepNumber: number): boolean => {
    let schema: z.ZodSchema;
    let dataToValidate: any;

    switch (stepNumber) {
      case 1:
        schema = step1Schema;
        dataToValidate = {
          firstName: formData.firstName,
          lastName: formData.lastName,
          fatherName: formData.fatherName,
          grandFatherName: formData.grandFatherName,
          dateOfBirth: formData.dateOfBirth,
          gender: formData.gender,
          nationality: formData.nationality,
          bloodType: formData.bloodType,
          languageAtHome: formData.languageAtHome,
          studentPhoto: formData.studentPhoto,
        };
        break;
      case 2:
        schema = step2Schema;
        dataToValidate = {
          grade: formData.grade,
          academicYear: formData.academicYear,
          isTransfer: formData.isTransfer,
          previousSchool: formData.previousSchool,
          previousGrades: formData.previousGrades,
          transportation: formData.transportation,
          lunchProgram: formData.lunchProgram,
        };
        break;
      case 3:
        schema = step3Schema;
        dataToValidate = {
          address: formData.address,
          city: formData.city,
          state: formData.state,
          postalCode: formData.postalCode,
          fatherPhone: formData.fatherPhone,
          motherPhone: formData.motherPhone,
          parentEmail: formData.parentEmail,
        };
        break;
      case 4:
        schema = step4Schema;
        dataToValidate = {
          guardianName: formData.guardianName,
          guardianPhone: formData.guardianPhone,
          guardianRelation: formData.guardianRelation,
          emergencyContactName: formData.emergencyContactName,
          emergencyContactPhone: formData.emergencyContactPhone,
          siblingInSchool: formData.siblingInSchool,
          siblingDetails: formData.siblingDetails,
        };
        break;
      case 5:
        schema = step5Schema;
        dataToValidate = {
          hasMedicalCondition: formData.hasMedicalCondition,
          medicalDetails: formData.medicalDetails,
          hasDisability: formData.hasDisability,
          disabilityDetails: formData.disabilityDetails,
          requiresAccommodation: formData.requiresAccommodation,
          accommodationDetails: formData.accommodationDetails,
          allergies: formData.allergies,
        };
        break;
      case 6:
        schema = step6Schema;
        dataToValidate = {
          extracurriculars: formData.extracurriculars,
        };
        break;
      default:
        return true;
    }

    try {
      schema.parse(dataToValidate);
      // Clear errors for this step
      const stepErrors = { ...errors };
      Object.keys(dataToValidate).forEach((key) => {
        delete stepErrors[key];
      });
      setErrors(stepErrors);
      return true;
    } catch (error) {
      if (error instanceof z.ZodError) {
        const newErrors: Record<string, string> = {};
        error.errors.forEach((err) => {
          if (err.path.length > 0) {
            newErrors[err.path[0] as string] = err.message;
          }
        });
        setErrors((prev) => ({ ...prev, ...newErrors }));
      }
      return false;
    }
  };

  const validateField = (
    field: keyof StudentRegistrationFormData,
    value: any,
  ) => {
    try {
      // Unwrap ZodEffects to access the underlying ZodObject with shape
      let schema: any = studentRegistrationSchema;
      while (schema && typeof schema.innerType === "function") {
        schema = schema.innerType();
      }
      const fieldSchema = schema.shape[field];
      console.log("fieldSchema: ", fieldSchema);
      if (fieldSchema) {
        fieldSchema.parse(value);
        setErrors((prev) => {
          const newErrors = { ...prev };
          delete newErrors[field];
          return newErrors;
        });
      }
    } catch (error) {
      if (error instanceof z.ZodError) {
        setErrors((prev) => ({
          ...prev,
          [field]: error.errors[0]?.message || "Invalid input",
        }));
      }
    }
  };

  const handleFieldChange = (
    field: keyof StudentRegistrationFormData,
    value: any,
  ) => {
    value = value === "" ? undefined : value; // Handle empty strings
    updateFormData(field, value);
    setTouchedFields((prev) => ({ ...prev, [field]: true }));

    // Validate field after a short delay to avoid validating while typing
    setTimeout(() => {
      validateField(field, value);
    }, 300);
  };

  const nextStep = () => {
    if (validateStep(currentStep) && currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
      setCurrentStepName(
        stepNames[(currentStep + 1) as keyof typeof stepNames] ||
          "Unknown Step",
      );
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
      setCurrentStepName(
        stepNames[(currentStep - 1) as keyof typeof stepNames] ||
          "Unknown Step",
      );
    }
  };

  const handleRestoreForm = () => {
    const savedData = loadFormData();
    if (savedData) {
      setFormData((prev) => ({ ...prev, ...savedData.data }));
      setCurrentStep(savedData.step);
      setCurrentStepName(
        stepNames[savedData.step as keyof typeof stepNames] || "Unknown Step",
      );
      if (savedData.data.extracurriculars) {
        setSelectedExtracurriculars(savedData.data.extracurriculars);
      }
    }
    setShowRestorationDialog(false);
  };

  const handleStartFresh = () => {
    clearFormData();
    setFormData(initialFormData);
    setCurrentStep(1);
    setShowRestorationDialog(false);
  };

  const handleSubmit = () => {
    try {
      const validatedData = studentRegistrationSchema.parse(formData);
      console.log("Form submitted:", validatedData);

      // Clear saved data after successful submission
      clearFormData();

      alert("Registration submitted successfully!");
    } catch (error) {
      if (error instanceof z.ZodError) {
        const newErrors: Record<string, string> = {};
        error.errors.forEach((err) => {
          if (err.path.length > 0) {
            newErrors[err.path[0] as string] = err.message;
          }
        });
        setErrors(newErrors);
        alert("Please fix the errors before submitting.");
      }
    }
  };

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
                  onChange={(e) =>
                    handleFieldChange("firstName", e.target.value)
                  }
                  placeholder="Enter first name"
                  error={errors.firstName}
                />
              </FormField>
              <FormField
                label="Last Name"
                id="lastName"
                required
                error={errors.lastName}
                success={!errors.lastName && touchedFields.lastName}
              >
                <InputWithError
                  id="lastName"
                  value={formData.lastName}
                  onChange={(e) =>
                    handleFieldChange("lastName", e.target.value)
                  }
                  placeholder="Enter last name"
                  error={errors.lastName}
                />
              </FormField>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                label="Father's Name"
                id="fatherName"
                required
                error={errors.fatherName}
                success={!errors.fatherName && touchedFields.fatherName}
              >
                <InputWithError
                  id="fatherName"
                  value={formData.fatherName}
                  onChange={(e) =>
                    handleFieldChange("fatherName", e.target.value)
                  }
                  placeholder="Enter father's name"
                  error={errors.fatherName}
                />
              </FormField>
              <FormField
                label="Grandfather's Name"
                id="grandFatherName"
                required={false}
                error={errors.grandFatherName}
                success={
                  !errors.grandFatherName && touchedFields.grandFatherName
                }
              >
                <InputWithError
                  id="grandFatherName"
                  value={formData.grandFatherName}
                  onChange={(e) =>
                    handleFieldChange("grandFatherName", e.target.value)
                  }
                  placeholder="Enter grandfather's name"
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
                  onChange={(e) =>
                    handleFieldChange("dateOfBirth", e.target.value)
                  }
                  error={errors.dateOfBirth}
                />
              </FormField>
              <div className="space-y-2 w-[200px]">
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
                {errors.gender && (
                  <p className="text-red-500 text-sm">{errors.gender}</p>
                )}
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
                  onChange={(e) =>
                    handleFieldChange("nationality", e.target.value)
                  }
                  placeholder="Enter nationality"
                  error={errors.nationality}
                />
              </FormField>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="bloodType">Blood Type</Label>
                <SelectWithError
                  placeholder="Select blood type"
                  value={formData.bloodType}
                  onValueChange={(value) =>
                    handleFieldChange("bloodType", value)
                  }
                  error={errors.bloodType}
                >
                  {bloodTypes.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectWithError>
                {errors.bloodType && (
                  <p className="text-red-500 text-sm">{errors.bloodType}</p>
                )}
              </div>
              <FormField
                label="Primary Language at Home"
                id="languageAtHome"
                required={false}
                error={errors.languageAtHome}
                success={!errors.languageAtHome && touchedFields.languageAtHome}
              >
                <InputWithError
                  id="languageAtHome"
                  value={formData.languageAtHome}
                  onChange={(e) =>
                    handleFieldChange("languageAtHome", e.target.value)
                  }
                  placeholder="e.g., English, Spanish, etc."
                  error={errors.languageAtHome}
                />
              </FormField>
            </div>

            <div className="space-y-2">
              <Label htmlFor="studentPhoto">Student Photo</Label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <div className="mt-2">
                  <Label htmlFor="studentPhoto" className="cursor-pointer">
                    <span className="text-blue-600 hover:text-blue-500">
                      Upload a photo
                    </span>
                    <Input
                      id="studentPhoto"
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={(e) =>
                        updateFormData(
                          "studentPhoto",
                          e.target.files?.[0] || null,
                        )
                      }
                    />
                  </Label>
                </div>
                <p className="text-xs text-gray-500">PNG, JPG up to 2MB</p>
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <GraduationCap className="h-5 w-5 text-green-600" />
              <h3 className="text-lg font-semibold">{currentStepName}</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="grade">Grade Level *</Label>
                <SelectWithError
                  placeholder="Select grade"
                  value={formData.grade}
                  onValueChange={(value) => handleFieldChange("grade", value)}
                  error={errors.grade}
                >
                  {grades.map((grade) => (
                    <SelectItem key={grade} value={grade}>
                      {grade}
                    </SelectItem>
                  ))}
                </SelectWithError>
                {errors.grade && (
                  <p className="text-red-500 text-sm">{errors.grade}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label htmlFor="academicYear">Academic Year *</Label>
                <SelectWithError
                  placeholder="Select academic year"
                  value={formData.academicYear}
                  onValueChange={(value) =>
                    handleFieldChange("academicYear", value)
                  }
                  error={errors.academicYear}
                >
                  <SelectItem value="2024-2025">2024-2025</SelectItem>
                  <SelectItem value="2025-2026">2025-2026</SelectItem>
                  <SelectItem value="2026-2027">2026-2027</SelectItem>
                </SelectWithError>
                {errors.academicYear && (
                  <p className="text-red-500 text-sm">{errors.academicYear}</p>
                )}
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="isTransfer"
                  checked={formData.isTransfer}
                  onCheckedChange={(checked) =>
                    handleFieldChange("isTransfer", checked)
                  }
                />
                <Label htmlFor="isTransfer">
                  Is the student transferring from another school?
                </Label>
              </div>

              {formData.isTransfer && (
                <div className="ml-6 space-y-4 p-4 bg-gray-50 rounded-lg">
                  <FormField
                    label="Previous School Name"
                    id="previousSchool"
                    required
                    error={errors.previousSchool}
                    success={
                      !errors.previousSchool && touchedFields.previousSchool
                    }
                  >
                    <InputWithError
                      id="previousSchool"
                      value={formData.previousSchool}
                      onChange={(e) =>
                        handleFieldChange("previousSchool", e.target.value)
                      }
                      placeholder="Enter previous school name"
                      error={errors.previousSchool}
                    />
                  </FormField>
                  <FormField
                    label="Previous Academic Performance"
                    id="previousGrades"
                    error={errors.previousGrades}
                    success={
                      !errors.previousGrades && touchedFields.previousGrades
                    }
                  >
                    <TextareaWithError
                      id="previousGrades"
                      value={formData.previousGrades}
                      onChange={(e) =>
                        handleFieldChange("previousGrades", e.target.value)
                      }
                      placeholder="Brief description of academic performance at previous school"
                      rows={3}
                      error={errors.previousGrades}
                    />
                  </FormField>
                </div>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="transportation">Transportation Method</Label>
              <SelectWithError
                placeholder="How will the student get to school?"
                value={formData.transportation}
                onValueChange={(value) =>
                  handleFieldChange("transportation", value)
                }
                error={errors.transportation}
              >
                <SelectItem value="school-bus">School Bus</SelectItem>
                <SelectItem value="parent-drop">Parent Drop-off</SelectItem>
                <SelectItem value="walk">Walking</SelectItem>
                <SelectItem value="bicycle">Bicycle</SelectItem>
                <SelectItem value="other">Other</SelectItem>
              </SelectWithError>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="lunchProgram"
                checked={formData.lunchProgram}
                onCheckedChange={(checked) =>
                  handleFieldChange("lunchProgram", checked)
                }
              />
              <Label htmlFor="lunchProgram">
                Enroll in school lunch program
              </Label>
            </div>
          </div>
        );

      case 3:
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

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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
                  onChange={(e) =>
                    handleFieldChange("postalCode", e.target.value)
                  }
                  placeholder="Enter postal code"
                  error={errors.postalCode}
                />
              </FormField>
            </div>

            <Separator />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                label="Father's Phone Number"
                id="fatherPhone"
                required
                error={errors.fatherPhone}
                success={!errors.fatherPhone && touchedFields.fatherPhone}
              >
                <InputWithError
                  id="fatherPhone"
                  value={formData.fatherPhone}
                  onChange={(e) =>
                    handleFieldChange(
                      "fatherPhone",
                      formatPhoneNumber(e.target.value),
                    )
                  }
                  placeholder="+251/7xx-xxx-xxx"
                  error={errors.fatherPhone}
                />
              </FormField>
              <FormField
                label="Mother's Phone Number"
                id="motherPhone"
                required
                error={errors.motherPhone}
                success={!errors.motherPhone && touchedFields.motherPhone}
              >
                <InputWithError
                  id="motherPhone"
                  value={formData.motherPhone}
                  onChange={(e) =>
                    handleFieldChange(
                      "motherPhone",
                      formatPhoneNumber(e.target.value),
                    )
                  }
                  placeholder="+251/7xx-xxx-xxx"
                  error={errors.motherPhone}
                />
              </FormField>
            </div>

            <FormField
              label="Parent/Guardian Email"
              id="parentEmail"
              required
              error={errors.parentEmail}
              success={!errors.parentEmail && touchedFields.parentEmail}
            >
              <InputWithError
                id="parentEmail"
                type="email"
                value={formData.parentEmail}
                onChange={(e) =>
                  handleFieldChange("parentEmail", e.target.value)
                }
                placeholder="parent@example.com"
                error={errors.parentEmail}
              />
            </FormField>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <Users className="h-5 w-5 text-orange-600" />
              <h3 className="text-lg font-semibold">{currentStepName}</h3>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                label="Guardian Name"
                id="guardianName"
                required
                error={errors.guardianName}
                success={!errors.guardianName && touchedFields.guardianName}
              >
                <InputWithError
                  id="guardianName"
                  value={formData.guardianName}
                  onChange={(e) =>
                    handleFieldChange("guardianName", e.target.value)
                  }
                  placeholder="Enter guardian name"
                  error={errors.guardianName}
                />
              </FormField>
              <div className="space-y-2">
                <Label htmlFor="guardianRelation" aria-required>
                  Relationship to Student
                </Label>
                <SelectWithError
                  placeholder="Select relationship"
                  value={formData.guardianRelation}
                  onValueChange={(value) =>
                    handleFieldChange("guardianRelation", value)
                  }
                  error={errors.guardianRelation}
                >
                  <SelectItem value="parent">Parent</SelectItem>
                  <SelectItem value="grandparent">Grandparent</SelectItem>
                  <SelectItem value="aunt-uncle">Aunt/Uncle</SelectItem>
                  <SelectItem value="sibling">Sibling</SelectItem>
                  <SelectItem value="family-friend">Family Friend</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectWithError>
                {errors.guardianRelation && (
                  <p className="text-red-500 text-sm">
                    {errors.guardianRelation}
                  </p>
                )}
              </div>
            </div>

            <FormField
              label="Guardian Phone Number"
              id="guardianPhone"
              error={errors.guardianPhone}
              success={!errors.guardianPhone && touchedFields.guardianPhone}
            >
              <InputWithError
                id="guardianPhone"
                value={formData.guardianPhone}
                onChange={(e) =>
                  handleFieldChange(
                    "guardianPhone",
                    formatPhoneNumber(e.target.value),
                  )
                }
                placeholder="+251 9/7xx-xxx-xxx"
                error={errors.guardianPhone}
              />
            </FormField>

            <Separator />

            <div className="space-y-4">
              <h4 className="font-medium text-red-600">
                Emergency Contact (if different from above)
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  label="Emergency Contact Name"
                  id="emergencyContactName"
                  required={false}
                  error={errors.emergencyContactName}
                  success={
                    !errors.emergencyContactName &&
                    touchedFields.emergencyContactName
                  }
                >
                  <InputWithError
                    id="emergencyContactName"
                    placeholder="Enter emergency contact name"
                    value={formData.emergencyContactName}
                    onChange={(e) =>
                      handleFieldChange("emergencyContactName", e.target.value)
                    }
                  />
                </FormField>
                <FormField
                  label="Emergency Contact Phone"
                  id="emergencyContactPhone"
                  error={errors.emergencyContactPhone}
                  success={
                    !errors.emergencyContactPhone &&
                    touchedFields.emergencyContactPhone
                  }
                >
                  <InputWithError
                    id="emergencyContactPhone"
                    value={formData.emergencyContactPhone}
                    onChange={(e) =>
                      handleFieldChange(
                        "emergencyContactPhone",
                        formatPhoneNumber(e.target.value),
                      )
                    }
                    placeholder="+251/7xx-xxx-xxx"
                    error={errors.emergencyContactPhone}
                  />
                </FormField>
              </div>
            </div>

            <Separator />

            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="siblingInSchool"
                  checked={formData.siblingInSchool}
                  onCheckedChange={(checked) =>
                    handleFieldChange("siblingInSchool", checked)
                  }
                />
                <Label htmlFor="siblingInSchool">
                  Does the student have siblings currently enrolled in this
                  school?
                </Label>
              </div>

              {formData.siblingInSchool && (
                <div className="ml-6 space-y-2 p-4 bg-gray-50 rounded-lg">
                  <FormField
                    label="Sibling Information"
                    id="siblingDetails"
                    error={errors.siblingDetails}
                    success={
                      !errors.siblingDetails && touchedFields.siblingDetails
                    }
                  >
                    <TextareaWithError
                      id="siblingDetails"
                      value={formData.siblingDetails}
                      onChange={(e) =>
                        handleFieldChange("siblingDetails", e.target.value)
                      }
                      placeholder="Please provide names and grades of siblings currently enrolled"
                      rows={3}
                      error={errors.siblingDetails}
                    />
                  </FormField>
                </div>
              )}
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <Heart className="h-5 w-5 text-red-600" />
              <h3 className="text-lg font-semibold">{currentStepName}</h3>
            </div>

            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="hasMedicalCondition"
                  checked={formData.hasMedicalCondition}
                  onCheckedChange={(checked) =>
                    handleFieldChange("hasMedicalCondition", checked)
                  }
                />
                <Label htmlFor="hasMedicalCondition">
                  Does the student have any medical conditions?
                </Label>
              </div>

              {formData.hasMedicalCondition && (
                <div className="ml-6 space-y-2 p-4 bg-red-50 rounded-lg">
                  <FormField
                    label="Medical Condition Details"
                    id="medicalDetails"
                    required
                    error={errors.medicalDetails}
                    success={
                      !errors.medicalDetails && touchedFields.medicalDetails
                    }
                  >
                    <TextareaWithError
                      id="medicalDetails"
                      value={formData.medicalDetails}
                      onChange={(e) =>
                        handleFieldChange("medicalDetails", e.target.value)
                      }
                      placeholder="Please describe the medical condition and any required care"
                      rows={3}
                      error={errors.medicalDetails}
                    />
                  </FormField>
                </div>
              )}
            </div>

            <FormField
              label="Allergies"
              id="allergies"
              error={errors.allergies}
              success={!errors.allergies && touchedFields.allergies}
            >
              <TextareaWithError
                id="allergies"
                value={formData.allergies}
                onChange={(e) => handleFieldChange("allergies", e.target.value)}
                placeholder="List any known allergies (food, environmental, medications, etc.)"
                rows={2}
                error={errors.allergies}
              />
            </FormField>

            <Separator />

            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="hasDisability"
                  checked={formData.hasDisability}
                  onCheckedChange={(checked) =>
                    handleFieldChange("hasDisability", checked)
                  }
                />
                <Label htmlFor="hasDisability">
                  Does the student have any disabilities?
                </Label>
              </div>

              {formData.hasDisability && (
                <div className="ml-6 space-y-2 p-4 bg-blue-50 rounded-lg">
                  <FormField
                    label="Disability Details"
                    id="disabilityDetails"
                    required
                    error={errors.disabilityDetails}
                    success={
                      !errors.disabilityDetails &&
                      touchedFields.disabilityDetails
                    }
                  >
                    <TextareaWithError
                      id="disabilityDetails"
                      value={formData.disabilityDetails}
                      onChange={(e) =>
                        handleFieldChange("disabilityDetails", e.target.value)
                      }
                      placeholder="Please describe the disability and any support needed"
                      rows={3}
                      error={errors.disabilityDetails}
                    />
                  </FormField>
                </div>
              )}
            </div>

            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="requiresAccommodation"
                  checked={formData.requiresAccommodation}
                  onCheckedChange={(checked) =>
                    handleFieldChange("requiresAccommodation", checked)
                  }
                />
                <Label htmlFor="requiresAccommodation">
                  Does the student require special accommodations?
                </Label>
              </div>

              {formData.requiresAccommodation && (
                <div className="ml-6 space-y-2 p-4 bg-yellow-50 rounded-lg">
                  <FormField
                    label="Special Accommodation Details"
                    id="accommodationDetails"
                    required
                    error={errors.accommodationDetails}
                    success={
                      !errors.accommodationDetails &&
                      touchedFields.accommodationDetails
                    }
                  >
                    <TextareaWithError
                      id="accommodationDetails"
                      value={formData.accommodationDetails}
                      onChange={(e) =>
                        handleFieldChange(
                          "accommodationDetails",
                          e.target.value,
                        )
                      }
                      placeholder="Please describe the special accommodations needed"
                      rows={3}
                      error={errors.accommodationDetails}
                    />
                  </FormField>
                </div>
              )}
            </div>
          </div>
        );

      case 6:
        return (
          <div className="space-y-6">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="h-5 w-5 text-indigo-600" />
              <h3 className="text-lg font-semibold">{currentStepName}</h3>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label>Extracurricular Interests</Label>
                <p className="text-sm text-gray-600">
                  Select activities the student is interested in:
                </p>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                  {extracurricularOptions.map((activity) => (
                    <div key={activity} className="flex items-center space-x-2">
                      <Checkbox
                        id={activity}
                        checked={selectedExtracurriculars.includes(activity)}
                        onCheckedChange={() =>
                          handleExtracurricularToggle(activity)
                        }
                      />
                      <Label htmlFor={activity} className="text-sm">
                        {activity}
                      </Label>
                    </div>
                  ))}
                </div>
                {selectedExtracurriculars.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {selectedExtracurriculars.map((activity) => (
                      <Badge key={activity} variant="secondary">
                        {activity}
                      </Badge>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <Separator />

            <div className="space-y-4">
              <h4 className="font-medium">Registration Summary</h4>
              <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                <p>
                  <strong>Student:</strong> {formData.firstName}{" "}
                  {formData.lastName}
                </p>
                <p>
                  <strong>Grade:</strong> {formData.grade}
                </p>
                <p>
                  <strong>Academic Year:</strong> {formData.academicYear}
                </p>
                <p>
                  <strong>Father:</strong> {formData.fatherName}
                </p>
                <p>
                  <strong>Contact:</strong> {formData.fatherPhone}
                </p>
                {formData.isTransfer && (
                  <p>
                    <strong>Transfer Student:</strong> Yes (from{" "}
                    {formData.previousSchool})
                  </p>
                )}
                {formData.hasMedicalCondition && (
                  <p>
                    <strong>Medical Condition:</strong> Yes
                  </p>
                )}
                {formData.hasDisability && (
                  <p>
                    <strong>Disability:</strong> Yes
                  </p>
                )}
                {formData.requiresAccommodation && (
                  <p>
                    <strong>Special Accommodations:</strong> Yes
                  </p>
                )}
              </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Note:</strong> Please review all information carefully
                before submitting. You will receive a confirmation email once
                the registration is processed.
              </p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        <Card className="shadow-xl">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl font-bold text-gray-800">
              Student Registration Form
            </CardTitle>
            <CardDescription className="text-lg">
              Complete all steps to register your student for the upcoming
              academic year
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
              <Button
                variant="outline"
                onClick={prevStep}
                disabled={currentStep === 1}
                className="px-8"
              >
                Previous
              </Button>

              {currentStep < totalSteps ? (
                <Button onClick={nextStep} className="px-8">
                  Next Step
                </Button>
              ) : (
                <Button
                  onClick={handleSubmit}
                  className="px-8 bg-green-600 hover:bg-green-700"
                >
                  Submit Registration
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
  );
}
