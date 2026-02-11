import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { ChevronLeftIcon, GraduationCap, Loader2Icon } from "lucide-react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { passwordRecoveryMutation, verifyOtpMutation } from "@/client/@tanstack/react-query.gen";
import { zOtpRequest, zPasswordRecovery } from "@/client/zod.gen";
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
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot,
} from "@/components/ui/input-otp";
import { Tabs, TabsContent, TabsList } from "@/components/ui/tabs";

import type { OtpRequest, PasswordRecovery, PasswordRecoveryError, VerifyOtpError } from "@/client/types.gen";
import type { AxiosError } from "axios";

export const Route = createFileRoute("/forgot-password/")({
  component: RouteComponent,
});

function RouteComponent() {
  const [activeTab, setActiveTab] = useState("send-otp");
  const navigate = useNavigate();

  const recoveryForm = useForm<PasswordRecovery>({
    resolver: zodResolver(zPasswordRecovery),
    defaultValues: {
      email: "",
    },
  });

  const {
    formState: { errors: recoveryErrors },
  } = recoveryForm;

  const otpForm = useForm<OtpRequest>({
    resolver: zodResolver(zOtpRequest),
    defaultValues: {
      email: "",
      otp: "",
    },
  });

  const {
    formState: { errors: otpErrors },
  } = otpForm;

  const otpMutation = useMutation({
    ...verifyOtpMutation(),
    onSuccess: (response) => {
      navigate({ to: `/forgot-password/${response.token}`, search: { email: otpForm.getValues("email") } });
    },
    onError: (error: AxiosError<VerifyOtpError>) => {
      const detail = error.response?.data?.detail;
      if (detail && typeof detail === "string") {
        otpForm.setError("root", { message: detail });
      }
      else {
        toast.error("Something went wrong. Failed to verify OTP.", {
          style: { color: "red" },
        });
      }
    },
  });

  const recoveryMutation = useMutation({
    ...passwordRecoveryMutation(),
    onSuccess: () => {
      toast.success("Password reset email sent. Please check your inbox.");
      setActiveTab("verify-otp");
      otpForm.setValue("email", recoveryForm.getValues("email"));
    },
    onError: (error: AxiosError<PasswordRecoveryError>) => {
      const detail = error.response?.data?.detail;
      if (detail && typeof detail === "string") {
        recoveryForm.setError("root", { message: detail });
      }
      else {
        toast.error("Something went wrong. Failed to send password reset email.", {
          style: { color: "red" },
        });
      }
    },
  });

  async function onSubmit(values: PasswordRecovery) {
    recoveryMutation.mutate({
      body: values,
    });
  }

  async function onSubmitOtp(values: OtpRequest) {
    otpMutation.mutate({
      body: values,
    });
  }

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab}>
      <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
        <div className="flex w-full max-w-lg flex-col gap-6">
          <TabsList>
          </TabsList>
          <TabsContent value="send-otp" id="send-otp">
            <Card className="mx-auto max-w-lg">
              <CardHeader>
                <Link to="/" className="flex items-center gap-2 self-center font-sm text-2xl">
                  <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
                    <GraduationCap className="size-4" />
                  </div>
                  ClassEase
                </Link>
                <CardTitle className="text-2xl">Forgot Password</CardTitle>
                <CardDescription>
                  Enter your email address to receive a password recovery code.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Form {...recoveryForm}>
                  <form onSubmit={recoveryForm.handleSubmit(onSubmit)} className="space-y-8">
                    <div className="grid gap-4">
                      {/* Email Field */}
                      <InputWithLabel<PasswordRecovery>
                        id="email"
                        fieldTitle="Email"
                        nameInSchema="email"
                        placeholder="Enter your email address"
                        required
                      />
                      {recoveryErrors.root && (
                        <div className="text-sm text-red-500 text-center">
                          {recoveryErrors.root.message}
                        </div>
                      )}
                      <Button
                        type="submit"
                        className="w-full"
                        disabled={recoveryMutation.isPending}
                      >
                        {recoveryMutation.isPending && <Loader2Icon className="animate-spin" />}
                        {recoveryMutation.isPending ? "Sending..." : "Send Reset Code"}
                      </Button>
                      <Link to="/authentication" className="group mx-auto flex w-fit items-center gap-2">
                        <ChevronLeftIcon className="size-5 transition-transform duration-200 group-hover:-translate-x-0.5" />
                        <span>Back to login</span>
                      </Link>
                    </div>
                  </form>
                </Form>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="verify-otp" id="verify-otp">
            <Card className="mx-auto max-w-lg">
              <CardHeader>
                <Link to="/" className="flex items-center gap-2 self-center font-sm text-2xl">
                  <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
                    <GraduationCap className="size-4" />
                  </div>
                  ClassEase
                </Link>
                <CardTitle className="text-2xl">Enter Verification Code</CardTitle>
                <CardDescription>
                  <Input
                    id="email"
                    type="email"
                    value={otpForm.getValues("email")}
                    disabled
                    className="mb-2"
                  />
                  Enter the verification code sent to your email address.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Form {...otpForm}>
                  <form onSubmit={otpForm.handleSubmit(onSubmitOtp)} className="space-y-8">
                    <div className="grid gap-4">
                      <FormField
                        control={otpForm.control}
                        name="otp"
                        render={({ field }) => (
                          <FormItem className="grid gap-2 justify-center">
                            <FormControl>
                              {/* Spread 'field' here to connect it to the form state */}
                              <InputOTP maxLength={6} {...field} className="justify-center" autoFocus>
                                <InputOTPGroup>
                                  <InputOTPSlot index={0} />
                                  <InputOTPSlot index={1} />
                                  <InputOTPSlot index={2} />
                                </InputOTPGroup>
                                <InputOTPSeparator />
                                <InputOTPGroup>
                                  <InputOTPSlot index={3} />
                                  <InputOTPSlot index={4} />
                                  <InputOTPSlot index={5} />
                                </InputOTPGroup>
                              </InputOTP>
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      {otpErrors.root && (
                        <div className="text-sm text-red-500 text-center">
                          {otpErrors.root.message}
                        </div>
                      )}
                      <Button type="submit" className="w-full">
                        Verify Code
                      </Button>
                      <Link to="/authentication" className="group mx-auto flex w-fit items-center gap-2">
                        <ChevronLeftIcon className="size-5 transition-transform duration-200 group-hover:-translate-x-0.5" />
                        <span>Back to login</span>
                      </Link>
                    </div>
                  </form>
                </Form>
              </CardContent>
            </Card>
          </TabsContent>
        </div>
      </div>
    </Tabs>
  );
}
