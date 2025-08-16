"use client";

import { useEffect, useCallback, useRef } from "react";
import type { StudentRegistrationFormData } from "@/lib/form-validation";

const STORAGE_KEY = "student-registration-form";
const STEP_STORAGE_KEY = "student-registration-step";
const DEBOUNCE_DELAY = 1000; // Save after 1 second of inactivity

export function useFormPersistence() {
  const debounceTimerRef = useRef<NodeJS.Timeout>();

  // Save form data to localStorage with debouncing
  const saveFormData = useCallback(
    (data: StudentRegistrationFormData, currentStep: number) => {
      // Clear existing timer
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }

      // Set new timer
      debounceTimerRef.current = setTimeout(() => {
        try {
          // Convert File objects to a serializable format
          const serializableData = {
            ...data,
            studentPhoto: data.studentPhoto
              ? {
                  name: data.studentPhoto.name,
                  size: data.studentPhoto.size,
                  type: data.studentPhoto.type,
                  lastModified: data.studentPhoto.lastModified,
                }
              : undefined,
          };

          localStorage.setItem(STORAGE_KEY, JSON.stringify(serializableData));
          localStorage.setItem(STEP_STORAGE_KEY, currentStep.toString());

          // Show a subtle save indicator
          console.log("Form progress saved automatically");
        } catch (error) {
          console.error("Failed to save form data:", error);
        }
      }, DEBOUNCE_DELAY);
    },
    [],
  );

  // Load form data from localStorage
  const loadFormData = useCallback((): {
    data: Partial<StudentRegistrationFormData>;
    step: number;
  } | null => {
    try {
      const savedData = localStorage.getItem(STORAGE_KEY);
      const savedStep = localStorage.getItem(STEP_STORAGE_KEY);

      if (savedData) {
        const parsedData = JSON.parse(savedData);
        const step = savedStep ? Number.parseInt(savedStep, 10) : 1;
        return {
          data: parsedData,
          step: Math.max(1, Math.min(step, 6)), // Ensure step is between 1-6
        };
      }
    } catch (error) {
      console.error("Failed to load form data:", error);
    }

    return null;
  }, []);

  // Clear saved form data
  const clearFormData = useCallback(() => {
    try {
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(STEP_STORAGE_KEY);
      console.log("Form progress cleared");
    } catch (error) {
      console.error("Failed to clear form data:", error);
    }
  }, []);

  // Check if there's saved data
  const hasSavedData = useCallback((): boolean => {
    try {
      return localStorage.getItem(STORAGE_KEY) !== null;
    } catch (error) {
      return false;
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  return {
    saveFormData,
    loadFormData,
    clearFormData,
    hasSavedData,
  };
}
