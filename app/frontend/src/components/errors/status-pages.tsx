import { Link } from "@tanstack/react-router";

import { Button } from "@/components/ui/button";

type StatusPageProps = {
  title: string;
  description: string;
  status: string;
};

function StatusPage({ title, description, status }: StatusPageProps) {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4 text-center">
      <p className="text-sm font-medium text-muted-foreground">{status}</p>
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold tracking-tight">{title}</h1>
        <p className="max-w-md text-muted-foreground">{description}</p>
      </div>
      <Button asChild>
        <Link to="/dashboard">Back to dashboard</Link>
      </Button>
    </div>
  );
}

export function UnauthorizedPage() {
  return (
    <StatusPage
      status="401"
      title="Authentication required"
      description="Sign in and select a school membership to continue."
    />
  );
}

export function ForbiddenPage() {
  return (
    <StatusPage
      status="403"
      title="Access denied"
      description="Your current membership does not include permission to view this page."
    />
  );
}

export function NotFoundPage() {
  return (
    <StatusPage
      status="404"
      title="Page not found"
      description="The page you are looking for does not exist."
    />
  );
}
