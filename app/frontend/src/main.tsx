import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Toaster } from "sonner";
import RootLayout from "./RootLayout";
import App from "./App";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RootLayout>
      <App />
      <Toaster />
    </RootLayout>
  </StrictMode>
);
