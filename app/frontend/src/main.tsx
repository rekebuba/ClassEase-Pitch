import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { NuqsAdapter } from "nuqs/adapters/react";
import { StrictMode, Suspense } from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";
import { RouterProvider } from "react-router-dom";
import { Toaster } from "sonner";
import "../src/globals.css";
import { LoadingSpinner } from "./components";
import RootLayout from "./RootLayout";
import router from "./routes/AppRoutes";
import { store } from "./store";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Provider store={store}>
      <QueryClientProvider client={queryClient}>
        <RootLayout>
          <NuqsAdapter>
            <Suspense fallback={<LoadingSpinner />}>
              <RouterProvider router={router} />
            </Suspense>
          </NuqsAdapter>
          <Toaster />
        </RootLayout>
      </QueryClientProvider>
    </Provider>
  </StrictMode>,
);
