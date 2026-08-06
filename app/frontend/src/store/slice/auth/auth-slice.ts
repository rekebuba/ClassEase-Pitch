import { createSlice } from "@reduxjs/toolkit";

import type { MembershipSummary, PermissionEnum, SchoolSummary, SessionScope } from "@/client/types.gen";
import type { JwtPayloadType } from "@/lib/validations";
import type { PayloadAction } from "@reduxjs/toolkit";

export type AuthState = {
  token: string | null;
  refreshToken: string | null;
  userInfo: JwtPayloadType | null;
  sessionScope: SessionScope | null;
  activeMembership: MembershipSummary | null;
  availableMemberships: MembershipSummary[];
  isLoading: boolean;
  error: string | null;
};

const initialState: AuthState = {
  token: null,
  refreshToken: null,
  userInfo: null,
  activeMembership: null,
  availableMemberships: [],
  isLoading: false,
  error: null,
  sessionScope: null,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    loginSuccess: (
      state,
      action: PayloadAction<{
        token: string;
        refreshToken?: string | null;
        userInfo: JwtPayloadType;
        activeSchool?: SchoolSummary | null;
        selectedSchool?: SchoolSummary | null;
        currentSchool?: SchoolSummary | null;
        activeMembership?: MembershipSummary | null;
        currentMembership?: MembershipSummary | null;
        availableMemberships?: MembershipSummary[];
        permissions?: PermissionEnum[];
        permissionVersion?: number | null;
        sessionScope?: SessionScope | null;
      }>,
    ) => {
      state.token = action.payload.token;
      state.refreshToken = action.payload.refreshToken ?? null;
      state.userInfo = action.payload.userInfo;
      state.activeMembership = action.payload.activeMembership ?? null;
      state.availableMemberships = action.payload.availableMemberships ?? [];
      state.isLoading = false;
      state.error = null;
      state.sessionScope = action.payload.sessionScope ?? null;
    },
    loginFailure: (state, action: PayloadAction<string>) => {
      state.token = null;
      state.refreshToken = null;
      state.error = action.payload;
      state.isLoading = false;
      state.userInfo = null;
      state.activeMembership = null;
      state.availableMemberships = [];
      state.sessionScope = null;
    },
    logout: (state) => {
      state.token = null;
      state.refreshToken = null;
      state.error = null;
      state.isLoading = false;
      state.userInfo = null;
      state.activeMembership = null;
      state.availableMemberships = [];
      state.sessionScope = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const { loginSuccess, loginFailure, logout, clearError }
  = authSlice.actions;

export default authSlice.reducer;
