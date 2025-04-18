import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Toaster } from "sonner";
import RootLayout from "./RootLayout";
import App from "./App";
import { NuqsAdapter } from 'nuqs/adapters/react';

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RootLayout>
      <NuqsAdapter>
        <App />
      </NuqsAdapter>
      <Toaster />
    </RootLayout>
  </StrictMode>
);
