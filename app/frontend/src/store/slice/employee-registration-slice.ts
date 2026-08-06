import { createSlice } from "@reduxjs/toolkit";

import type { EmployeeProfile } from "@/client/types.gen";
import type { PayloadAction } from "@reduxjs/toolkit";

type EmployeeRegistrationFormState = {
  data: EmployeeProfile;
  step: number;
};

const initialFormData: EmployeeProfile = {
  userId: "",
  employeeNumber: "",
  hireDate: "",
  employmentStatus: undefined as any,
  employmentType: undefined as any,
  terminationDate: "",
  departmentId: "",
  primaryPositionId: "",
  managerEmployeeId: "",
  workEmail: "",
  workPhone: "",
};

const initialState: EmployeeRegistrationFormState = {
  data: initialFormData,
  step: 1,
};

export const employeeRegistrationFormSlice = createSlice({
  name: "employeeRegistrationForm",
  initialState,
  reducers: {
    setFormData: (state, action: PayloadAction<EmployeeProfile>) => {
      state.data = action.payload;
    },
    setFormStep: (state, action: PayloadAction<number>) => {
      state.step = action.payload;
    },
    resetForm: (state) => {
      state.data = initialFormData;
      state.step = 1;
    },
  },
});

export const { setFormData, setFormStep, resetForm }
  = employeeRegistrationFormSlice.actions;
export default employeeRegistrationFormSlice.reducer;
