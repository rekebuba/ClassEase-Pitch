import { createSlice } from "@reduxjs/toolkit";

import type { EmployeeRegistrationForm } from "@/client/types.gen";
import type { PayloadAction } from "@reduxjs/toolkit";

type EmployeeRegistrationFormState = {
  data: EmployeeRegistrationForm;
  step: number;
};

const initialFormData: EmployeeRegistrationForm = {
  // Personal Information
  firstName: "",
  fatherName: "",
  grandFatherName: "",
  dateOfBirth: "",
  gender: undefined as any,
  nationality: "",
  maritalStatus: undefined,
  socialSecurityNumber: "",

  // Contact Information
  address: "",
  city: "",
  state: "",
  country: "",
  primaryPhone: "",
  secondaryPhone: "",
  personalEmail: "",

  // Emergency Contact
  emergencyContactName: "",
  emergencyContactRelation: "",
  emergencyContactPhone: "",

  // Educational Background
  highestEducation: undefined as any,
  university: "",
  graduationYear: 0,
  gpa: 0,

  // Teaching Experience
  yearsOfExperience: undefined as any,

  // Employment Information
  position: undefined as any,
  subjectId: undefined,

  // Background & References
  reference1Name: "",
  reference1Organization: "",
  reference1Phone: "",
  reference1Email: undefined,

  // Documents
  resume: undefined,
  backgroundCheck: undefined,

  // Additional Information
  agreeToTerms: false,
  agreeToBackgroundCheck: false,
};

const initialState: EmployeeRegistrationFormState = {
  data: initialFormData,
  step: 1,
};

export const employeeRegistrationFormSlice = createSlice({
  name: "employeeRegistrationForm",
  initialState,
  reducers: {
    setFormData: (state, action: PayloadAction<EmployeeRegistrationForm>) => {
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
