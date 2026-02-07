import { AlertTriangle } from "lucide-react";

import { ErrorPage } from "@/components/ui/error-page";

export default function BadRequestPage() {
  return (
    <ErrorPage
      statusCode={400}
      title="Bad Request"
      description="The request could not be understood by the server due to malformed syntax. Please check your request and try again."
      actions={{
        primary: {
          label: "Try Again",
          onClick: () => window.location.reload(),
          icon: <AlertTriangle className="mr-2 h-4 w-4" />,
        },
        secondary: {
          label: "Back to Home",
          href: "/",
        },
      }}
    />
  );
}
