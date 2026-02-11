import { client } from "@/client/client.gen";
import { router } from "@/main";
import { store } from "@/store/main-store";
import { loginFailure } from "@/store/slice/auth-slice";
import { ENV } from "@/utils/utils";

// Create a new client with auth configuration
client.setConfig({
  auth: () => store.getState().auth.token || "",
  baseURL: ENV.API_BASE_URL,
});

client.instance.interceptors.response.use(
  response => response,
  (error) => {
    const status = error.response?.status;
    const state = store.getState();
    const isLoggedIn = !!state.auth.token;

    if (status === 401 && isLoggedIn) {
      store.dispatch(loginFailure("Session expired"));
      router.navigate({ to: "/authentication" });
    }

    return Promise.reject(error);
  },
);

// Export the original client from the SDK
export { client } from "@/client/client.gen";
