import { TeacherRegistrationForm } from "@/client/types.gen";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface TeacherRegistrationFormState {
  data: TeacherRegistrationForm;
  step: number;
}

const initialFormData: TeacherRegistrationForm = {
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
  highestDegree: undefined as any,
  university: "",
  graduationYear: 0,
  gpa: 0,

  // Teaching Certifications & Licenses
  teachingLicense: false,

  // Teaching Experience
  yearsOfExperience: undefined as any,

  // Employment Information
  positionApplyingFor: "",

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

const initialState: TeacherRegistrationFormState = {
  data: initialFormData,
  step: 1,
};

export const teacherRegistrationFormSlice = createSlice({
  name: "teacherRegistrationForm",
  initialState,
  reducers: {
    setFormData: (state, action: PayloadAction<TeacherRegistrationForm>) => {
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

export const { setFormData, setFormStep, resetForm } =
  teacherRegistrationFormSlice.actions;
export default teacherRegistrationFormSlice.reducer;
