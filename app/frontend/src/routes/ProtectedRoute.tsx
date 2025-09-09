import { Header } from "@/components/Header";
import AdminSidebar from "@/components/layout/sidebar/admin-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import useAuth from "@/hooks/use-auth";
import { RoleType } from "@/lib/enums";
import { Navigate, Outlet } from "react-router-dom";

interface ProtectedRouteProps {
  allowedRoles?: RoleType[];
}
/**
 * This component checks if a JWT token is present in the local storage.
 * If the token is found, it renders the given component.
 * Otherwise, it redirects the user to the login page.
 */
const ProtectedRoute = ({ allowedRoles }: ProtectedRouteProps) => {
  const { userError, user } = useAuth();

  if (!user || userError) {
    return <Navigate to="/auth" replace />;
  }

  if (allowedRoles && user.role && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return (
    <SidebarProvider>
      <AdminSidebar />
      <div className="flex min-h-screen flex-col w-full overflow-x-hidden">
        <Header />
        <div className="p-4">
          <Outlet />
        </div>
      </div>
    </SidebarProvider>
  );
};

export default ProtectedRoute;
