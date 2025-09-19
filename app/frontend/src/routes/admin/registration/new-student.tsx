import {
  getGradesOptions,
  registerNewStudentMutation,
  registerStudentStep1Mutation,
  registerStudentStep2Mutation,
  registerStudentStep3Mutation,
  registerStudentStep4Mutation,
  registerStudentStep5Mutation,
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
import AdvanceTooltip from "@/components/advance-tooltip";
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled";
import { DateWithLabel } from "@/components/inputs/date-labeled";
import { FileUploadField } from "@/components/inputs/file-upload-field";
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
import {
  resetForm,
  setFormData,
  setFormStep,
} from "@/store/slice/student-registration-slice";
import { extractFirstWord } from "@/utils/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Loader, RefreshCcw, Save } from "lucide-react";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

// undefined fields are optional

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
  const { data: initialData, step } = store.getState().studentRegistrationForm;
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [currentStep, setCurrentStep] = useState(step);
  const [savePending, setSavePending] = useState(false);
  const [resetPending, setResetPending] = useState(false);

  const [step1InitialValues] = useState<StudRegStep1>({
    firstName: initialData.firstName,
    fatherName: initialData.fatherName,
    grandFatherName: initialData.grandFatherName,
    dateOfBirth: initialData.dateOfBirth,
    gender: initialData.gender,
    nationality: initialData.nationality,
    studentPhoto: initialData.studentPhoto,
  });
  const [step2InitialValues] = useState<StudRegStep2>({
    registeredForGradeId: initialData.registeredForGradeId,
    transportation: initialData.transportation,
    isTransfer: initialData.isTransfer,
    previousSchool: initialData.previousSchool,
  });

  const [step3InitialValues] = useState<StudRegStep3>({
    address: initialData.address,
    city: initialData.city,
    state: initialData.state,
    postalCode: initialData.postalCode,
    fatherPhone: initialData.fatherPhone,
    motherPhone: initialData.motherPhone,
    parentEmail: initialData.parentEmail,
  });
  const [step4InitialValues] = useState<StudRegStep4>({
    guardianName: initialData.guardianName,
    guardianPhone: initialData.guardianPhone,
    guardianRelation: initialData.guardianRelation,
    emergencyContactName: initialData.emergencyContactName,
    emergencyContactPhone: initialData.emergencyContactPhone,
    siblingInSchool: initialData.siblingInSchool,
    siblingDetails: initialData.siblingDetails,
  });
  const [step5InitialValues] = useState<StudRegStep5>({
    hasMedicalCondition: initialData.hasMedicalCondition,
    medicalDetails: initialData.medicalDetails,
    hasDisability: initialData.hasDisability,
    disabilityDetails: initialData.disabilityDetails,
  });

  const form = useForm<StudentRegistrationForm>({
    resolver: zodResolver(zStudentRegistrationForm),
    defaultValues: initialData,
  });
  const step1Form = useForm<StudRegStep1>({
    resolver: zodResolver(zStudRegStep1),
    defaultValues: step1InitialValues,
  });
  const step2Form = useForm<StudRegStep2>({
    resolver: zodResolver(zStudRegStep2),
    defaultValues: step2InitialValues,
  });
  const step3Form = useForm<StudRegStep3>({
    resolver: zodResolver(zStudRegStep3),
    defaultValues: step3InitialValues,
  });
  const step4Form = useForm<StudRegStep4>({
    resolver: zodResolver(zStudRegStep4),
    defaultValues: step4InitialValues,
  });
  const step5Form = useForm<StudRegStep5>({
    resolver: zodResolver(zStudRegStep5),
    defaultValues: step5InitialValues,
  });

  const { reset, setError, setValue } = form;

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
      dispatch(resetForm());
      reset(initialData);
      navigate({
        to: "/admin/registration/students",
      });
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
      dispatch(setFormData(form.getValues()));
      dispatch(setFormStep(2));
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && Array.isArray(detail)) {
        detail.forEach(({ loc, msg }: { loc: string[]; msg: string }) => {
          step1Form.setError(extractFirstWord(loc, msg) as keyof StudRegStep1, {
            type: "server",
            message: msg,
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
      dispatch(setFormData(form.getValues()));
      dispatch(setFormStep(3));
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && Array.isArray(detail)) {
        detail.forEach(({ loc, msg }: { loc: string[]; msg: string }) => {
          step2Form.setError(extractFirstWord(loc, msg) as keyof StudRegStep2, {
            type: "server",
            message: msg,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 2.");
      }
    },
  });

  const step3Mutation = useMutation({
    ...registerStudentStep3Mutation(),
    onSuccess: () => {
      const step3Values = step3Form.getValues();
      Object.entries(step3Values).forEach(([key, value]) => {
        setValue(key as keyof StudRegStep3, value, {
          shouldDirty: true,
        });
      });
      setCurrentStep(4);
      dispatch(setFormData(form.getValues()));
      dispatch(setFormStep(4));
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;
      console.log(detail);

      if (detail && Array.isArray(detail)) {
        detail.forEach(({ loc, msg }: { loc: string[]; msg: string }) => {
          step3Form.setError(extractFirstWord(loc, msg) as keyof StudRegStep3, {
            type: "server",
            message: msg,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 3.");
      }
    },
  });

  const step4Mutation = useMutation({
    ...registerStudentStep4Mutation(),
    onSuccess: () => {
      const step4Values = step4Form.getValues();
      Object.entries(step4Values).forEach(([key, value]) => {
        setValue(key as keyof StudRegStep4, value, {
          shouldDirty: true,
        });
      });
      setCurrentStep(5);
      dispatch(setFormData(form.getValues()));
      dispatch(setFormStep(5));
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && Array.isArray(detail)) {
        detail.forEach(({ loc, msg }: { loc: string[]; msg: string }) => {
          step4Form.setError(extractFirstWord(loc, msg) as keyof StudRegStep4, {
            type: "server",
            message: msg,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 4.");
      }
    },
  });

  const step5Mutation = useMutation({
    ...registerStudentStep5Mutation(),
    onSuccess: () => {
      const step5Values = step5Form.getValues();
      Object.entries(step5Values).forEach(([key, value]) => {
        setValue(key as keyof StudRegStep5, value, {
          shouldDirty: true,
        });
      });
      dispatch(setFormData(form.getValues()));
      dispatch(setFormStep(5));
      handleSave();
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && Array.isArray(detail)) {
        detail.forEach(({ loc, msg }: { loc: string[]; msg: string }) => {
          step5Form.setError(extractFirstWord(loc, msg) as keyof StudRegStep5, {
            type: "server",
            message: msg,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 5.");
      }
    },
  });

  const onStep1Submit = step1Form.handleSubmit((data) =>
    step1Mutation.mutate({ body: data }),
  );

  const onStep2Submit = step2Form.handleSubmit((data) =>
    step2Mutation.mutate({ body: data }),
  );

  const onStep3Submit = step3Form.handleSubmit((data) =>
    step3Mutation.mutate({ body: data }),
  );

  const onStep4Submit = step4Form.handleSubmit((data) =>
    step4Mutation.mutate({ body: data }),
  );

  const onStep5Submit = step5Form.handleSubmit((data) =>
    step5Mutation.mutate({ body: data }),
  );

  const handleSave = () => {
    mutation.mutate({ body: form.getValues() });
  };

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
              <FileUploadField<StudRegStep1>
                nameInSchema="studentPhoto"
                fieldTitle="Student Photo"
                description="Upload Recent 4x4 Student Picture"
                accept={{ "image/*": [] }}
                maxFiles={1}
                maxSize={1024 * 1024 * 5}
              />
            </div>
            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button variant="outline" disabled={true} className="px-8">
                Previous
              </Button>
              <Button
                type="submit"
                onClick={onStep1Submit}
                disabled={step1Mutation.isPending}
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
                disabled={step2Mutation.isPending}
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
                type="submit"
                onClick={onStep3Submit}
                disabled={step3Mutation.isPending}
                className="px-8"
              >
                {step3Mutation.isPending && <Loader className="animate-spin" />}
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
                type="submit"
                onClick={onStep4Submit}
                disabled={step4Mutation.isPending}
                className="px-8"
              >
                {step4Mutation.isPending && <Loader className="animate-spin" />}
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
                type="submit"
                onClick={onStep5Submit}
                disabled={step5Mutation.isPending || mutation.isPending}
                className="px-8 bg-green-600 hover:bg-green-700"
              >
                {(step5Mutation.isPending || mutation.isPending) && (
                  <Loader className="animate-spin" />
                )}
                Submit Registration
              </Button>{" "}
            </div>
          </FormProvider>
        );

      default:
        return null;
    }
  };

  return (
    <Card>
      <CardHeader className="text-center">
        <div className="flex justify-between items-center w-full">
          <AdvanceTooltip
            tooltip="Save Progress"
            isPending={savePending}
            size="sm"
            onClick={() => {
              setSavePending(true);
              setTimeout(() => setSavePending(false), 500);
              dispatch(
                setFormData({
                  ...step1Form.getValues(),
                  ...step2Form.getValues(),
                  ...step3Form.getValues(),
                  ...step4Form.getValues(),
                  ...step5Form.getValues(),
                }),
              );
              dispatch(setFormStep(currentStep));
            }}
            className="ml-2 h-10 w-10 rounded-full"
          >
            <Save className="h-4 w-4" />
          </AdvanceTooltip>
          <CardTitle className="text-3xl font-bold text-gray-800">
            Student Registration Form
          </CardTitle>
          <AdvanceTooltip
            tooltip="Reset Form"
            isPending={resetPending}
            size="sm"
            onClick={() => {
              setResetPending(true);
              setTimeout(() => setResetPending(false), 300);
              dispatch(resetForm());
              form.reset(initialData);
              step1Form.reset(step1InitialValues);
              step2Form.reset(step2InitialValues);
              step3Form.reset(step3InitialValues);
              step4Form.reset(step4InitialValues);
              step5Form.reset(step5InitialValues);
              setCurrentStep(1);
            }}
            className="ml-2 h-10 w-10 rounded-full"
          >
            <RefreshCcw className="h-4 w-4" />
          </AdvanceTooltip>
        </div>
        <CardDescription className="text-lg">
          Complete all steps to register your student for the upcoming academic
          year
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
      </CardContent>
    </Card>
  );
}
