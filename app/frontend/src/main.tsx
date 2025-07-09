import { StrictMode, Suspense } from "react";
import { createRoot } from "react-dom/client";
import { Toaster } from "sonner";
import RootLayout from "./RootLayout";
import { RouterProvider } from "react-router-dom";
import router from "./routes/AppRoutes";
import { NuqsAdapter } from 'nuqs/adapters/react';
import { LoadingSpinner } from "./components";
import '../src/globals.css';


createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RootLayout>
      <NuqsAdapter>
        <Suspense fallback={<LoadingSpinner />}>
          <RouterProvider router={router} />
        </Suspense>
      </NuqsAdapter>
      <Toaster />
    </RootLayout>
  </StrictMode>
);
