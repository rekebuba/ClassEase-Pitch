import { zPermissionEnum } from "@/client/zod.gen";
import { store } from "@/store/main-store";
import { selectPermissions } from "@/store/slice/auth/auth-selectors";

import type { PermissionEnum } from "@/client/types.gen";

export const Permission = zPermissionEnum.enum;

export type PermissionRequirement = PermissionEnum | PermissionEnum[];

export function hasPermission(
  permissions: readonly PermissionEnum[],
  required: PermissionRequirement,
): boolean {
  const requirements = Array.isArray(required) ? required : [required];
  return requirements.every(permission => permissions.includes(permission));
}

export function hasAnyPermission(
  permissions: readonly PermissionEnum[],
  required: PermissionRequirement,
): boolean {
  const requirements = Array.isArray(required) ? required : [required];
  return requirements.some(permission => permissions.includes(permission));
}

export function can(permission: PermissionRequirement): boolean {
  const state = store.getState();
  const permissions = selectPermissions(state);
  return hasPermission(permissions, permission);
}

export function canAny(permission: PermissionRequirement): boolean {
  const state = store.getState();
  const permissions = selectPermissions(state);
  return hasAnyPermission(permissions, permission);
}
