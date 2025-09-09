import type { Middleware } from "@reduxjs/toolkit";
import { isRejectedWithValue } from "@reduxjs/toolkit";
import { toast } from "sonner";

/**
 * Log a warning and show a toast!
 */
export const rtkQueryErrorLogger: Middleware = () => (next) => (action) => {
  // RTK Query uses `createAsyncThunk` from redux-toolkit under the hood, so we're able to utilize these matchers!
  if (isRejectedWithValue(action)) {
    console.log(action.error);
    console.warn("We got a rejected action!");
    toast.warning("Async error!", {
      description:
        "data" in action.error
          ? (action.error.data as { message: string }).message
          : action.error.message,
    });
  }

  return next(action);
};
