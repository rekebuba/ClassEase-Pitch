import { GoogleLogin } from "@react-oauth/google";
import { useMutation } from "@tanstack/react-query";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

import { loginProviderMutation } from "@/client/@tanstack/react-query.gen";
import { loginFailure } from "@/store/slice/auth-slice";

import type {
  LoginProviderError,
  LoginResponse,
} from "@/client/types.gen";
import type { CredentialResponse } from "@react-oauth/google";
import type { AxiosError } from "axios";

type GoogleAuthProps = {
  schoolSlug?: string;
  onAuthResponse: (response: LoginResponse) => void;
};

function GoogleAuth({ schoolSlug, onAuthResponse }: GoogleAuthProps) {
  const dispatch = useDispatch();

  const mutation = useMutation({
    ...loginProviderMutation(),
    onSuccess: (response) => {
      onAuthResponse(response);
    },
    onError: (error: AxiosError<LoginProviderError>) => {
      const detail = error.response?.data?.detail;
      if (detail && typeof detail === "string") {
        toast.error(detail || "Something went wrong. Failed to login.", {
          style: { color: "red" },
        });
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

  const onSuccess = (credentialResponse: CredentialResponse) => {
    if (!credentialResponse.credential) {
      toast.error("Invalid Google credential");
      return;
    }

    mutation.mutate({
      body: {
        credential: credentialResponse.credential,
        school_slug: schoolSlug || undefined,
      },
      path: { provider: "google" },
    });
  };

  const onError = () => {
    toast.error("Login Failed. Please try again.", {
      style: { color: "red" },
    });
  };

  return (
    <div>
      <GoogleLogin onSuccess={onSuccess} onError={onError} useOneTap ux_mode="popup" />
    </div>
  );
}

export default GoogleAuth;
