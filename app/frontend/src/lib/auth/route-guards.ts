import { redirect } from "@tanstack/react-router";

import { can } from "@/lib/permissions";
import { store } from "@/store/main-store";

import type { PermissionRequirement } from "@/lib/permissions";

export function requireAuthentication() {
  const { auth } = store.getState();

  if (!auth.token) {
    throw redirect({ to: "/authentication" });
  }

  return auth;
}

export function requireMembership() {
  const auth = requireAuthentication();

  if (!(auth.activeMembership)) {
    throw redirect({ to: "/authentication" });
  }

  return auth;
}

export function requireRoutePermission(required: PermissionRequirement) {
  const auth = requireMembership();

  if (!can(required)) {
    throw redirect({ to: "/dashboard/forbidden" });
  }

  return auth;
}
