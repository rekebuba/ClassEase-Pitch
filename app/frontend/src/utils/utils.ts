import { toast } from "sonner";

export const emailPattern = {
  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  message: "Invalid email address",
};

export const namePattern = {
  value: /^[A-Za-z\s\u00C0-\u017F]{1,30}$/,
  message: "Invalid name",
};

export const passwordRules = (isRequired = true) => {
  const rules: any = {
    minLength: {
      value: 8,
      message: "Password must be at least 8 characters",
    },
  };

  if (isRequired) {
    rules.required = "Password is required";
  }

  return rules;
};

export const confirmPasswordRules = (
  getValues: () => any,
  isRequired = true,
) => {
  const rules: any = {
    validate: (value: string) => {
      const password = getValues().password || getValues().new_password;
      return value === password ? true : "The passwords do not match";
    },
  };

  if (isRequired) {
    rules.required = "Password confirmation is required";
  }

  return rules;
};

export const handleError = (err: any) => {
  const errDetail = err.detail;
  let errorMessage: string = "Something went wrong.";
  if (Array.isArray(errDetail) && errDetail.length > 0) {
    errorMessage = errDetail[0].msg;
  } else if (typeof errDetail === "string" && errDetail) {
    errorMessage = errDetail;
  }
  toast.error(errorMessage, {
    style: {
      color: "red",
    },
  });
  return errorMessage;
};

// Map RHF's dirtyFields over the `data` received by `handleSubmit` and return the changed subset of that data.
export function getDirtyValues<T extends object>(
  dirtyFields: unknown,
  allValues: T,
): Partial<T> {
  // Handle primitive dirty fields
  if (dirtyFields === true) {
    return allValues;
  }

  // Handle arrays - if any item is dirty, return entire array
  if (Array.isArray(dirtyFields)) {
    const hasDirtyItems = dirtyFields.some(
      (item) =>
        item === true ||
        (typeof item === "object" && item !== null) ||
        Array.isArray(item),
    );
    return hasDirtyItems ? allValues : undefined!;
  }

  // Handle non-object dirty fields or false values
  if (typeof dirtyFields !== "object" || dirtyFields === null) {
    return undefined!;
  }

  // Handle object case
  const result: Partial<T> = {};

  Object.entries(dirtyFields).forEach(([key, value]) => {
    const fieldKey = key as keyof T;
    const fieldValue = allValues[fieldKey];

    if (fieldValue !== undefined) {
      const dirtyValue = getDirtyValues(value, fieldValue as object);
      if (dirtyValue !== undefined) {
        result[fieldKey] = dirtyValue as T[keyof T];
      }
    }
  });

  return Object.keys(result).length > 0 ? result : undefined!;
}
export function uniqueByKey<T, K extends keyof T>(
  array: T[],
  key: K = "id" as K,
): T[] {
  return [...new Map(array.map((item) => [item[key], item])).values()];
}

export function academicYearRange(
  startDate: string | undefined,
  endDate: string | undefined,
): string {
  if (!startDate || !endDate) {
    return "N/A";
  }
  const start = new Date(startDate);
  const end = new Date(endDate);
  const startYear = start.getFullYear();
  const endYear = end.getFullYear();
  if (isNaN(startYear) || isNaN(endYear)) {
    return "";
  }
  if (startYear === endYear) {
    return `${startYear}`;
  }
  return `${startYear}/${endYear}`;
}

export function extractFirstWord(loc: string[], msg: string): string | null {
  // Split by comma, take the part after the first comma
  if (loc.length === 2) {
    return loc[1];
  }

  const [, afterComma] = msg.split(",", 2);

  if (!afterComma) return null;

  // Trim spaces and split into words
  const firstWord = afterComma.trim().split(/\s+/)[0];
  return firstWord || null;
}

export const getInitials = (firstName: string, fatherName: string) => {
  return `${firstName.charAt(0)}${fatherName.charAt(0)}`.toUpperCase();
};

export const calculateAge = (dateOfBirth: string) => {
  const today = new Date();
  const birthDate = new Date(dateOfBirth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  if (
    monthDiff < 0 ||
    (monthDiff === 0 && today.getDate() < birthDate.getDate())
  ) {
    age--;
  }
  return age;
};
