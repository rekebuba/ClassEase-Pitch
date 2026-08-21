import { createSlice } from "@reduxjs/toolkit";

import type { StudentProfile } from "@/client/types.gen";
import type { PayloadAction } from "@reduxjs/toolkit";

type StudentRegistrationFormState = {
  data: StudentProfile;
  step: number;
};

const initialFormData: StudentProfile = {
  userId: "",
  isTransfer: false,
  parents: [],
};

const initialState: StudentRegistrationFormState = {
  data: initialFormData,
  step: 1,
};

export const studentRegistrationFormSlice = createSlice({
  name: "studentRegistrationForm",
  initialState,
  reducers: {
    setFormData: (state, action: PayloadAction<StudentProfile>) => {
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
  = studentRegistrationFormSlice.actions;
export default studentRegistrationFormSlice.reducer;
