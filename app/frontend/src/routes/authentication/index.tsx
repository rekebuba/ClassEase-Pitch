import { AuthLayout } from "@/components";
import AuthActionBar from "@/components/authentication/auth-action-bar";
import { store } from "@/store/main-store";
import { createFileRoute, redirect } from "@tanstack/react-router";
import { GraduationCap } from "lucide-react";

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
    <AuthLayout>
      <div className="flex justify-center mb-8 lg:hidden">
        <div className="flex items-center gap-2">
          <GraduationCap className="h-8 w-8 text-sky-500" />
          <span className="text-2xl font-bold text-sky-500">ClassEase</span>
        </div>
      </div>

      <AuthActionBar />
    </AuthLayout>
  );
}
