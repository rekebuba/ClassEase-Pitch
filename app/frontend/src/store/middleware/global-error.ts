import { isRejectedWithValue } from "@reduxjs/toolkit";
import { toast } from "sonner";

import type { Middleware } from "@reduxjs/toolkit";

/**
 * Log a warning and show a toast!
 */
export const rtkQueryErrorLogger: Middleware = () => next => (action) => {
  // RTK Query uses `createAsyncThunk` from redux-toolkit under the hood, so we're able to utilize these matchers!
  if (isRejectedWithValue(action)) {
    console.warn("We got a rejected action!");

    // In RTK Query, server error responses live in action.payload
    const payload = action.payload as { data?: { message?: string }; status?: number };

    toast.warning("Async error!", {
      description: payload?.data?.message || "An unexpected error occurred",
    });
  }

  return next(action);
};
