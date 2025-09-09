import type React from "react";
import { ApiError } from "./api-error";
import LoadingSpinner from "./loading-spinner";

interface ApiStateProps {
  isLoading: boolean;
  error?: string | null;
  onRetry?: () => void;
  loadingText?: string;
  errorTitle?: string;
  children: React.ReactNode;
  className?: string;
}

export function ApiState({
  isLoading,
  error,
  onRetry,
  loadingText,
  errorTitle,
  children,
  className,
}: ApiStateProps) {
  if (isLoading) {
    return (
      <div className={className}>
        <LoadingSpinner text={loadingText} />
      </div>
    );
  }

  if (error) {
    return (
      <div className={className}>
        <ApiError title={errorTitle} message={error} onRetry={onRetry} />
      </div>
    );
  }

  return <>{children}</>;
}
