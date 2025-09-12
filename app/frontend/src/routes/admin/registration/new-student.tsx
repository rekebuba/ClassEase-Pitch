import {
  getGradesOptions,
  registerNewStudentMutation,
  registerStudentStep1Mutation,
  registerStudentStep2Mutation,
} from "@/client/@tanstack/react-query.gen";
import {
  StudentRegistrationForm,
  StudRegStep1,
  StudRegStep2,
  StudRegStep3,
  StudRegStep4,
  StudRegStep5,
} from "@/client/types.gen";
import {
  zBloodTypeEnum,
  zStudentRegistrationForm,
  zStudRegStep1,
  zStudRegStep2,
  zStudRegStep3,
  zStudRegStep4,
  zStudRegStep5,
} from "@/client/zod.gen";
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled";
import { DateWithLabel } from "@/components/inputs/date-labeled";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { PhoneInputWithLabel } from "@/components/inputs/phone-input-labeled";
import { RadioGroupLabel } from "@/components/inputs/radio-group-labeled";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
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
import { Separator } from "@/components/ui/separator";
import {
  Stepper,
  StepperDescription,
  StepperIndicator,
  StepperItem,
  StepperSeparator,
  StepperTitle,
  StepperTrigger,
} from "@/components/ui/stepper";
import { store } from "@/store/main-store";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Loader, Upload } from "lucide-react";
import { useCallback, useState } from "react";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import { toast } from "sonner";

// undefined fields are optional
const initialFormData: StudentRegistrationForm = {
  registeredForGradeId: "",
  firstName: "",
  fatherName: "",
  grandFatherName: "",
  dateOfBirth: "",
  gender: undefined as any,
  nationality: "",
  bloodType: undefined,
  studentPhoto: undefined,
  isTransfer: false,
  previousSchool: "",
  address: "",
  city: "",
  state: "",
  postalCode: "",
  fatherPhone: "",
  motherPhone: "",
  parentEmail: "",
  guardianName: "",
  guardianPhone: "",
  guardianRelation: null,
  emergencyContactName: null,
  emergencyContactPhone: null,
  hasMedicalCondition: false,
  medicalDetails: "",
  hasDisability: false,
  disabilityDetails: "",
  transportation: null,
  siblingInSchool: false,
  siblingDetails: "",
};

const steps = [
  {
    step: 1,
    title: "Step One",
    description: "Personal Information",
  },
  {
    step: 2,
    title: "Step Two",
    description: "Academic Information",
  },
  {
    step: 3,
    title: "Step Three",
    description: "Address & Contact",
  },
  {
    step: 4,
    title: "Step Four",
    description: "Guardian & Emergency Contact",
  },
  {
    step: 5,
    title: "Step Five",
    description: "Medical Information",
  },
];

export const Route = createFileRoute("/admin/registration/new-student")({
  component: RouteComponent,
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(1);
  const [defaultValues] = useState<StudentRegistrationForm>(initialFormData);

  const form = useForm<StudentRegistrationForm>({
    resolver: zodResolver(zStudentRegistrationForm),
    defaultValues,
  });
  const step1Form = useForm<StudRegStep1>({
    resolver: zodResolver(zStudRegStep1),
    defaultValues: {
      firstName: defaultValues.firstName,
      fatherName: defaultValues.fatherName,
      grandFatherName: defaultValues.grandFatherName,
      dateOfBirth: defaultValues.dateOfBirth,
      gender: defaultValues.gender,
      nationality: defaultValues.nationality,
    },
  });
  const step2Form = useForm<StudRegStep2>({
    resolver: zodResolver(zStudRegStep2),
    defaultValues: {
      registeredForGradeId: defaultValues.registeredForGradeId,
      transportation: defaultValues.transportation,
      isTransfer: defaultValues.isTransfer,
      previousSchool: defaultValues.previousSchool,
    },
  });
  const step3Form = useForm<StudRegStep3>({
    resolver: zodResolver(zStudRegStep3),
    defaultValues: {
      address: defaultValues.address,
      city: defaultValues.city,
      state: defaultValues.state,
      postalCode: defaultValues.postalCode,
      fatherPhone: defaultValues.fatherPhone,
      motherPhone: defaultValues.motherPhone,
      parentEmail: defaultValues.parentEmail,
    },
  });
  const step4Form = useForm<StudRegStep4>({
    resolver: zodResolver(zStudRegStep4),
    defaultValues: {
      guardianName: defaultValues.guardianName,
      guardianPhone: defaultValues.guardianPhone,
      guardianRelation: defaultValues.guardianRelation,
      emergencyContactName: defaultValues.emergencyContactName,
      emergencyContactPhone: defaultValues.emergencyContactPhone,
      siblingInSchool: defaultValues.siblingInSchool,
      siblingDetails: defaultValues.siblingDetails,
    },
  });
  const step5Form = useForm<StudRegStep5>({
    resolver: zodResolver(zStudRegStep5),
    defaultValues: {
      hasMedicalCondition: defaultValues.hasMedicalCondition,
      medicalDetails: defaultValues.medicalDetails,
      hasDisability: defaultValues.hasDisability,
      disabilityDetails: defaultValues.disabilityDetails,
    },
  });

  const {
    formState: { isDirty },
    reset,
    handleSubmit,
    setError,
    setValue,
  } = form;

  const { data: grades } = useQuery({
    ...getGradesOptions({
      query: { yearId: yearId! },
    }),
    enabled: !!yearId,
  });

  const mutation = useMutation({
    ...registerNewStudentMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      handleCancel();
      reset(defaultValues);
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          setError(field as keyof StudentRegistrationForm, {
            type: "server",
            message: message as string,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Register Student.");
      }
    },
  });

  const step1Mutation = useMutation({
    ...registerStudentStep1Mutation(),
    onSuccess: () => {
      const step1Values = step1Form.getValues();
      Object.entries(step1Values).forEach(([key, value]) => {
        setValue(key as keyof StudRegStep1, value, {
          shouldDirty: true,
        });
      });
      setCurrentStep(2);
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          setError(field as keyof StudentRegistrationForm, {
            type: "server",
            message: message as string,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 1.");
      }
    },
  });

  const step2Mutation = useMutation({
    ...registerStudentStep2Mutation(),
    onSuccess: () => {
      const step2Values = step2Form.getValues();
      Object.entries(step2Values).forEach(([key, value]) => {
        setValue(key as keyof StudRegStep2, value, {
          shouldDirty: true,
        });
      });
      setCurrentStep(3);
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;
      console.log(detail);

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          setError(field as keyof StudentRegistrationForm, {
            type: "server",
            message: message as string,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 1.");
      }
    },
  });

  const onStep1Submit = step1Form.handleSubmit((data) =>
    step1Mutation.mutate({ body: data }),
  );

  const onStep2Submit = step2Form.handleSubmit((data) =>
    step2Mutation.mutate({ body: data }),
  );

  // const onStep3Submit = step3Form.handleSubmit(
  //   (data) => step3Mutation.mutate({ body: data }),
  // );

  // const onStep4Submit = step4Form.handleSubmit(
  //   (data) => step4Mutation.mutate({ body: data }),
  // );

  // const onStep5Submit = step5Form.handleSubmit(
  //   (data) => step5Mutation.mutate({ body: data }),
  // );

  const onValid: SubmitHandler<StudentRegistrationForm> = (data) => {
    mutation.mutate({ body: data });
  };
  const handleSave = handleSubmit(onValid);

  const handleCancel = useCallback(() => {
    navigate({
      to: "/admin/registration/student",
    });
  }, [navigate]);

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <FormProvider {...step1Form}>
            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-medium text-blue-800">
                Step 1: Personal Information
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Please provide the student's basic personal details. Fields
                marked with * are required. Use the student's legal name as it
                appears on official documents.
              </p>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <InputWithLabel<StudRegStep1>
                  nameInSchema="firstName"
                  fieldTitle="First Name *"
                  placeholder="Enter First Name"
                  description="Student's legal first name"
                />
                <InputWithLabel<StudRegStep1>
                  nameInSchema="fatherName"
                  fieldTitle="Father Name *"
                  placeholder="Enter Father Name"
                  description="Student's father's full name"
                />
                <InputWithLabel<StudRegStep1>
                  nameInSchema="grandFatherName"
                  fieldTitle="Grandfather Name"
                  placeholder="Enter Grandfather Name"
                  description="Student's paternal grandfather name (optional)"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <DateWithLabel<StudRegStep1>
                  nameInSchema="dateOfBirth"
                  fieldTitle="Date of Birth *"
                  placeholder="Select date of birth"
                  description="Student's date of birth"
                />
                <div className="space-y-2 w-[200px]">
                  <RadioGroupLabel<StudRegStep1, string>
                    fieldTitle="Gender *"
                    nameInSchema="gender"
                    options={[
                      { label: "Male", value: "male" },
                      { label: "Female", value: "female" },
                    ]}
                  />
                </div>
                <InputWithLabel<StudRegStep1>
                  nameInSchema="nationality"
                  fieldTitle="Nationality *"
                  placeholder="Enter Nationality"
                  description="Student's nationality (e.g., Ethiopian)"
                />
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
                  <p className="text-xs text-gray-400 mt-1">
                    Recent passport-style photo with plain background
                  </p>
                </div>
              </div>
            </div>
            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button variant="outline" disabled={true} className="px-8">
                Previous
              </Button>
              <Button
                type="submit"
                onClick={onStep1Submit}
                disabled={
                  !step1Form.formState.isDirty || step1Mutation.isPending
                }
                className="px-8"
              >
                {step1Mutation.isPending && <Loader className="animate-spin" />}
                Next Step
              </Button>
            </div>
          </FormProvider>
        );

      case 2:
        return (
          <FormProvider {...step2Form}>
            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-medium text-blue-800">
                Step 2: Academic Information
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Provide information about the student's academic level and
                transportation needs. The transfer information section only
                needs to be completed if applicable.
              </p>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <SelectWithLabel<StudRegStep2, string>
                  fieldTitle="Grade Level *"
                  nameInSchema="registeredForGradeId"
                  description="Select the grade the student will be entering"
                >
                  {grades?.map((grade) => (
                    <SelectItem key={grade.id} value={grade.id}>
                      Grade {grade.grade}
                    </SelectItem>
                  ))}
                </SelectWithLabel>
                <SelectWithLabel<StudRegStep2, string>
                  fieldTitle="Transportation Method"
                  nameInSchema="transportation"
                  description="How will the student get to school? (optional)"
                >
                  <SelectItem value="school-bus">School Bus</SelectItem>
                  <SelectItem value="parent-drop">Parent Drop-off</SelectItem>
                  <SelectItem value="walk">Walking</SelectItem>
                  <SelectItem value="bicycle">Bicycle</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectWithLabel>
              </div>
              <div className="space-y-4">
                <CheckboxWithLabel<StudRegStep2, boolean>
                  nameInSchema="isTransfer"
                  fieldTitle="Is the student transferring from another school?"
                />
                {step2Form.watch().isTransfer && (
                  <div className="ml-6 space-y-2 p-4 bg-blue-50 rounded-lg">
                    <InputWithLabel<StudRegStep2>
                      nameInSchema="previousSchool"
                      fieldTitle="Previous School Name"
                      placeholder="Enter previous school name"
                      description="Name of the school the student previously attended"
                    />
                  </div>
                )}
              </div>
            </div>
            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button
                variant="outline"
                onClick={() => setCurrentStep(1)}
                className="px-8"
              >
                Previous
              </Button>
              <Button
                type="submit"
                onClick={onStep2Submit}
                disabled={
                  !step2Form.formState.isDirty || step2Mutation.isPending
                }
                className="px-8"
              >
                {step2Mutation.isPending && <Loader className="animate-spin" />}
                Next Step
              </Button>
            </div>
          </FormProvider>
        );

      case 3:
        return (
          <FormProvider {...step3Form}>
            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-medium text-blue-800">
                Step 3: Contact Information
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Please provide the student's primary address and parent/guardian
                contact details. At least one phone number is required for
                emergency contact purposes.
              </p>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <InputWithLabel<StudRegStep3>
                  nameInSchema="address"
                  fieldTitle="Street Address *"
                  placeholder="Enter street address"
                  description="House number, street name, and neighborhood"
                />
                <InputWithLabel<StudRegStep3>
                  nameInSchema="city"
                  fieldTitle="City *"
                  placeholder="Enter city"
                  description="City of residence"
                />
                <InputWithLabel<StudRegStep3>
                  nameInSchema="state"
                  fieldTitle="State/Province *"
                  placeholder="Enter state or province"
                  description="State or province of residence"
                />
              </div>
              <Separator />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <PhoneInputWithLabel<StudRegStep3>
                  nameInSchema="fatherPhone"
                  fieldTitle="Father's Phone Number *"
                  description="Primary contact number for the father (Use Country Code +251)"
                />
                <PhoneInputWithLabel<StudRegStep3>
                  nameInSchema="motherPhone"
                  fieldTitle="Mother's Phone Number (Optional)"
                  description="Primary contact number for the mother (Use Country Code +251)"
                />
              </div>
              <InputWithLabel<StudRegStep3>
                nameInSchema="parentEmail"
                fieldTitle="Parent/Guardian Email *"
                placeholder="Enter Parent/Guardian Email"
                description="Primary email for school communications"
              />
            </div>

            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button
                variant="outline"
                onClick={() => setCurrentStep(2)}
                className="px-8"
              >
                Previous
              </Button>
              <Button
                onClick={() => setCurrentStep(4)}
                disabled={currentStep >= steps.length}
                className="px-8"
              >
                Next Step
              </Button>
            </div>
          </FormProvider>
        );

      case 4:
        return (
          <FormProvider {...step4Form}>
            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-medium text-blue-800">
                Step 4: Guardian & Emergency Contacts
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Provide information about the student's primary guardian and
                emergency contacts. Emergency contact should be someone who can
                be reached if parents are unavailable.
              </p>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InputWithLabel<StudRegStep4>
                  nameInSchema="guardianName"
                  fieldTitle="Guardian Name *"
                  placeholder="Enter guardian name"
                  description="Full name of the primary guardian"
                />
                <SelectWithLabel<StudRegStep4, string>
                  fieldTitle="Select relationship *"
                  nameInSchema="guardianRelation"
                  description="Guardian's relationship to the student"
                >
                  <SelectItem value="parent">Parent</SelectItem>
                  <SelectItem value="grandparent">Grandparent</SelectItem>
                  <SelectItem value="aunt-uncle">Aunt/Uncle</SelectItem>
                  <SelectItem value="sibling">Sibling</SelectItem>
                  <SelectItem value="family-friend">Family Friend</SelectItem>
                  <SelectItem value="other">Other</SelectItem>
                </SelectWithLabel>
              </div>
              <PhoneInputWithLabel<StudRegStep4>
                nameInSchema="guardianPhone"
                fieldTitle="Guardian Phone Number *"
                placeholder="+251 9/7xx-xxx-xxx"
                description="Primary contact number for the guardian"
              />
              <Separator />
              <div className="space-y-4">
                <h4 className="font-medium text-red-600">
                  Emergency Contact (if different from above)
                </h4>
                <p className="text-sm text-gray-600 -mt-2">
                  Provide an alternative contact person in case of emergency
                  when parents cannot be reached
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <InputWithLabel<StudRegStep4>
                    nameInSchema="emergencyContactName"
                    fieldTitle="Emergency Contact Name"
                    placeholder="Enter emergency contact name"
                    description="Full name of emergency contact person"
                  />
                  <PhoneInputWithLabel<StudRegStep4>
                    nameInSchema="emergencyContactPhone"
                    fieldTitle="Emergency Contact Phone"
                    description="Phone number for emergency contact"
                  />
                </div>
              </div>
              <Separator />
              <div className="space-y-4">
                <CheckboxWithLabel<StudRegStep4, boolean>
                  nameInSchema="siblingInSchool"
                  fieldTitle="Does the student have siblings currently enrolled in this school?"
                />
                {step4Form.watch().siblingInSchool && (
                  <div className="ml-6 space-y-2 p-4 bg-gray-50 rounded-lg">
                    <InputWithLabel<StudRegStep4>
                      nameInSchema="siblingDetails"
                      fieldTitle="Sibling Information"
                      placeholder="Please provide names and grades of siblings currently enrolled"
                      description="Example: 'Abebe - Grade 5, Tigist - Grade 3'"
                    />
                  </div>
                )}
              </div>
            </div>
            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button
                variant="outline"
                onClick={() => setCurrentStep(3)}
                className="px-8"
              >
                Previous
              </Button>
              <Button
                onClick={() => setCurrentStep(5)}
                disabled={currentStep >= steps.length}
                className="px-8"
              >
                Next Step
              </Button>
            </div>
          </FormProvider>
        );

      case 5:
        return (
          <FormProvider {...step5Form}>
            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-medium text-blue-800">
                Step 5: Medical Information
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Provide important health information to help us ensure the
                student's well-being at school. All medical information is kept
                confidential and is only shared with authorized staff.
              </p>
            </div>

            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <SelectWithLabel<StudRegStep5, string>
                  fieldTitle="Select blood type"
                  nameInSchema="bloodType"
                  description="Student's blood type (optional but recommended for emergencies)"
                >
                  {zBloodTypeEnum.options.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectWithLabel>
              </div>
              <div className="space-y-4">
                <div className="flex items-center space-x-2">
                  <CheckboxWithLabel
                    nameInSchema="hasMedicalCondition"
                    fieldTitle="Does the student have any medical conditions?"
                  />
                </div>
                {step5Form.watch().hasMedicalCondition && (
                  <div className="ml-6 space-y-2 p-4 bg-blue-50 rounded-lg">
                    <InputWithLabel<StudRegStep5>
                      nameInSchema="medicalDetails"
                      fieldTitle="Medical Condition Details"
                      placeholder="Please describe the medical condition and any required care"
                      description="Include condition name, medications, and emergency procedures if needed"
                    />
                  </div>
                )}
              </div>
              <Separator />
              <div className="space-y-4">
                <CheckboxWithLabel
                  nameInSchema="hasDisability"
                  fieldTitle="Does the student have any disabilities?"
                />
                {step5Form.watch().hasDisability && (
                  <div className="ml-6 space-y-2 p-4 bg-blue-50 rounded-lg">
                    <InputWithLabel<StudRegStep5>
                      nameInSchema="disabilityDetails"
                      fieldTitle="Disability Details"
                      placeholder="Please describe the disability and any support needed"
                      description="Describe the disability and any accommodations or support required"
                    />
                  </div>
                )}
              </div>
            </div>
            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button
                variant="outline"
                onClick={() => setCurrentStep(4)}
                className="px-8"
              >
                Previous
              </Button>
              <Button
                disabled={!isDirty || mutation.isPending}
                type="submit"
                onClick={handleSave}
                className="px-8 bg-green-600 hover:bg-green-700"
              >
                {mutation.isPending && <Loader className="animate-spin" />}
                Submit Registration
              </Button>
            </div>
          </FormProvider>
        );

      default:
        return null;
    }
  };

  return (
    // <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
    <>
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-3xl font-bold text-gray-800">
            Student Registration Form
          </CardTitle>
          <CardDescription className="text-lg">
            Complete all steps to register your student for the upcoming
            academic year
          </CardDescription>
          <CardDescription className="space-y-8 text-center">
            <Stepper value={currentStep} onValueChange={setCurrentStep}>
              {steps.map(({ step, title, description }) => (
                <StepperItem
                  key={step}
                  step={step}
                  className="relative flex-1 flex-col!"
                >
                  <StepperTrigger
                    className="flex-col gap-3 rounded"
                    onClick={() => {}}
                  >
                    <StepperIndicator />
                    <div className="space-y-0.5 px-2">
                      <StepperTitle>{title}</StepperTitle>
                      <StepperDescription>{description}</StepperDescription>
                    </div>
                  </StepperTrigger>
                  {step < steps.length && (
                    <StepperSeparator className="absolute inset-x-0 top-3 left-[calc(50%+0.75rem+0.125rem)] -order-1 m-0 -translate-y-1/2 group-data-[orientation=horizontal]/stepper:w-[calc(100%-1.5rem-0.25rem)] group-data-[orientation=horizontal]/stepper:flex-none" />
                  )}
                </StepperItem>
              ))}
            </Stepper>
          </CardDescription>
        </CardHeader>

        <CardContent className="p-8">
          <div className="w-full">{renderStep()}</div>
          {/* <div className="flex justify-between mt-8 pt-6 border-t">
            <Button
              variant="outline"
              onClick={() => setCurrentStep((prev) => prev - 1)}
              disabled={currentStep === 1}
              className="px-8"
            >
              Previous
            </Button>
            {currentStep < totalSteps ? (
              <Button
                onClick={() => setCurrentStep((prev) => prev + 1)}
                disabled={currentStep >= steps.length}
                className="px-8"
              >
                Next Step
              </Button>
            ) : (
              <Button
                disabled={!isDirty || mutation.isPending}
                type="submit"
                onClick={handleSave}
                className="px-8 bg-green-600 hover:bg-green-700"
              >
                {mutation.isPending && <Loader className="animate-spin" />}
                Submit Registration
              </Button>
            )}
          </div> */}
        </CardContent>
      </Card>
    </>
  );
}
