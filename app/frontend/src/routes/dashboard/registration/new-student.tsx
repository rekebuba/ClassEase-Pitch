import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Loader, RefreshCcw, Save } from "lucide-react";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

import {
  getGradesOptions,
  studentMutation,
} from "@/client/@tanstack/react-query.gen";
import { zStudentProfile } from "@/client/zod.gen";
import AdvanceTooltip from "@/components/advance-tooltip";
import { InputWithLabel } from "@/components/inputs/input-labeled";
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
import {
  Stepper,
  StepperDescription,
  StepperIndicator,
  StepperItem,
  StepperSeparator,
  StepperTitle,
  StepperTrigger,
} from "@/components/ui/stepper";
import { requireRoutePermission } from "@/lib/auth/route-guards";
import { Permission } from "@/lib/permissions";
import { store } from "@/store/main-store";
import {
  resetForm,
  setFormData,
  setFormStep,
} from "@/store/slice/student-registration-slice";

import type {
  StudentProfile,
} from "@/client/types.gen";

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

export const Route = createFileRoute("/dashboard/registration/new-student")({
  beforeLoad: () => requireRoutePermission(Permission["students:write"]),
  component: RouteComponent,
});

function RouteComponent() {
  const { data: initialData, step } = store.getState().studentRegistrationForm;
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [currentStep, setCurrentStep] = useState(step);
  const [savePending, setSavePending] = useState(false);
  const [resetPending, setResetPending] = useState(false);

  const form = useForm<StudentProfile>({
    resolver: zodResolver(zStudentProfile),
    defaultValues: initialData,
  });

  const { reset, setError } = form;

  const { data: grades } = useQuery({
    ...getGradesOptions(),
  });

  const mutation = useMutation({
    ...studentMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      dispatch(resetForm());
      reset(initialData);
      navigate({
        to: "/dashboard/registration/students",
      });
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          setError(field as keyof StudentProfile, {
            type: "server",
            message: message as string,
          });
        });
      }
      else {
        toast.error("Something went wrong. Failed to Register Student.");
      }
    },
  });

  const handleSave = () => {
    mutation.mutate({ body: form.getValues() });
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <FormProvider {...form}>
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
                <InputWithLabel<StudentProfile>
                  nameInSchema="userId"
                  fieldTitle="User ID *"
                  placeholder="Enter User ID"
                  description="Unique identifier for the student"
                />
                <SelectWithLabel<StudentProfile, string>
                  fieldTitle="Grade Level *"
                  nameInSchema="userId" // replace with registeredForGradeId
                  description="Select the grade the student will be entering"
                >
                  {grades?.map(grade => (
                    <SelectItem key={grade.id} value={grade.id}>
                      Grade
                      {" "}
                      {grade.grade}
                    </SelectItem>
                  ))}
                </SelectWithLabel>
              </div>
            </div>
            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button variant="outline" disabled={true} className="px-8">
                Previous
              </Button>
              <Button
                type="submit"
                onClick={handleSave}
                disabled={mutation.isPending}
                className="px-8"
              >
                {mutation.isPending && <Loader className="animate-spin" />}
                Next Step
              </Button>
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
                  ...form.getValues(),
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
