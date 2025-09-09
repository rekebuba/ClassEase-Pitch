import { AuthLayout } from "@/components";
import AuthActionBar from "@/components/authentication/auth-action-bar";
import { GraduationCap } from "lucide-react";

const AuthPage = () => {
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
};

export default AuthPage;
