"use client";

import { useEffect, useCallback, useRef } from "react";
import type { TeacherRegistrationFormData } from "@/lib/form-validation";

const STORAGE_KEY = "teacher-registration-form";
const STEP_STORAGE_KEY = "teacher-registration-step";
const DEBOUNCE_DELAY = 1000;

export function useTeacherFormPersistence() {
  const debounceTimerRef = useRef<NodeJS.Timeout>();

  const saveFormData = useCallback(
    (data: TeacherRegistrationFormData, currentStep: number) => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }

      debounceTimerRef.current = setTimeout(() => {
        try {
          // Convert File objects to serializable format
          const serializableData = {
            ...data,
            profilePhoto: data.profilePhoto
              ? {
                  name: data.profilePhoto.name,
                  size: data.profilePhoto.size,
                  type: data.profilePhoto.type,
                  lastModified: data.profilePhoto.lastModified,
                }
              : undefined,
            resume: data.resume
              ? {
                  name: data.resume.name,
                  size: data.resume.size,
                  type: data.resume.type,
                  lastModified: data.resume.lastModified,
                }
              : undefined,
            coverLetter: data.coverLetter
              ? {
                  name: data.coverLetter.name,
                  size: data.coverLetter.size,
                  type: data.coverLetter.type,
                  lastModified: data.coverLetter.lastModified,
                }
              : undefined,
            transcripts: data.transcripts
              ? {
                  name: data.transcripts.name,
                  size: data.transcripts.size,
                  type: data.transcripts.type,
                  lastModified: data.transcripts.lastModified,
                }
              : undefined,
            teachingCertificate: data.teachingCertificate
              ? {
                  name: data.teachingCertificate.name,
                  size: data.teachingCertificate.size,
                  type: data.teachingCertificate.type,
                  lastModified: data.teachingCertificate.lastModified,
                }
              : undefined,
            backgroundCheck: data.backgroundCheck
              ? {
                  name: data.backgroundCheck.name,
                  size: data.backgroundCheck.size,
                  type: data.backgroundCheck.type,
                  lastModified: data.backgroundCheck.lastModified,
                }
              : undefined,
          };

          localStorage.setItem(STORAGE_KEY, JSON.stringify(serializableData));
          localStorage.setItem(STEP_STORAGE_KEY, currentStep.toString());

          console.log("Teacher form progress saved automatically");
        } catch (error) {
          console.error("Failed to save teacher form data:", error);
        }
      }, DEBOUNCE_DELAY);
    },
    [],
  );

  const loadFormData = useCallback((): {
    data: Partial<TeacherRegistrationFormData>;
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
          step: Math.max(1, Math.min(step, 7)),
        };
      }
    } catch (error) {
      console.error("Failed to load teacher form data:", error);
    }

    return null;
  }, []);

  const clearFormData = useCallback(() => {
    try {
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(STEP_STORAGE_KEY);
      console.log("Teacher form progress cleared");
    } catch (error) {
      console.error("Failed to clear teacher form data:", error);
    }
  }, []);

  const hasSavedData = useCallback((): boolean => {
    try {
      return localStorage.getItem(STORAGE_KEY) !== null;
    } catch (error) {
      return false;
    }
  }, []);

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
