import { useQuery } from "@tanstack/react-query";
import { createContext, use, useMemo } from "react";

import { getLoggedInUserOptions } from "@/client/@tanstack/react-query.gen";
import {
  hasAnyPermission as checkAnyPermission,
  hasPermission as checkPermission,
} from "@/lib/permissions";

import type { MembershipSummary, SchoolSummary } from "@/client/types.gen";
import type { PermissionRequirement } from "@/lib/permissions";
import type { PropsWithChildren } from "react";

type PermissionContextValue = {
  activeMembership: MembershipSummary | null;
  activeSchool: SchoolSummary | null;
  hasPermission: (required: PermissionRequirement) => boolean;
  hasAnyPermission: (required: PermissionRequirement) => boolean;
};

const PermissionContext = createContext<PermissionContextValue | null>(null);

export function PermissionProvider({ children }: PropsWithChildren) {
  const { data } = useQuery(getLoggedInUserOptions());

  const value = useMemo<PermissionContextValue>(() => {
    const permissions = data?.activeMembership?.permissions ?? [];

    return {
      activeMembership: data?.activeMembership ?? null,
      activeSchool: data?.activeSchool ?? null,
      hasPermission: required =>
        checkPermission(permissions, required),
      hasAnyPermission: required =>
        checkAnyPermission(permissions, required),
    };
  }, [data]);

  return (
    <PermissionContext value={value}>
      {children}
    </PermissionContext>
  );
}

export function usePermissions() {
  const context = use(PermissionContext);

  if (!context) {
    throw new Error("usePermissions must be used within PermissionProvider");
  }

  return context;
}

export function useHasPermission(required: PermissionRequirement): boolean {
  return usePermissions().hasPermission(required);
}
