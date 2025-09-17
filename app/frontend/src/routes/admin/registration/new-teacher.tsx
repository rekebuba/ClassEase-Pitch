import {
  registerNewTeacherMutation,
  registerTeacherStep1Mutation,
  registerTeacherStep2Mutation,
  registerTeacherStep3Mutation,
  registerTeacherStep4Mutation,
  registerTeacherStep5Mutation,
} from "@/client/@tanstack/react-query.gen";
import {
  TeacherRegistrationForm,
  TeacherRegStep1,
  TeacherRegStep2,
  TeacherRegStep3,
  TeacherRegStep4,
  TeacherRegStep5,
} from "@/client/types.gen";
import {
  zTeacherRegistrationForm,
  zTeacherRegStep1,
  zTeacherRegStep2,
  zTeacherRegStep3,
  zTeacherRegStep4,
  zTeacherRegStep5,
} from "@/client/zod.gen";
import AdvanceTooltip from "@/components/advance-tooltip";
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled";
import { DateWithLabel } from "@/components/inputs/date-labeled";
import { FileUploadField } from "@/components/inputs/file-upload-field";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { PhoneInputWithLabel } from "@/components/inputs/phone-input-labeled";
import { RadioGroupLabel } from "@/components/inputs/radio-group-labeled";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
import { TextareaWithLabel } from "@/components/inputs/textarea-labeled";
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
import {
  // NOTE: Assuming a Redux slice for teacher registration exists
  resetForm,
  setFormData,
  setFormStep,
} from "@/store/slice/teacher-registration-slice";
import { extractFirstWord } from "@/utils/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Loader, RefreshCcw, Save, Upload } from "lucide-react";
import { useCallback, useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

const steps = [
  { step: 1, title: "Step One", description: "Personal Information" },
  { step: 2, title: "Step Two", description: "Contact Information" },
  { step: 3, title: "Step Three", description: "Educational Background" },
  { step: 4, title: "Step Four", description: "Teaching & Experience" },
  { step: 5, title: "Step Five", description: "Background & References" },
];

export const Route = createFileRoute("/admin/registration/new-teacher")({
  component: RouteComponent,
});

function RouteComponent() {
  // NOTE: Assuming a 'teacherRegistrationForm' slice exists in your Redux store
  const { data: initialData, step } = store.getState().teacherRegistrationForm;
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [currentStep, setCurrentStep] = useState(step);
  const [savePending, setSavePending] = useState(false);
  const [resetPending, setResetPending] = useState(false);

  const [step1InitialValues] = useState<TeacherRegStep1>({
    firstName: initialData.firstName,
    fatherName: initialData.fatherName,
    grandFatherName: initialData.grandFatherName,
    dateOfBirth: initialData.dateOfBirth,
    gender: initialData.gender,
    nationality: initialData.nationality,
    maritalStatus: initialData.maritalStatus,
    socialSecurityNumber: initialData.socialSecurityNumber,
  });

  const [step2InitialValues] = useState<TeacherRegStep2>({
    address: initialData.address,
    city: initialData.city,
    state: initialData.state,
    country: initialData.country,
    primaryPhone: initialData.primaryPhone,
    secondaryPhone: initialData.secondaryPhone,
    personalEmail: initialData.personalEmail,
    emergencyContactName: initialData.emergencyContactName,
    emergencyContactRelation: initialData.emergencyContactRelation,
    emergencyContactPhone: initialData.emergencyContactPhone,
  });

  const [step3InitialValues] = useState<TeacherRegStep3>({
    highestDegree: initialData.highestDegree,
    university: initialData.university,
    graduationYear: initialData.graduationYear,
    gpa: initialData.gpa,
    positionApplyingFor: initialData.positionApplyingFor,
    teachingLicense: initialData.teachingLicense,
    yearsOfExperience: initialData.yearsOfExperience,
  });

  const [step4InitialValues] = useState<TeacherRegStep4>({
    reference1Name: initialData.reference1Name,
    reference1Organization: initialData.reference1Organization,
    reference1Phone: initialData.reference1Phone,
    reference1Email: initialData.reference1Email,
  });

  const [step5InitialValues] = useState<TeacherRegStep5>({
    resume: initialData.resume,
    backgroundCheck: initialData.backgroundCheck,
    agreeToTerms: initialData.agreeToTerms,
    agreeToBackgroundCheck: initialData.agreeToBackgroundCheck,
  });

  const form = useForm<TeacherRegistrationForm>({
    resolver: zodResolver(zTeacherRegistrationForm),
    defaultValues: initialData,
  });
  const step1Form = useForm<TeacherRegStep1>({
    resolver: zodResolver(zTeacherRegStep1),
    defaultValues: step1InitialValues,
  });
  const step2Form = useForm<TeacherRegStep2>({
    resolver: zodResolver(zTeacherRegStep2),
    defaultValues: step2InitialValues,
  });
  const step3Form = useForm<TeacherRegStep3>({
    resolver: zodResolver(zTeacherRegStep3),
    defaultValues: step3InitialValues,
  });
  const step4Form = useForm<TeacherRegStep4>({
    resolver: zodResolver(zTeacherRegStep4),
    defaultValues: step4InitialValues,
  });
  const step5Form = useForm<TeacherRegStep5>({
    resolver: zodResolver(zTeacherRegStep5),
    defaultValues: step5InitialValues,
  });

  const { reset, setError, setValue } = form;

  // const { data: subjects } = useQuery({ ...getSubjectsOptions() });
  // const { data: gradeLevels } = useQuery({ ...getGradeLevelsOptions() });

  const mutation = useMutation({
    ...registerNewTeacherMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      handleCancel();
      dispatch(resetForm());
      reset(initialData);
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          setError(field as keyof TeacherRegistrationForm, {
            type: "server",
            message: message as string,
          });
        });
      } else {
        toast.error("Something went wrong. Failed to Register Teacher.");
      }
    },
  });

  const step1Mutation = useMutation({
    ...registerTeacherStep1Mutation(),
    onSuccess: () => {
      const step1Values = step1Form.getValues();
      Object.entries(step1Values).forEach(([key, value]) => {
        setValue(key as keyof TeacherRegStep1, value, {
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
          step1Form.setError(
            extractFirstWord(loc, msg) as keyof TeacherRegStep1,
            {
              type: "server",
              message: msg,
            },
          );
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 1.");
      }
    },
  });

  const step2Mutation = useMutation({
    ...registerTeacherStep2Mutation(),
    onSuccess: () => {
      const step2Values = step2Form.getValues();
      Object.entries(step2Values).forEach(([key, value]) => {
        setValue(key as keyof TeacherRegStep2, value, {
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
          step2Form.setError(
            extractFirstWord(loc, msg) as keyof TeacherRegStep2,
            {
              type: "server",
              message: msg,
            },
          );
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 2.");
      }
    },
  });

  const step3Mutation = useMutation({
    ...registerTeacherStep3Mutation(),
    onSuccess: () => {
      const step3Values = step3Form.getValues();
      Object.entries(step3Values).forEach(([key, value]) => {
        setValue(key as keyof TeacherRegStep3, value, {
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
          step3Form.setError(
            extractFirstWord(loc, msg) as keyof TeacherRegStep3,
            {
              type: "server",
              message: msg,
            },
          );
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 3.");
      }
    },
  });

  const step4Mutation = useMutation({
    ...registerTeacherStep4Mutation(),
    onSuccess: () => {
      const step4Values = step4Form.getValues();
      Object.entries(step4Values).forEach(([key, value]) => {
        setValue(key as keyof TeacherRegStep4, value, {
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
          step4Form.setError(
            extractFirstWord(loc, msg) as keyof TeacherRegStep4,
            {
              type: "server",
              message: msg,
            },
          );
        });
      } else {
        toast.error("Something went wrong. Failed to Validate Step 4.");
      }
    },
  });

  const step5Mutation = useMutation({
    ...registerTeacherStep5Mutation(),
    onSuccess: () => {
      const step5Values = step5Form.getValues();
      Object.entries(step5Values).forEach(([key, value]) => {
        setValue(key as keyof TeacherRegStep5, value, {
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
          step5Form.setError(
            extractFirstWord(loc, msg) as keyof TeacherRegStep5,
            {
              type: "server",
              message: msg,
            },
          );
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

  const handleCancel = useCallback(() => {
    navigate({
      to: "/admin/registration/teacher",
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
                Please provide your basic personal details. Fields marked with *
                are required.
              </p>
            </div>
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <InputWithLabel<TeacherRegStep1>
                  nameInSchema="firstName"
                  fieldTitle="First Name *"
                  placeholder="Enter First Name"
                />
                <InputWithLabel<TeacherRegStep1>
                  nameInSchema="fatherName"
                  fieldTitle="Father Name *"
                  placeholder="Enter Father Name"
                />
                <InputWithLabel<TeacherRegStep1>
                  nameInSchema="grandFatherName"
                  fieldTitle="Grandfather Name"
                  placeholder="Enter Grandfather Name"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <DateWithLabel<TeacherRegStep1>
                  nameInSchema="dateOfBirth"
                  fieldTitle="Date of Birth *"
                  placeholder="Select date of birth"
                />
                <RadioGroupLabel<TeacherRegStep1, string>
                  fieldTitle="Gender *"
                  nameInSchema="gender"
                  options={[
                    { label: "Male", value: "male" },
                    { label: "Female", value: "female" },
                  ]}
                />
                <InputWithLabel<TeacherRegStep1>
                  nameInSchema="nationality"
                  fieldTitle="Nationality *"
                  placeholder="Enter Nationality"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <SelectWithLabel<TeacherRegStep1, string>
                  fieldTitle="Marital Status"
                  nameInSchema="maritalStatus"
                  placeholder="Select marital status"
                >
                  <SelectItem value="single">Single</SelectItem>
                  <SelectItem value="married">Married</SelectItem>
                  <SelectItem value="divorced">Divorced</SelectItem>
                  <SelectItem value="widowed">Widowed</SelectItem>
                </SelectWithLabel>
                <InputWithLabel<TeacherRegStep1>
                  nameInSchema="socialSecurityNumber"
                  fieldTitle="Social Security Number"
                  placeholder="123-45-6789"
                />
              </div>
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
                Step 2: Contact Information
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Provide your primary address and contact details.
              </p>
            </div>
            <div className="space-y-6">
              <InputWithLabel<TeacherRegStep2>
                nameInSchema="address"
                fieldTitle="Street Address *"
                placeholder="Enter street address"
              />
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <InputWithLabel<TeacherRegStep2>
                  nameInSchema="city"
                  fieldTitle="City *"
                  placeholder="Enter city"
                />
                <InputWithLabel<TeacherRegStep2>
                  nameInSchema="state"
                  fieldTitle="State/Province *"
                  placeholder="Enter state"
                />
                <InputWithLabel<TeacherRegStep2>
                  nameInSchema="country"
                  fieldTitle="Country *"
                  placeholder="Enter country"
                />
              </div>
              <Separator />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <PhoneInputWithLabel<TeacherRegStep2>
                  nameInSchema="primaryPhone"
                  fieldTitle="Primary Phone Number *"
                  description="Use Country Code +251"
                />
                <PhoneInputWithLabel<TeacherRegStep2>
                  nameInSchema="secondaryPhone"
                  fieldTitle="Secondary Phone Number"
                  description="Use Country Code +251"
                />
              </div>
              <InputWithLabel<TeacherRegStep2>
                nameInSchema="personalEmail"
                fieldTitle="Personal Email *"
                placeholder="personal@example.com"
              />
              <Separator />
              <div className="space-y-4">
                <h4 className="font-medium text-red-600">Emergency Contact</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <InputWithLabel<TeacherRegStep2>
                    nameInSchema="emergencyContactName"
                    fieldTitle="Emergency Contact Name *"
                    placeholder="Enter full name"
                  />
                  <SelectWithLabel<TeacherRegStep2, string>
                    fieldTitle="Relationship *"
                    nameInSchema="emergencyContactRelation"
                  >
                    <SelectItem value="parent">Parent</SelectItem>
                    <SelectItem value="grandparent">Grandparent</SelectItem>
                    <SelectItem value="aunt-uncle">Aunt/Uncle</SelectItem>
                    <SelectItem value="spouse">Spouse</SelectItem>
                    <SelectItem value="family-friend">Family Friend</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectWithLabel>
                  <PhoneInputWithLabel<TeacherRegStep2>
                    nameInSchema="emergencyContactPhone"
                    fieldTitle="Emergency Contact Phone *"
                  />
                </div>
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
                Step 3: Educational & Professional Background
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Detail your qualifications and the position you're applying for.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputWithLabel<TeacherRegStep3>
                nameInSchema="positionApplyingFor"
                fieldTitle="Position Applying For *"
                placeholder="e.g., Elementary Teacher"
              />
            </div>
            <Separator />
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <SelectWithLabel<TeacherRegStep3, string>
                fieldTitle="Highest Degree *"
                nameInSchema="highestDegree"
                placeholder="Select highest degree"
              >
                <SelectItem value="bachelors">Bachelor's Degree</SelectItem>
                <SelectItem value="masters">Master's Degree</SelectItem>
                <SelectItem value="doctorate">Doctorate/PhD</SelectItem>
                <SelectItem value="other">Other</SelectItem>
              </SelectWithLabel>
              <InputWithLabel<TeacherRegStep3>
                nameInSchema="university"
                fieldTitle="University/College *"
                placeholder="Enter university name"
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputWithLabel<TeacherRegStep3>
                nameInSchema="graduationYear"
                fieldTitle="Graduation Year *"
                placeholder="2020"
                type="number"
              />
              <InputWithLabel<TeacherRegStep3>
                nameInSchema="gpa"
                fieldTitle="GPA"
                placeholder="3.50"
                type="number"
              />
            </div>
            <CheckboxWithLabel<TeacherRegStep3, boolean>
              nameInSchema="teachingLicense"
              fieldTitle="Do you have a valid teaching license?"
            />
            <SelectWithLabel<TeacherRegStep3, string>
              fieldTitle="Years of Teaching Experience *"
              nameInSchema="yearsOfExperience"
              placeholder="Select years of experience"
            >
              <SelectItem value="0">No experience</SelectItem>
              <SelectItem value="1-2">1-2 years</SelectItem>
              <SelectItem value="3-5">3-5 years</SelectItem>
              <SelectItem value="6-10">6-10 years</SelectItem>
              <SelectItem value="11-15">11-15 years</SelectItem>
              <SelectItem value="16-20">16-20 years</SelectItem>
              <SelectItem value="20+">20+ years</SelectItem>
            </SelectWithLabel>
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
                Step 4: Background Check & References
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Please provide this information for background screening
                purposes.
              </p>
            </div>
            <div className="space-y-6">
              <h4 className="font-medium text-blue-600">
                Professional References
              </h4>
              <div className="space-y-4 p-4 bg-blue-50 rounded-lg">
                <h5 className="font-medium">Reference 1 (Required)</h5>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <InputWithLabel<TeacherRegStep4>
                    nameInSchema="reference1Name"
                    fieldTitle="Name *"
                  />
                  <InputWithLabel<TeacherRegStep4>
                    nameInSchema="reference1Organization"
                    fieldTitle="Organization *"
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <PhoneInputWithLabel<TeacherRegStep4>
                    nameInSchema="reference1Phone"
                    fieldTitle="Phone Number *"
                  />
                  <InputWithLabel<TeacherRegStep4>
                    nameInSchema="reference1Email"
                    fieldTitle="Email (Optional)"
                    type="email"
                  />
                </div>
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
                Step 6: Documents & Final Information
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                Upload required documents and provide final statements.
              </p>
            </div>
            <div className="space-y-6">
              <h4 className="font-medium text-blue-600">Required Documents</h4>
              <FileUploadField<TeacherRegStep5>
                nameInSchema="resume"
                fieldTitle="Resume/CV *"
                description="Upload Recent Resume or CV"
                accept={{ "file/*": [] }}
                maxFiles={1}
                maxSize={1024 * 1024 * 5}
              />
            </div>

            <div className="space-y-4 mt-4">
              <h4 className="font-medium text-red-600">Terms and Agreements</h4>

              <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
                <div className="flex items-start space-x-2">
                  <CheckboxWithLabel<TeacherRegStep5, boolean>
                    nameInSchema="agreeToTerms"
                    fieldTitle="I agree to the terms and conditions of employment and understand that all information provided is accurate and complete. I understand that any false information may result in rejection of my application or termination of employment. *"
                  />
                </div>

                <div className="flex items-start space-x-2">
                  <CheckboxWithLabel<TeacherRegStep5, boolean>
                    nameInSchema="agreeToBackgroundCheck"
                    fieldTitle="I authorize the school district to conduct a comprehensive background check, including criminal history, employment verification, and reference checks. I understand this is required for all teaching positions. *"
                  />
                </div>
              </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Note:</strong> Please review all information carefully
                before submitting. After submission, you will receive a
                confirmation email and our HR team will contact you within 5-7
                business days regarding the next steps in the hiring process.
              </p>
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
            Teacher Registration Form
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
          Complete all steps to apply for a teaching position at our school
        </CardDescription>
        <CardDescription className="space-y-8 text-center">
          <Stepper value={currentStep} onValueChange={setCurrentStep}>
            {steps.map(({ step, title, description }) => (
              <StepperItem key={step} step={step} className="relative flex-1">
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
                {step < steps.length && <StepperSeparator />}
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
