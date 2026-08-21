import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { Link, useNavigate } from "@tanstack/react-router";
import { Loader2Icon } from "lucide-react";
import { FormProvider, useForm } from "react-hook-form";
import { toast } from "sonner";

import { signupMutation } from "@/client/@tanstack/react-query.gen";
import { zSignUpRequest } from "@/client/zod.gen";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Field, FieldDescription, FieldGroup } from "@/components/ui/field";
import { SelectItem } from "@/components/ui/select";

import type { SignupError, SignUpRequest } from "@/client/types.gen";
import type { AxiosError } from "axios";
import type { SubmitHandler } from "react-hook-form";

export default function SignupTab() {
  const navigate = useNavigate();
  const form = useForm<SignUpRequest>({
    resolver: zodResolver(zSignUpRequest),
    defaultValues: {
      firstName: "",
      fatherName: "",
      grandFatherName: null,
      email: "",
      phone: null,
      dateOfBirth: "",
      username: "",
      password: "",
    },
  });

  const {
    handleSubmit,
    setError,
    formState: { errors },
  } = form;

  const mutation = useMutation({
    ...signupMutation(),
    onSuccess: () => {
      toast.success("Account created. You can sign in now.");
      navigate({ to: "/auth/sign-in" });
    },
    onError: (error: AxiosError<SignupError>) => {
      const detail = error.response?.data?.detail;
      if (typeof detail === "string") {
        setError("root", { message: detail });
        return;
      }

      setError("root", {
        message: "Something went wrong. Failed to create your account.",
      });
    },
  });

  const submitSignup: SubmitHandler<SignUpRequest> = (data) => {
    mutation.mutate({
      body: {
        ...data,
        grandFatherName: null,
        phone: null,
      },
    });
  };

  return (
    <Card className="border-0 shadow-lg animate-fade-left">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold text-center">
          Create an account
        </CardTitle>
        <CardDescription className="text-center">
          Enter the required details to create your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <FormProvider {...form}>
          <form onSubmit={handleSubmit(submitSignup)}>
            <FieldGroup>
              <div className="grid gap-4 sm:grid-cols-2">
                <Field>
                  <InputWithLabel<SignUpRequest>
                    id="firstName"
                    fieldTitle="First Name"
                    nameInSchema="firstName"
                    placeholder="Enter first name"
                    required
                  />
                </Field>
                <Field>
                  <InputWithLabel<SignUpRequest>
                    id="fatherName"
                    fieldTitle="Father Name"
                    nameInSchema="fatherName"
                    placeholder="Enter father name"
                    required
                  />
                </Field>
              </div>
              <Field>
                <InputWithLabel<SignUpRequest>
                  id="email"
                  type="email"
                  fieldTitle="Email"
                  nameInSchema="email"
                  placeholder="name@example.com"
                  required
                />
              </Field>
              <div className="grid gap-4 sm:grid-cols-2">
                <Field>
                  <InputWithLabel<SignUpRequest>
                    id="dateOfBirth"
                    type="date"
                    fieldTitle="Date of Birth"
                    nameInSchema="dateOfBirth"
                    required
                  />
                </Field>
                <Field>
                  <SelectWithLabel<SignUpRequest, SignUpRequest["gender"]>
                    fieldTitle="Gender"
                    nameInSchema="gender"
                    placeholder="Select gender"
                  >
                    <SelectItem value="male">Male</SelectItem>
                    <SelectItem value="female">Female</SelectItem>
                  </SelectWithLabel>
                </Field>
              </div>
              <Field>
                <InputWithLabel<SignUpRequest>
                  id="username"
                  fieldTitle="Username"
                  nameInSchema="username"
                  placeholder="Choose a username"
                  required
                />
              </Field>
              <Field>
                <InputWithLabel<SignUpRequest>
                  id="password"
                  type="password"
                  fieldTitle="Password"
                  nameInSchema="password"
                  placeholder="Create a password"
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
                  {mutation.isPending ? "Creating account..." : "Create account"}
                </Button>
              </Field>
              <FieldDescription className="text-center">
                Already have an account?
                {" "}
                <Link
                  to="/auth/sign-in"
                  className="underline underline-offset-4 hover:text-primary"
                >
                  Sign in
                </Link>
              </FieldDescription>
            </FieldGroup>
          </form>
        </FormProvider>
      </CardContent>
      <CardFooter className="flex flex-col">
        <p className="mt-2 text-xs text-center text-muted-foreground">
          By creating an account, you agree to our
          {" "}
          <a className="underline underline-offset-4 hover:text-primary">
            Terms of Service
          </a>
          {" "}
          and
          {" "}
          <a className="underline underline-offset-4 hover:text-primary">
            Privacy Policy
          </a>
          .
        </p>
      </CardFooter>
    </Card>
  );
}
