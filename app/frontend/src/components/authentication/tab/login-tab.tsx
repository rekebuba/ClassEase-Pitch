import { zodResolver } from "@hookform/resolvers/zod/dist/zod";
import { useMutation } from "@tanstack/react-query";
import { Link } from "@tanstack/react-router";
import { Loader2Icon } from "lucide-react";
import { FormProvider, useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

import { loginMutation } from "@/client/@tanstack/react-query.gen";
import { zBodyLoginCredential } from "@/client/zod.gen";
import GoogleAuth from "@/components/authentication/google-auth";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";
import { loginFailure } from "@/store/slice/auth-slice";

import type {
  BodyLoginCredential,
  LoginError,
  LoginResponse,
} from "@/client/types.gen";
import type { AxiosError } from "axios";
import type { SubmitHandler } from "react-hook-form";

type LoginTabProps = {
  onAuthResponse: (response: LoginResponse) => void;
};

export default function LoginTab({ onAuthResponse }: LoginTabProps) {
  const form = useForm<BodyLoginCredential>({
    resolver: zodResolver(zBodyLoginCredential),
    defaultValues: {
      username: "",
      password: "",
      schoolSlug: "",
      grant_type: "password",
      scope: "",
    },
  });

  const {
    setError,
    watch,
    formState: { errors },
    handleSubmit,
  } = form;

  const dispatch = useDispatch();

  const mutation = useMutation({
    ...loginMutation(),
    onSuccess: (response) => {
      onAuthResponse(response);
    },
    onError: (error: AxiosError<LoginError>) => {
      const detail = error.response?.data?.detail;
      if (detail && typeof detail === "string") {
        setError("root", { message: detail });
        dispatch(loginFailure(detail));
      }
      else {
        dispatch(loginFailure("Something went wrong. Failed to Login."));
        toast.error("Something went wrong. Failed to Login.", {
          style: { color: "red" },
        });
      }
    },
  });

  const submitLogin: SubmitHandler<BodyLoginCredential> = (data) => {
    mutation.mutate({
      body: {
        ...data,
        grant_type: data.grant_type || "password",
      },
    });
  };

  return (
    <Card className="border-0 shadow-lg animate-fade-left">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold text-center">
          Welcome back
        </CardTitle>
        <CardDescription className="text-center">
          Enter your credentials to access your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <FormProvider {...form}>
          <form onSubmit={handleSubmit(submitLogin)}>
            <FieldGroup>
              <Field>
                <InputWithLabel<BodyLoginCredential>
                  id="username"
                  fieldTitle="Username/ID"
                  nameInSchema="username"
                  placeholder="Enter your username or ID"
                  required
                />
              </Field>
              <Field>
                <InputWithLabel<BodyLoginCredential>
                  id="schoolSlug"
                  fieldTitle="School Slug (Optional)"
                  nameInSchema="schoolSlug"
                  placeholder="Enter school slug if you belong to multiple schools"
                />
              </Field>
              <Field>
                <div className="flex items-center">
                  <FieldLabel htmlFor="password">Password</FieldLabel>
                  <Link to="/forgot-password" className="ml-auto text-sm underline-offset-4 hover:underline">
                    Forgot your password?
                  </Link>
                </div>
                <InputWithLabel<BodyLoginCredential>
                  id="password"
                  type="password"
                  nameInSchema="password"
                  placeholder="Enter your password"
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
                  {mutation.isPending ? "Logging in..." : "Log in"}
                </Button>
              </Field>
              <FieldSeparator>Or continue with</FieldSeparator>
              <GoogleAuth
                schoolSlug={watch("schoolSlug") || undefined}
                onAuthResponse={onAuthResponse}
              />
              <FieldDescription className="text-center">
                Use your school account credentials or Google to continue.
              </FieldDescription>
            </FieldGroup>
          </form>
        </FormProvider>
      </CardContent>

      <CardFooter className="flex flex-col">
        <p className="mt-2 text-xs text-center text-muted-foreground">
          By logging in, you agree to our
          {" "}
          <a
            className="underline underline-offset-4 hover:text-primary"
          >
            Terms of Service
          </a>
          {" "}
          and
          {" "}
          <a
            className="underline underline-offset-4 hover:text-primary"
          >
            Privacy Policy
          </a>
          .
        </p>
      </CardFooter>
    </Card>
  );
}
