import {
  getGradesOptions,
  registerNewStudentMutation,
} from "@/client/@tanstack/react-query.gen";
import { StudentRegistrationForm } from "@/client/types.gen";
import { zBloodTypeEnum, zStudentRegistrationForm } from "@/client/zod.gen";
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled";
import { DateWithLabel } from "@/components/inputs/date-labeled";
import { InputWithLabel } from "@/components/inputs/input-labeled";
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
  transportation: undefined,
  siblingInSchool: false,
  siblingDetails: "",
};

const stepNames = {
  1: "Personal Information",
  2: "Academic Information",
  3: "Address & Contact",
  4: "Guardian & Emergency Contact",
  5: "Medical Information",
  6: "Additional Information & Review",
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
  {
    step: 6,
    title: "Step Six",
    description: "Additional Information & Review",
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
  const {
    formState: { isDirty },
    reset,
    watch,
    handleSubmit,
    setError,
  } = form;

  const watchForm = watch();

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

  const onValid: SubmitHandler<StudentRegistrationForm> = (data) => {
    mutation.mutate({ body: data });
  };
  const handleSave = handleSubmit(onValid);

  const handleCancel = useCallback(() => {
    navigate({
      to: "/admin/registration/student",
    });
  }, [navigate]);

  const totalSteps = 6;

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="firstName"
                fieldTitle="First Name"
                placeholder="Enter First Name"
              />

              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="fatherName"
                fieldTitle="Father Name"
                placeholder="Enter Father Name"
              />
              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="grandFatherName"
                fieldTitle="Grandfather Name"
                placeholder="Enter Father Name"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <DateWithLabel<StudentRegistrationForm>
                nameInSchema="dateOfBirth"
                fieldTitle="Date of Birth"
                placeholder="Select date of birth"
              />
              <div className="space-y-2 w-[200px]">
                <RadioGroupLabel<
                  StudentRegistrationForm,
                  StudentRegistrationForm["gender"]
                >
                  fieldTitle="Gender *"
                  nameInSchema="gender"
                  options={[
                    { label: "male", value: "male" },
                    { label: "female", value: "female" },
                  ]}
                />
              </div>
              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="nationality"
                fieldTitle="Nationality"
                placeholder="Enter Nationality"
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
              </div>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <SelectWithLabel<StudentRegistrationForm, string>
                fieldTitle="Grade Level *"
                nameInSchema="registeredForGradeId"
              >
                {grades?.map((grade) => (
                  <SelectItem key={grade.id} value={grade.id}>
                    {grade.grade}
                  </SelectItem>
                ))}
              </SelectWithLabel>

              <SelectWithLabel<StudentRegistrationForm, string>
                fieldTitle="Transportation Method"
                nameInSchema="transportation"
              >
                <SelectItem value="school-bus">School Bus</SelectItem>
                <SelectItem value="parent-drop">Parent Drop-off</SelectItem>
                <SelectItem value="walk">Walking</SelectItem>
                <SelectItem value="bicycle">Bicycle</SelectItem>
                <SelectItem value="other">Other</SelectItem>
              </SelectWithLabel>
            </div>

            <div className="space-y-4">
              <CheckboxWithLabel<StudentRegistrationForm, boolean>
                nameInSchema="isTransfer"
                fieldTitle="Is the student transferring from another school?"
              />

              {watchForm.isTransfer && (
                <InputWithLabel<StudentRegistrationForm>
                  nameInSchema="previousSchool"
                  fieldTitle="Previous School Name"
                  placeholder="Enter previous school name"
                />
              )}
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="address"
                fieldTitle="Street Address"
                placeholder="Enter street address"
              />

              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="city"
                fieldTitle="City"
                placeholder="Enter city"
              />
              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="state"
                fieldTitle="State/Province"
                placeholder="Enter state or province"
              />
            </div>

            <Separator />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="fatherPhone"
                fieldTitle="Father's Phone Number"
              />
              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="motherPhone"
                fieldTitle="Mother's Phone Number"
              />
            </div>

            <InputWithLabel<StudentRegistrationForm>
              nameInSchema="parentEmail"
              fieldTitle="Parent/Guardian Email"
            />
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InputWithLabel<StudentRegistrationForm>
                nameInSchema="guardianName"
                fieldTitle="Guardian Name"
                placeholder="Enter guardian name"
              />

              <SelectWithLabel<StudentRegistrationForm, string>
                fieldTitle="Select relationship"
                nameInSchema="guardianRelation"
              >
                <SelectItem value="parent">Parent</SelectItem>
                <SelectItem value="grandparent">Grandparent</SelectItem>
                <SelectItem value="aunt-uncle">Aunt/Uncle</SelectItem>
                <SelectItem value="sibling">Sibling</SelectItem>
                <SelectItem value="family-friend">Family Friend</SelectItem>
                <SelectItem value="other">Other</SelectItem>
              </SelectWithLabel>
            </div>

            <InputWithLabel<StudentRegistrationForm>
              nameInSchema="guardianPhone"
              fieldTitle="Guardian Phone Number"
              placeholder="+251 9/7xx-xxx-xxx"
            />

            <Separator />

            <div className="space-y-4">
              <h4 className="font-medium text-red-600">
                Emergency Contact (if different from above)
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InputWithLabel<StudentRegistrationForm>
                  nameInSchema="emergencyContactName"
                  fieldTitle="Emergency Contact Name"
                  placeholder="Enter emergency contact name"
                />
                <InputWithLabel<StudentRegistrationForm>
                  nameInSchema="emergencyContactPhone"
                  fieldTitle="Emergency Contact Phone"
                  placeholder="+251/7xx-xxx-xxx"
                />
              </div>
            </div>

            <Separator />

            <div className="space-y-4">
              <CheckboxWithLabel<StudentRegistrationForm, boolean>
                nameInSchema="siblingInSchool"
                fieldTitle="Does the student have siblings currently enrolled in this school?"
              />

              {watchForm.siblingInSchool && (
                <div className="ml-6 space-y-2 p-4 bg-gray-50 rounded-lg">
                  <InputWithLabel<StudentRegistrationForm>
                    nameInSchema="siblingDetails"
                    fieldTitle="Sibling Information"
                    placeholder="Please provide names and grades of siblings currently enrolled"
                  />
                </div>
              )}
            </div>
          </div>
        );

      case 5:
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <SelectWithLabel<
                StudentRegistrationForm,
                StudentRegistrationForm["bloodType"]
              >
                fieldTitle="Select blood type"
                nameInSchema="nationality"
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

              {watchForm.hasMedicalCondition && (
                <div className="ml-6 space-y-2 p-4 bg-red-50 rounded-lg">
                  <InputWithLabel<StudentRegistrationForm>
                    nameInSchema="medicalDetails"
                    fieldTitle="Medical Condition Details"
                    placeholder="Please describe the medical condition and any required care"
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

              {watchForm.hasDisability && (
                <div className="ml-6 space-y-2 p-4 bg-blue-50 rounded-lg">
                  <InputWithLabel<StudentRegistrationForm>
                    nameInSchema="disabilityDetails"
                    fieldTitle="Disability Details"
                    placeholder="Please describe the disability and any support needed"
                  />
                </div>
              )}
            </div>
          </div>
        );

      case 6:
        return (
          <div className="space-y-6">
            <div className="space-y-4">
              <h4 className="font-medium">Registration Summary</h4>
              <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                <p>
                  <strong>Student:</strong> {watchForm.firstName}
                  {watchForm.fatherName}
                  {watchForm.grandFatherName}
                </p>
                <p>
                  <strong>Grade:</strong> {watchForm.firstName}
                </p>
                <p>
                  <strong>Father:</strong> {watchForm.fatherName}
                </p>
                <p>
                  <strong>Contact:</strong> {watchForm.fatherPhone}
                </p>
                {watchForm.isTransfer && (
                  <p>
                    <strong>Transfer Student:</strong> Yes (from{" "}
                    {watchForm.previousSchool})
                  </p>
                )}
                {watchForm.hasMedicalCondition && (
                  <p>
                    <strong>Medical Condition:</strong> Yes
                  </p>
                )}
                {watchForm.hasDisability && (
                  <p>
                    <strong>Disability:</strong> Yes
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

        <FormProvider {...form}>
          <CardContent className="p-8">
            <div>
              <div className="flex gap-8">
                <div className="w-full">{renderStep()}</div>
              </div>
            </div>
            <div className="flex justify-between mt-8 pt-6 border-t">
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
            </div>
          </CardContent>
        </FormProvider>
      </Card>
    </>
  );
}
