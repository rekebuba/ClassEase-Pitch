import { useQuery } from "@tanstack/react-query";
import { redirect } from "@tanstack/react-router";

import { getLoggedInUserOptions } from "@/client/@tanstack/react-query.gen";
import { api } from "@/store/api";
import {
  clearError,
  loginFailure,
  loginSuccess,
} from "@/store/slice/auth-slice";

import { useAppDispatch, useAppSelector } from "./use-store";

import type { BodyLoginCredential } from "@/store/api";

function useAuth() {
  const dispatch = useAppDispatch();
  const { userRole, error } = useAppSelector(state => state.auth);

  // current logged-in user (only run if token exists)
  const {
    data: user,
    isLoading: isUserLoading,
    error: userError,
  } = useQuery(getLoggedInUserOptions());

  // mutations from RTK Query
  const [loginUser, { isLoading }] = api.useLoginMutation();

  // login
  const login = async (credentials: BodyLoginCredential) => {
    try {
      const response = await loginUser({
        bodyLoginCredential: credentials,
      }).unwrap();

      dispatch(loginSuccess({ token: response.access_token }));
      if (userRole) {
        throw redirect({ to: `/${userRole}` });
      }
    }
    catch (err: any) {
      dispatch(loginFailure(err.message || "Login failed"));
    }
  };

  // logout
  const logout = () => {
    localStorage.removeItem("access_token");
    throw redirect({ to: "/authentication" });
  };

  return {
    login,
    logout,
    isLoading,
    isUserLoading,
    userError,
    user,
    error,
    resetError: () => dispatch(clearError()),
  };
}

export default useAuth;
