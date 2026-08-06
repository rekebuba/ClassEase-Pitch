import type { RootState } from "@/store/main-store";

export function selectPermissions(state: RootState) {
  return state.auth.activeMembership?.permissions ?? [];
}

export function selectActiveMembership(state: RootState) {
  return state.auth.activeMembership;
}
export function selectRoleNames(state: RootState) {
  return state.auth.activeMembership?.roleNames ?? [];
}
export function selectShellRole(state: RootState) {
  return state.auth.activeMembership?.shellRole;
}

export function selectCurrentSchool(state: RootState) {
  const membership = state.auth.activeMembership;

  if (!membership)
    return null;

  return {
    id: membership.schoolId,
    slug: membership.schoolSlug,
    name: membership.schoolName,
  };
};

export function selectSchoolId(state: RootState) {
  return state.auth.activeMembership?.schoolId ?? null;
}

export function selectSchoolSlug(state: RootState) {
  return state.auth.activeMembership?.schoolSlug ?? null;
}

export function selectLoginIdentifier(state: RootState) {
  return state.auth.activeMembership?.loginIdentifier ?? null;
}

export function selectIsPrimaryMembership(state: RootState) {
  return state.auth.activeMembership?.isPrimary ?? false;
}
