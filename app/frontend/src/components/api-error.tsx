import { AlertCircle, RefreshCw } from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type ApiErrorProps = {
  title?: string;
  message?: string;
  onRetry?: () => void;
  retryText?: string;
  className?: string;
  variant?: "default" | "destructive";
};

export function ApiError({
  title = "Something went wrong",
  message = "We encountered an error while loading your data. Please try again.",
  onRetry,
  retryText = "Try again",
  className,
  variant = "destructive",
}: ApiErrorProps) {
  return (
    <Alert variant={variant} className={cn("max-w-md", className)}>
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>{title}</AlertTitle>
      <AlertDescription className="mt-2">
        {message}
        {onRetry && (
          <Button
            variant="outline"
            size="sm"
            onClick={onRetry}
            className="mt-3 w-full bg-transparent"
          >
            <RefreshCw className="w-4 h-4 mr-2" />
            {retryText}
          </Button>
        )}
      </AlertDescription>
    </Alert>
  );
}
