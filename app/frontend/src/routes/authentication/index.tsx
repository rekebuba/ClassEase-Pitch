import { createFileRoute, Link, redirect } from "@tanstack/react-router";
import { GraduationCap } from "lucide-react";

import AuthActionBar from "@/components/authentication/auth-action-bar";
import { store } from "@/store/main-store";

export const Route = createFileRoute("/authentication/")({
  component: AuthPage,
  beforeLoad: async () => {
    const state = store.getState();
    const { token, userInfo } = state.auth;
    if (token && userInfo) {
      throw redirect({
        to: `/${userInfo.role}`,
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
        <AuthActionBar />
      </div>
    </div>
  );
}
