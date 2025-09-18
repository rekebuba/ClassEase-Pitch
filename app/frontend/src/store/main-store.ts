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
import { api } from "./api"; // this is the generated file
import { rtkQueryErrorLogger } from "./middleware/global-error";
import {
  persistedAuthReducer,
  persistedStudentRegistrationForm,
  persistedEmployeeRegistrationForm,
  persistedYearReducer,
} from "./persist";

export const store = configureStore({
  reducer: {
    [api.reducerPath]: api.reducer,
    auth: persistedAuthReducer,
    year: persistedYearReducer,
    studentRegistrationForm: persistedStudentRegistrationForm,
    employeeRegistrationForm: persistedEmployeeRegistrationForm,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    })
      .concat(api.middleware)
      .concat(rtkQueryErrorLogger),
});

export const persister = persistStore(store);
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
