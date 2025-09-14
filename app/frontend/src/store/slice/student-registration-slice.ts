import { StudentRegistrationForm } from "@/client/types.gen";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface StudentRegistrationFormState {
  data: StudentRegistrationForm;
  step: number;
}

const initialFormData: StudentRegistrationForm = {
  registeredForGradeId: "",
  firstName: "",
  fatherName: "",
  grandFatherName: "",
  dateOfBirth: "",
  gender: undefined as any,
  nationality: "",
  bloodType: undefined,
  studentPhoto: undefined,
  isTransfer: false,
  previousSchool: "",
  address: "",
  city: "",
  state: "",
  postalCode: "1000",
  fatherPhone: "",
  motherPhone: "",
  parentEmail: "",
  guardianName: "",
  guardianPhone: "",
  guardianRelation: null,
  emergencyContactName: null,
  emergencyContactPhone: null,
  hasMedicalCondition: false,
  medicalDetails: "",
  hasDisability: false,
  disabilityDetails: "",
  transportation: null,
  siblingInSchool: false,
  siblingDetails: "",
};

const initialState: StudentRegistrationFormState = {
  data: initialFormData,
  step: 1,
};

export const studentRegistrationFormSlice = createSlice({
  name: "studentRegistrationForm",
  initialState,
  reducers: {
    setFormData: (state, action: PayloadAction<StudentRegistrationForm>) => {
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
  studentRegistrationFormSlice.actions;
export default studentRegistrationFormSlice.reducer;
