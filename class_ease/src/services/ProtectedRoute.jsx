import React from "react";
import { Navigate } from "react-router-dom";

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
const ProtectedRoute = ({ element: Component }) => {
  const isAuthenticated = localStorage.getItem("token"); // Check if JWT is present

  return isAuthenticated ? Component : <Navigate to="/login" />;
};

export default ProtectedRoute;
