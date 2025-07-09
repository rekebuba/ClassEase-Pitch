import { LoadingSpinner } from "@/components";
import useAuth from "@/context/auth-context";
import { RoleEnumType } from "@/lib/enums";
import { Navigate, Outlet } from "react-router-dom";

interface ProtectedRouteProps {
  allowedRoles?: RoleEnumType[];
}
/**
 * This component checks if a JWT token is present in the local storage.
 * If the token is found, it renders the given component.
 * Otherwise, it redirects the user to the login page.
 */
const ProtectedRoute = ({ allowedRoles }: ProtectedRouteProps) => {
  const { isAuthenticated, userRole, isLoading } = useAuth();

  if (isLoading) return <LoadingSpinner />;

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  if (allowedRoles && userRole && !allowedRoles.includes(userRole)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
