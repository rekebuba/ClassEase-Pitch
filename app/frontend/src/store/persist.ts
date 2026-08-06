import { persistReducer } from "redux-persist";
// import storage from "redux-persist/lib/storage"; // defaults to localStorage for web

import authReducer from "./slice/auth/auth-slice";
import employeeRegistrationFormReducer from "./slice/employee-registration-slice";
import studentRegistrationFormReducer from "./slice/student-registration-slice";
import yearReducer from "./slice/year-slice";

const storage = {
  getItem: (key: string) => Promise.resolve(localStorage.getItem(key)),
  setItem: (key: string, value: string) => {
    localStorage.setItem(key, value);
    return Promise.resolve();
  },
  removeItem: (key: string) => {
    localStorage.removeItem(key);
    return Promise.resolve();
  },
};

// Persist configuration
const authPersistConfig = {
  key: "auth",
  storage,
  // Only persist the token, not loading states or errors
  whitelist: [
    "token",
    "refreshToken",
    "userInfo",
    "activeSchool",
    "selectedSchool",
    "currentSchool",
    "activeMembership",
    "currentMembership",
    "availableMemberships",
    "permissions",
    "permissionVersion",
  ],
  // Optionally, you can blacklist instead
  // blacklist: ['isLoading', 'error']
};

// Create persisted reducer
export const persistedAuthReducer = persistReducer(
  authPersistConfig,
  authReducer,
);

// Persist configuration
const yearPersistConfig = {
  key: "year",
  storage,
  whitelist: ["id", "name"],
};

// Create persisted reducer
export const persistedYearReducer = persistReducer(
  yearPersistConfig,
  yearReducer,
);

const studentRegistrationFormConfig = {
  key: "studentRegistrationForm",
  storage,
  whitelist: ["data", "step"],
};

export const persistedStudentRegistrationForm = persistReducer(
  studentRegistrationFormConfig,
  studentRegistrationFormReducer,
);

const employeeRegistrationFormConfig = {
  key: "employeeRegistrationForm",
  storage,
  whitelist: ["data", "step"],
};

export const persistedEmployeeRegistrationForm = persistReducer(
  employeeRegistrationFormConfig,
  employeeRegistrationFormReducer,
);
