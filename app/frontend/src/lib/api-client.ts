import { client } from "@/client/client.gen";
import { store } from "@/store/main-store";
import { loginFailure } from "@/store/slice/auth-slice";

// Create a new client with auth configuration
client.setConfig({
  auth: () => store.getState().auth.token || "",
  baseURL: "http://localhost:8000",
});

client.instance.interceptors.response.use(
  (response) => response,
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
