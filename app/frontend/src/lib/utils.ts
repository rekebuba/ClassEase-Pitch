import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getIsMacOS() {
  if (typeof navigator === "undefined") return false
  return navigator.userAgent?.includes("Mac")
}
