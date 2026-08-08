import { createContext, use, useEffect, useMemo, useState } from "react";
import { toast } from "sonner";

import {
  demoGuestProfile,
  emptyGuestProfile,
  getProfileMissingFields,
  initialGuestApplications,
} from "@/lib/guest-data";

import type { GuestApplication, GuestApplicationStatus, GuestProfile, GuestSchool, SchoolPosition } from "@/lib/guest-data";
import type { ReactNode } from "react";

const profileStorageKey = "classease.guest.profile";
const applicationsStorageKey = "classease.guest.applications";

type GuestContextValue = {
  profile: GuestProfile;
  applications: GuestApplication[];
  isProfileComplete: boolean;
  missingProfileFields: ReturnType<typeof getProfileMissingFields>;
  saveProfile: (profile: GuestProfile) => void;
  loadDemoProfile: () => void;
  submitApplication: (school: GuestSchool, position: SchoolPosition) => GuestApplication;
  updateApplicationStatus: (applicationId: string, status: GuestApplicationStatus) => void;
};

const GuestContext = createContext<GuestContextValue | null>(null);

function readStoredValue<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") {
    return fallback;
  }

  try {
    const value = window.localStorage.getItem(key);
    return value ? JSON.parse(value) as T : fallback;
  }
  catch {
    return fallback;
  }
}

export function GuestProvider({ children }: { children: ReactNode }) {
  const [profile, setProfile] = useState<GuestProfile>(() =>
    readStoredValue(profileStorageKey, emptyGuestProfile));
  const [applications, setApplications] = useState<GuestApplication[]>(() =>
    readStoredValue(applicationsStorageKey, initialGuestApplications));

  useEffect(() => {
    window.localStorage.setItem(profileStorageKey, JSON.stringify(profile));
  }, [profile]);

  useEffect(() => {
    window.localStorage.setItem(applicationsStorageKey, JSON.stringify(applications));
  }, [applications]);

  const missingProfileFields = useMemo(() => getProfileMissingFields(profile), [profile]);
  const isProfileComplete = missingProfileFields.length === 0;

  const value = useMemo<GuestContextValue>(() => ({
    profile,
    applications,
    missingProfileFields,
    isProfileComplete,
    saveProfile: (nextProfile) => {
      setProfile(nextProfile);
      toast.success("Application profile saved");
    },
    loadDemoProfile: () => {
      setProfile(demoGuestProfile);
      toast.success("Profile completed with realistic sample details");
    },
    submitApplication: (school, position) => {
      const existing = applications.find(application =>
        application.schoolSlug === school.slug && application.positionId === position.id);

      if (existing) {
        return existing;
      }

      const application: GuestApplication = {
        id: `app-${Date.now()}`,
        schoolSlug: school.slug,
        schoolName: school.name,
        positionId: position.id,
        positionTitle: position.title,
        submittedAt: new Date().toISOString().slice(0, 10),
        status: "Pending",
        applicantName: `${profile.firstName} ${profile.lastName}`.trim(),
        email: profile.email,
        phone: profile.phone,
        education: [profile.highestEducation, profile.fieldOfStudy].filter(Boolean).join(" in "),
        experience: profile.yearsOfExperience ? `${profile.yearsOfExperience} years` : "Not specified",
      };

      setApplications(current => [application, ...current]);
      toast.success("Application submitted");
      return application;
    },
    updateApplicationStatus: (applicationId, status) => {
      setApplications(current =>
        current.map(application =>
          application.id === applicationId ? { ...application, status } : application));
    },
  }), [applications, isProfileComplete, missingProfileFields, profile]);

  return <GuestContext value={value}>{children}</GuestContext>;
}

export function useGuest() {
  const context = use(GuestContext);

  if (!context) {
    throw new Error("useGuest must be used within GuestProvider");
  }

  return context;
}
