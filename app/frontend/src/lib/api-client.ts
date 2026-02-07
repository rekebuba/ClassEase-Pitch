import { client } from "@/client/client.gen";
import { store } from "@/store/main-store";
import { loginFailure } from "@/store/slice/auth-slice";
import { getEnv } from "@/utils/utils";

const ENV = {
  API_BASE_URL: getEnv("VITE_API_BASE_URL"),
} as const;

// Create a new client with auth configuration
client.setConfig({
  auth: () => store.getState().auth.token || "",
  baseURL: ENV.API_BASE_URL,
});

client.instance.interceptors.response.use(
  response => response,
  (error) => {
    if (error.response?.status === 401) {
      // clear auth state, redirect, etc.
      store.dispatch(
        loginFailure(error.response?.data?.message || "Unauthorized"),
      );
      window.location.href = "/authentication";
    }
    return Promise.reject(error);
  },
);

// Export the original client from the SDK
export { client } from "@/client/client.gen";
