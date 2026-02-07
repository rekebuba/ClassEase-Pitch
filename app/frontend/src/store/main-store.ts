import { configureStore } from "@reduxjs/toolkit";
import {
  FLUSH,
  PAUSE,
  PERSIST,
  persistStore,
  PURGE,
  REGISTER,
  REHYDRATE,
} from "redux-persist";

import { rtkQueryErrorLogger } from "./middleware/global-error";
import {
  persistedAuthReducer,
  persistedEmployeeRegistrationForm,
  persistedStudentRegistrationForm,
  persistedYearReducer,
} from "./persist";

export const store = configureStore({
  reducer: {
    auth: persistedAuthReducer,
    year: persistedYearReducer,
    studentRegistrationForm: persistedStudentRegistrationForm,
    employeeRegistrationForm: persistedEmployeeRegistrationForm,
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    })
      .concat(rtkQueryErrorLogger),
});

export const persister = persistStore(store);
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
