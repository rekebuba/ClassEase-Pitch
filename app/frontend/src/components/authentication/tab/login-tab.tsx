import { loginMutation } from "@/client/@tanstack/react-query.gen";
import { LoginError } from "@/client/types.gen";
import { zBodyLoginCredential } from "@/client/zod.gen";
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
import { Checkbox } from "@/components/ui/checkbox";
import { decodeToken } from "@/context/auth-context";
import { BodyLoginCredential } from "@/store/api";
import { loginFailure, loginSuccess } from "@/store/slice/auth-slice";
import { zodResolver } from "@hookform/resolvers/zod/dist/zod";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { AxiosError } from "axios";
import { EyeIcon, EyeOffIcon, Loader2Icon } from "lucide-react";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

export default function LoginTab() {
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const form = useForm<BodyLoginCredential>({
    resolver: zodResolver(zBodyLoginCredential),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const {
    setError,
    formState: { errors },
  } = form;

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const mutation = useMutation({
    ...loginMutation(),
    onSuccess: (response) => {
      const decodedToken = decodeToken(response.accessToken);

      if (decodedToken === null) {
        dispatch(loginFailure("Invalid token received"));
        toast.error("Invalid token received", {
          style: { color: "red" },
        });
        return;
      }

      dispatch(
        loginSuccess({ token: response.accessToken, userInfo: decodedToken }),
      );

      const userRole = decodedToken.role;

      navigate({ to: `/${userRole}` });
    },
    onError: (error: AxiosError<LoginError>) => {
      const detail = error.response?.data?.detail;
      if (detail && typeof detail === "string") {
        setError("root", { message: detail });
        dispatch(loginFailure(detail));
      } else {
        dispatch(loginFailure("Something went wrong. Failed to Login."));
        toast.error("Something went wrong. Failed to Login.", {
          style: { color: "red" },
        });
      }
    },
  });

  const handleLogin = (
    loginForm: BodyLoginCredential,
    e?: React.BaseSyntheticEvent,
  ) => {
    e?.preventDefault();
    mutation.mutate({ body: loginForm });
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
          <form onSubmit={form.handleSubmit(handleLogin)}>
            <div className="grid gap-4">
              <div className="grid gap-2">
                <InputWithLabel<BodyLoginCredential>
                  id="username"
                  fieldTitle="Username/ID"
                  nameInSchema="username"
                  placeholder="Enter your username or ID"
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="relative">
                  <InputWithLabel<BodyLoginCredential>
                    id="password"
                    type={showPassword ? "text" : "password"}
                    fieldTitle="Password"
                    nameInSchema="password"
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-2/3 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                    aria-label={
                      showPassword ? "Hide password" : "Show password"
                    }
                  >
                    {showPassword ? (
                      <EyeOffIcon className="h-4 w-4" />
                    ) : (
                      <EyeIcon className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>
              <div className="flex justify-between">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="remember"
                    checked={rememberMe}
                    onCheckedChange={() => setRememberMe(!rememberMe)}
                  />
                  <label
                    htmlFor="remember"
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    Remember me
                  </label>
                </div>
                <button
                  type="button"
                  onClick={(e) => {
                    e.preventDefault();
                    // handle forgot password logic
                  }}
                  className="text-sm text-sky-500 hover:text-sky-600 bg-transparent border-none p-0"
                >
                  Forgot password?
                </button>
              </div>
              {errors.root && (
                <div className="text-sm text-red-500 text-center">
                  {errors.root.message}
                </div>
              )}
              <Button
                type="submit"
                className="w-full"
                disabled={mutation.isPending}
              >
                {mutation.isPending && <Loader2Icon className="animate-spin" />}
                {mutation.isPending ? "Logging in..." : "Log in"}
              </Button>
            </div>
          </form>
        </FormProvider>
      </CardContent>

      <CardFooter className="flex flex-col">
        <p className="mt-2 text-xs text-center text-muted-foreground">
          By logging in, you agree to our{" "}
          <a
            href="#"
            className="underline underline-offset-4 hover:text-primary"
          >
            Terms of Service
          </a>{" "}
          and{" "}
          <a
            href="#"
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
