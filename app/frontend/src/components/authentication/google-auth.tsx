import { GoogleLogin } from "@react-oauth/google";
import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { useDispatch } from "react-redux";
import { toast } from "sonner";

import { loginProviderMutation } from "@/client/@tanstack/react-query.gen";
import { loginFailure, loginSuccess } from "@/store/slice/auth-slice";
import { decodeToken } from "@/utils/utils";

import type { LoginError } from "@/client/types.gen";
import type { CredentialResponse } from "@react-oauth/google";
import type { AxiosError } from "axios";

function GoogleAuth() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const mutation = useMutation({
    ...loginProviderMutation(),
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
        toast.error(detail || "Something went wrong. Failed to Login.", {
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
      body: { credential: credentialResponse.credential },
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
