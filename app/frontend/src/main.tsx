import { QueryClientProvider } from "@tanstack/react-query";
import { createRouter, RouterProvider } from "@tanstack/react-router";
import { NuqsAdapter } from "nuqs/adapters/react";
import { StrictMode, Suspense } from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { Toaster } from "sonner";

import { queryClient } from "./lib/query-client";
import { routeTree } from "./routeTree.gen";
import { persister, store } from "./store/main-store";

import "../src/globals.css";

import "./lib/api-client";

// Create a new router instance
const router = createRouter({ routeTree });

// Register the router instance for type safety
declare module "@tanstack/react-router" {
  type Register = {
    router: typeof router;
  };
}

const rootElement = document.getElementById("root")!;
if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <StrictMode>
      <Provider store={store}>
        <PersistGate loading={null} persistor={persister}>
          <QueryClientProvider client={queryClient}>
            <NuqsAdapter>
              <Suspense fallback={<div />}>
                {/* <PageLoader /> */}
                <RouterProvider router={router} />
              </Suspense>
            </NuqsAdapter>
            <Toaster />
          </QueryClientProvider>
        </PersistGate>
      </Provider>
    </StrictMode>,
  );
}
