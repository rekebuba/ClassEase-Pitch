import { createFileRoute } from "@tanstack/react-router";

import AuthActionBar from "@/components/authentication/auth-action-bar";

export const Route = createFileRoute("/auth/sign-in/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div>
      <AuthActionBar />
    </div>
  );
}
