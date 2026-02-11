import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { ChevronLeftIcon, Loader2Icon } from "lucide-react";
import { FormProvider, useForm } from "react-hook-form";
import { toast } from "sonner";
import z from "zod";

import { passwordResetMutation } from "@/client/@tanstack/react-query.gen";
import { zPasswordResetRequest } from "@/client/zod.gen";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Field,
    FieldGroup,
    FieldSeparator,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";

import type { PasswordResetError, PasswordResetRequest } from "@/client/types.gen";
import type { AxiosError } from "axios";

const searchSchema = z.object({
  email: z.email(),
});

export const Route = createFileRoute("/forgot-password/$token/")({
  component: RouteComponent,
  validateSearch: searchSchema,
});

function RouteComponent() {
  const token = Route.useParams().token;
  const email = Route.useSearch().email;
  const navigate = useNavigate();

  const form = useForm<PasswordResetRequest>({
    resolver: zodResolver(zPasswordResetRequest.refine(data => data.newPassword === data.confirmPassword, {
      message: "Passwords do not match",
      path: ["confirmPassword"], // This sets the error on the confirmPassword field
    })),
    defaultValues: {
      email: email || "",
      token: token || "",
      newPassword: "",
      confirmPassword: "",
    },
  });

  const {
    setError,
    formState: { errors },
    handleSubmit,
  } = form;

  const mutation = useMutation({
    ...passwordResetMutation(),
    onSuccess: (response) => {
      toast.success(response.message, {
        style: { color: "green" },
      });
      navigate({ to: "/authentication" });
    },
    onError: (error: AxiosError<PasswordResetError>) => {
      const detail = error.response?.data?.detail;
      if (detail && typeof detail === "string") {
        setError("root", { message: detail });
      }
      else {
        toast.error("Something went wrong. Failed to reset password.", {
          style: { color: "red" },
        });
      }
    },
  });

  async function onSubmit(values: PasswordResetRequest) {
    mutation.mutate({ body: values });
  };

  return (
    <div className="relative flex h-auto min-h-screen items-center justify-center overflow-x-hidden px-4 py-10 sm:px-6 lg:px-8">
      <Card className="z-1 w-full border-none shadow-md sm:max-w-md">
        <CardHeader className="gap-6">
          <div>
            <CardTitle className="mb-1.5 text-2xl">Reset Password</CardTitle>
            <CardDescription className="text-base">
              Please Enter your new password and confirm it to reset your password.
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          {/* ResetPassword Form */}
          <FormProvider {...form}>
            <form onSubmit={handleSubmit(onSubmit)}>
              <FieldGroup>
                <Field>
                  <Input
                    id="email"
                    type="email"
                    value={form.getValues("email")}
                    disabled
                    className="cursor-not-allowed bg-muted mb-2"
                  />
                  <FieldSeparator>New Credential</FieldSeparator>
                </Field>
                <Field>
                  <InputWithLabel<PasswordResetRequest>
                    id="password"
                    type="password"
                    fieldTitle="New Password"
                    nameInSchema="newPassword"
                    placeholder="Enter your new password"
                    required
                  />
                  <InputWithLabel<PasswordResetRequest>
                    id="password"
                    type="password"
                    fieldTitle="Confirm New Password"
                    nameInSchema="confirmPassword"
                    placeholder="Confirm your new password"
                    required
                  />
                </Field>
                {errors.root && (
                  <Field>
                    <div className="text-sm text-red-500 text-center">
                      {errors.root.message}
                    </div>
                  </Field>
                )}
                <Field>
                  <Button
                    type="submit"
                    className="w-full"
                    disabled={mutation.isPending}
                  >
                    {mutation.isPending && <Loader2Icon className="animate-spin" />}
                    {mutation.isPending ? "Resetting..." : "Reset Password"}
                  </Button>
                </Field>
              </FieldGroup>
            </form>
          </FormProvider>

          <Link to="/authentication" className="group mx-auto flex w-fit items-center gap-2">
            <ChevronLeftIcon className="size-5 transition-transform duration-200 group-hover:-translate-x-0.5" />
            <span>Back to login</span>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}
