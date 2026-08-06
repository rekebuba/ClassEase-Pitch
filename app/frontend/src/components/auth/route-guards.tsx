import { Navigate } from "@tanstack/react-router";

import { usePermissions } from "@/components/auth/permission-provider";
import { ForbiddenPage, UnauthorizedPage } from "@/components/errors/status-pages";

import type { PermissionRequirement } from "@/lib/permissions";
import type { ReactNode } from "react";

type GuardProps = {
  children: ReactNode;
};

export function RequireAuthentication({ children }: GuardProps) {
  const { activeMembership } = usePermissions();

  if (!activeMembership) {
    return <Navigate to="/authentication" />;
  }

  return children;
}

export function RequireMembership({ children }: GuardProps) {
  const { activeMembership } = usePermissions();

  if (!activeMembership) {
    return <UnauthorizedPage />;
  }

  return children;
}

export function RouteGuard({
  permission,
  children,
}: GuardProps & { permission?: PermissionRequirement }) {
  const { activeMembership, hasPermission } = usePermissions();

  if (!activeMembership) {
    return <Navigate to="/authentication" />;
  }

  if (permission && !hasPermission(permission)) {
    return <ForbiddenPage />;
  }

  return children;
}
