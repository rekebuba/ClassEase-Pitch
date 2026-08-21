import { createFileRoute } from "@tanstack/react-router";

import SignupTab from "@/components/authentication/tab/signup-tab";

export const Route = createFileRoute("/auth/sign-up/")({
  component: RouteComponent,
});

function RouteComponent() {
  return <SignupTab />;
}
