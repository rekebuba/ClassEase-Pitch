import { Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

/**
 * ProtectedRoute component to guard routes that require authentication.
 *
 * This component checks if a JWT token is present in the local storage.
 * If the token is found, it renders the given component.
 * Otherwise, it redirects the user to the login page.
 *
 * @param {Object} props - The properties object.
 * @param {React.Component} props.element - The component to render if authenticated.
 * @returns {React.Component} - The given component if authenticated, otherwise a <Navigate> component to redirect to the login page.
 */
const ProtectedRoute = ({ element, allowedRoles }) => {
  const { isAuthenticated, userRole, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>; // Show a loading spinner or placeholder
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth" />;
  }

  if (allowedRoles && !allowedRoles.includes(userRole)) {
    return <Navigate to="/unauthorized" />; // Redirect to an unauthorized page
  }


  return element;
};

export default ProtectedRoute;
