import { usePermissions } from "@/components/auth/permission-provider";

import type { PermissionRequirement } from "@/lib/permissions";
import type { ReactNode } from "react";

type PermissionGateProps = {
  permission: PermissionRequirement;
  fallback?: ReactNode;
  children: ReactNode;
};

export function PermissionGate({
  permission,
  fallback = null,
  children,
}: PermissionGateProps) {
  const { hasPermission } = usePermissions();

  if (!hasPermission(permission)) {
    return fallback;
  }

  return children;
}

export const RequirePermission = PermissionGate;
