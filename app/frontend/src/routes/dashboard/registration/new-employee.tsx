import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Loader, RefreshCcw, Save } from "lucide-react";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

import {
  employeeMutation,
} from "@/client/@tanstack/react-query.gen";
import {
  zEmployeeProfile,
} from "@/client/zod.gen";
import AdvanceTooltip from "@/components/advance-tooltip";
import { DateWithLabel } from "@/components/inputs/date-labeled";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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
} from "@/store/slice/employee-registration-slice";

import type {
  EmployeeProfile,
} from "@/client/types.gen";

const steps = [
  { step: 1, title: "Step One", description: "Personal Information" },
  { step: 2, title: "Step Two", description: "Contact Information" },
  { step: 3, title: "Step Three", description: "Educational Background" },
  { step: 4, title: "Step Four", description: "Teaching & Experience" },
  { step: 5, title: "Step Five", description: "Background & References" },
];

export const Route = createFileRoute("/dashboard/registration/new-employee")({
  beforeLoad: () => requireRoutePermission(Permission["employees:write"]),
  component: RouteComponent,
});

function RouteComponent() {
  const { data: initialData, step } = store.getState().employeeRegistrationForm;
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [currentStep, setCurrentStep] = useState(step);
  const [savePending, setSavePending] = useState(false);
  const [resetPending, setResetPending] = useState(false);

  // const { data: subjects } = useQuery(getSubjectsOptions());

  const form = useForm<EmployeeProfile>({
    resolver: zodResolver(zEmployeeProfile),
    defaultValues: initialData,
  });

  const { reset, setError } = form;

  const mutation = useMutation({
    ...employeeMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      navigate({
        to: "/dashboard/registration/employees",
      });
      dispatch(resetForm());
      reset(initialData);
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          setError(field as keyof EmployeeProfile, {
            type: "server",
            message: message as string,
          });
        });
      }
      else {
        toast.error("Something went wrong. Failed to Register Employee.");
      }
    },
  });

  const onSubmit = form.handleSubmit(data =>
    mutation.mutate({ body: data }),
  );

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
                Please provide your basic personal details. Fields marked with *
                are required.
              </p>
            </div>
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <InputWithLabel<EmployeeProfile>
                  nameInSchema="userId"
                  fieldTitle="User ID *"
                  placeholder="Enter User ID"
                />
                <InputWithLabel<EmployeeProfile>
                  nameInSchema="employeeNumber"
                  fieldTitle="Employee Number *"
                  placeholder="Enter Employee Number"
                />
                <InputWithLabel<EmployeeProfile>
                  nameInSchema="employmentStatus"
                  fieldTitle="Employment Status *"
                  placeholder="Enter Employment Status"
                />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <DateWithLabel<EmployeeProfile>
                  nameInSchema="hireDate"
                  fieldTitle="Hire Date *"
                  placeholder="Select hire date"
                />
                <InputWithLabel<EmployeeProfile>
                  nameInSchema="employmentType"
                  fieldTitle="Employment Type *"
                  placeholder="Enter Employment Type"
                />
              </div>
            </div>
            <div className="flex justify-between mt-8 pt-6 border-t">
              <Button
                type="submit"
                onClick={onSubmit}
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
            Employee Registration Form
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
              form.reset(initialData);
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
