import { AcademicTermTypeEnum } from "@/client/types.gen";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface YearState {
  id: string | undefined;
  name: string | undefined;
  startDate: string | undefined;
  endDate: string | undefined;
  calendarType: AcademicTermTypeEnum | undefined;
}

interface YearPayload {
  id: string;
  name: string;
  startDate: string;
  endDate: string;
  calendarType: AcademicTermTypeEnum;
}

const initialState: YearState = {
  id: undefined,
  name: undefined,
  startDate: undefined,
  endDate: undefined,
  calendarType: undefined,
};

export const yearSlice = createSlice({
  name: "year",
  initialState,
  reducers: {
    setYear: (state, action: PayloadAction<YearPayload>) => {
      state.id = action.payload.id;
      state.name = action.payload.name;
      state.startDate = action.payload.startDate;
      state.endDate = action.payload.endDate;
      state.calendarType = action.payload.calendarType;
    },
  },
});

export const { setYear } = yearSlice.actions;
export default yearSlice.reducer;
