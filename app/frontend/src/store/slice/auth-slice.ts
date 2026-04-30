import { createSlice } from "@reduxjs/toolkit";

import type { MembershipSummary, SchoolSummary } from "@/client/types.gen";
import type { JwtPayloadType } from "@/lib/validations";
import type { PayloadAction } from "@reduxjs/toolkit";

type AuthState = {
  token: string | null;
  refreshToken: string | null;
  userInfo: JwtPayloadType | null;
  activeSchool: SchoolSummary | null;
  activeMembership: MembershipSummary | null;
  availableMemberships: MembershipSummary[];
  isLoading: boolean;
  error: string | null;
};

const initialState: AuthState = {
  token: null,
  refreshToken: null,
  userInfo: null,
  activeSchool: null,
  activeMembership: null,
  availableMemberships: [],
  isLoading: false,
  error: null,
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
        activeMembership?: MembershipSummary | null;
        availableMemberships?: MembershipSummary[];
      }>,
    ) => {
      state.token = action.payload.token;
      state.refreshToken = action.payload.refreshToken ?? null;
      state.userInfo = action.payload.userInfo;
      state.activeSchool = action.payload.activeSchool ?? null;
      state.activeMembership = action.payload.activeMembership ?? null;
      state.availableMemberships = action.payload.availableMemberships ?? [];
      state.isLoading = false;
      state.error = null;
    },
    loginFailure: (state, action: PayloadAction<string>) => {
      state.token = null;
      state.refreshToken = null;
      state.error = action.payload;
      state.isLoading = false;
      state.userInfo = null;
      state.activeSchool = null;
      state.activeMembership = null;
      state.availableMemberships = [];
    },
    logout: (state) => {
      state.token = null;
      state.refreshToken = null;
      state.error = null;
      state.isLoading = false;
      state.userInfo = null;
      state.activeSchool = null;
      state.activeMembership = null;
      state.availableMemberships = [];
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const { loginSuccess, loginFailure, logout, clearError }
  = authSlice.actions;

export default authSlice.reducer;
