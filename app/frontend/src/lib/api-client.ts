import { client } from "@/client/client.gen";
import { refreshAccessToken } from "@/client/sdk.gen";
import { queryClient } from "@/lib/query-client";
import { router } from "@/main";
import { persister, store } from "@/store/main-store";
import { loginSuccess, logout } from "@/store/slice/auth-slice";
import { decodeToken, ENV } from "@/utils/utils";

// Create a new client with auth configuration
client.setConfig({
  auth: () => store.getState().auth.token || "",
  baseURL: ENV.API_BASE_URL,
});

let isRefreshing = false;
let refreshQueue: Array<(token: string | null) => void> = [];

function resetAuthState() {
  queryClient.clear();
  persister.purge();
  store.dispatch(logout());
  router.navigate({ to: "/authentication" });
}

function drainRefreshQueue(token: string | null) {
  refreshQueue.forEach(resolve => resolve(token));
  refreshQueue = [];
}

client.instance.interceptors.response.use(
  response => response,
  async (error) => {
    const status = error.response?.status;
    const state = store.getState();
    const isLoggedIn = !!state.auth.token;
    const refreshToken = state.auth.refreshToken;
    const requestUrl = String(error.config?.url || "");
    const originalRequest = error.config as typeof error.config & { _retry?: boolean };

    if (!originalRequest) {
      return Promise.reject(error);
    }

    const shouldTryRefresh
      = status === 401
        && isLoggedIn
        && !!refreshToken
        && !originalRequest?._retry
        && !requestUrl.includes("/auth/refresh")
        && !requestUrl.includes("/auth/login")
        && !requestUrl.includes("/auth/login/");

    if (shouldTryRefresh && refreshToken) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          refreshQueue.push((newAccessToken) => {
            if (!newAccessToken) {
              reject(error);
              return;
            }
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            }
            resolve(client.instance(originalRequest));
          });
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const { data } = await refreshAccessToken({
          body: { refresh_token: refreshToken },
        });

        if (!data) {
          throw new Error("Data is Undefined");
        }

        const decoded = decodeToken(data.accessToken);
        if (!decoded) {
          throw new Error("Unable to decode refreshed access token");
        }

        store.dispatch(
          loginSuccess({
            token: data.accessToken,
            refreshToken: data.refreshToken,
            userInfo: decoded,
            activeSchool: data.activeSchool ?? null,
            activeMembership: data.activeMembership ?? null,
            availableMemberships: data.availableMemberships ?? [],
          }),
        );

        drainRefreshQueue(data.accessToken);

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${data.accessToken}`;
        }
        return client.instance(originalRequest);
      }
      catch (refreshError) {
        drainRefreshQueue(null);
        resetAuthState();
        return Promise.reject(refreshError);
      }
      finally {
        isRefreshing = false;
      }
    }

    if (status === 401 && isLoggedIn) {
      resetAuthState();
    }

    return Promise.reject(error);
  },
);

// Export the original client from the SDK
export { client } from "@/client/client.gen";
