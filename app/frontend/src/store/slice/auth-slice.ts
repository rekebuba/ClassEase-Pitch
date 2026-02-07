import { createSlice } from "@reduxjs/toolkit";

import type { JwtPayloadType } from "@/lib/validations";
import type { PayloadAction } from "@reduxjs/toolkit";

type AuthState = {
  token: string | null;
  userInfo: JwtPayloadType | null;
  isLoading: boolean;
  error: string | null;
};

const initialState: AuthState = {
  token: null,
  userInfo: null,
  isLoading: false,
  error: null,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    loginSuccess: (
      state,
      action: PayloadAction<{ token: string; userInfo: JwtPayloadType }>,
    ) => {
      state.token = action.payload.token;
      state.userInfo = action.payload.userInfo;
      state.isLoading = false;
      state.error = null;
    },
    loginFailure: (state, action: PayloadAction<string>) => {
      state.token = null;
      state.error = action.payload;
      state.isLoading = false;
      state.userInfo = null;
    },
    logout: (state) => {
      state.token = null;
      state.error = null;
      state.isLoading = false;
      state.userInfo = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const { loginSuccess, loginFailure, logout, clearError }
  = authSlice.actions;

export default authSlice.reducer;
