import { createFileRoute, Link, Outlet, redirect } from "@tanstack/react-router";
import { GraduationCap } from "lucide-react";

import { store } from "@/store/main-store";

export const Route = createFileRoute("/auth")({
  component: AuthPage,
  beforeLoad: async () => {
    const state = store.getState();
    const { token, activeMembership } = state.auth;

    if (token && (activeMembership)) {
      throw redirect({
        to: "/dashboard",
      });
    }
  },
});

export default function AuthPage() {
  return (
    <div className="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
      <div className="flex w-full max-w-lg flex-col gap-6">
        <Link to="/" className="flex items-center gap-2 self-center font-medium">
          <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
            <GraduationCap className="size-4" />
          </div>
          ClassEase
        </Link>
        
        <Outlet />
      </div>
    </div>
  );
}
