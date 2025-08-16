import { useState, useEffect } from "react";
import sharedApi from "@/api/sharedApi";
import {
  GradeSchema,
  StreamSchema,
  SubjectSchema,
  YearSchema,
} from "@/lib/api-response-type";
import { AcademicTermEnumType, AcademicYearStatusEnumType } from "@/lib/enums";

export interface AcademicYear {
  id: string;
  name: string;
  startDate: string;
  endDate: string;
  calendarType: AcademicTermEnumType;
  status: AcademicYearStatusEnumType;
  grades: Grade[];
  subjects: Subject[];
  createdAt: string;
  updatedAt: string;
}

export interface Grade {
  id: string;
  grade: string;
  level: string | number;
  hasStreams: boolean;
  streams: Stream[];
  maxSections: number;
  sections: Section[];
  subjects: Subject[];
}

export interface Section {
  id: string;
  section: string;
}

export interface Stream {
  id: string;
  name: string;
  subjects: Subject[];
}

export interface Subject {
  id: string;
  name: string;
  code: string;
  grades: string[];
}

export function useAcademicYears() {
  const [data, setData] = useState<string[]>([]);
  const [subjects, setSubjects] = useState<SubjectSchema[]>([]);
  const [grades, setGrades] = useState<GradeSchema[]>([]);
  const [academicYears, setAcademicYears] = useState<YearSchema[]>([]);
  const [streams, setStreams] = useState<StreamSchema[]>([]);
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState({
    subjects: "",
    grades: "",
    global: "",
  });

  const fetchAllData = async () => {
    setLoading(true);
    setErrors({ subjects: "", grades: "", global: "" });

    try {
      const [subjectsRes, gradesRes, academicYearRes, streamsRes] =
        await Promise.all([
          sharedApi.getAcademicYears().catch((error) => error),
          sharedApi.getSubjects().catch((error) => error),
          sharedApi.getGrades().catch((error) => error),
          sharedApi.getStreams().catch((error) => error),
        ]);

      // Handle successful responses
      if (subjectsRes.success) setSubjects(subjectsRes.data);
      if (gradesRes.success) setGrades(gradesRes.data);
      if (academicYearRes.success) setAcademicYears(academicYearRes.data);
      if (streamsRes.success) setStreams(streamsRes.data);

      // Track individual errors
      const newErrors = { ...errors };
      if (!subjectsRes.success) newErrors.subjects = subjectsRes.error.message;
      if (!gradesRes.success) newErrors.grades = gradesRes.error.message;
      if (!academicYearRes.success)
        newErrors.global = academicYearRes.error.message;
      if (!streamsRes.success) newErrors.global = streamsRes.error.message;
      setErrors(newErrors);
    } catch (error) {
      setErrors((prev) => ({
        ...prev,
        global: "An unexpected error occurred",
      }));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  return { data, loading, errors, refetch: fetchAllData };
}
