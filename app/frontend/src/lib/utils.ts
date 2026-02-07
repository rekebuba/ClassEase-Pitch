import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

import type { ClassValue } from "clsx";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getIsMacOS() {
  if (typeof navigator === "undefined")
    return false;
  return navigator.userAgent?.includes("Mac");
}
