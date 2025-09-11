import { loginMutation } from "@/client/@tanstack/react-query.gen";
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
import { BodyLoginCredential } from "@/store/api";
import { store } from "@/store/main-store";
import { loginFailure, loginSuccess } from "@/store/slice/auth-slice";
import { handleError } from "@/utils/utils";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { EyeIcon, EyeOffIcon, Loader2Icon } from "lucide-react";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useDispatch } from "react-redux";

type LoginRequest = BodyLoginCredential;

export default function LoginTab() {
  const [showPassword, setShowPassword] = useState(false);
  const form = useForm<LoginRequest>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const mutation = useMutation({
    ...loginMutation(),
    onSuccess: (response) => {
      // save token to redux
      dispatch(loginSuccess({ token: response.access_token }));

      const userRole = store.getState().auth.userInfo?.role;

      // redirect after success
      if (userRole) {
        navigate({ to: `/${userRole}` });
      }
    },
    onError: (error) => {
      const errorMessage = handleError(error);
      dispatch(loginFailure(errorMessage));
    },
  });

  const handleLogin = (loginForm: BodyLoginCredential) => {
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
                <InputWithLabel<LoginRequest>
                  id="id"
                  type="id"
                  fieldTitle="ID"
                  nameInSchema="username"
                  placeholder="XXX/XXX/XXXX"
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="relative">
                  <InputWithLabel<LoginRequest>
                    id="password"
                    type={showPassword ? "text" : "password"}
                    fieldTitle="Password"
                    nameInSchema="password"
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
                <div className="flex items-center justify-between">
                  <a
                    href="#"
                    className="text-sm text-sky-500 hover:text-sky-600"
                  >
                    Forgot password?
                  </a>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox id="remember" checked={false} />
                <label
                  htmlFor="remember"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  Remember me
                </label>
              </div>
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
