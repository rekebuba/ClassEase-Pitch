"use client";

import { useEffect, useState } from "react";

import type {
  AverageRange,
  GradeCounts,
  SearchParams,
  SectionCounts,
  StatusCount,
  Student,
  StudentsDataResult,
  StudentsViews,
  TableId,
} from "@/lib/types";


export function useStudentsData(
  validQuery: SearchParams | null,
): StudentsDataResult {
  const [data, setData] = useState<Student[]>([]);
  const [pageCount, setPageCount] = useState(0);
  const [tableId, setTableId] = useState<TableId>({});
  const [statusCounts, setStatusCounts] = useState<StatusCount>({});
  const [gradeCounts, setGradeCounts] = useState<GradeCounts>({});
  const [sectionCounts, setSectionCounts] = useState<SectionCounts>({
    sectionSemesterOne: {},
    sectionSemesterTwo: {},
  });
  const [averageRange, setAverageRange] = useState<AverageRange>({
    totalAverage: { min: "N/A", max: "N/A" },
    averageSemesterOne: { min: "N/A", max: "N/A" },
    averageSemesterTwo: { min: "N/A", max: "N/A" },
    rank: { min: "N/A", max: "N/A" },
    rankSemesterOne: { min: "N/A", max: "N/A" },
    rankSemesterTwo: { min: "N/A", max: "N/A" },
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  // Function to fetch all data
  const fetchData = async () => {
    setIsLoading(true);
    setError(null);
    if (!validQuery) {
      setData([]);
      setPageCount(0);
      setTableId({});
      return;
    }

    // Pass params to API calls if needed
    const [
      studentsResult,
      statusCountsResult,
      gradeCountsResult,
      sectionCounts,
      averageRangeResult,
    ] = await Promise.all([
      getStudents(validQuery),
      getStudentsStatusCounts(),
      getGradeCounts(),
      getSectionCounts(),
      getStudentsAverageRange(),
    ]);

    setData(studentsResult.data);
    setPageCount(studentsResult.pageCount);
    setTableId(studentsResult.tableId);
    setStatusCounts(statusCountsResult);
    setGradeCounts(gradeCountsResult);
    setSectionCounts(sectionCounts);
    setAverageRange({
      totalAverage: {
        min: averageRangeResult.totalAverage.min ?? "N/A",
        max: averageRangeResult.totalAverage.max ?? "N/A",
      },
      averageSemesterOne: {
        min: averageRangeResult.averageSemesterOne.min ?? "N/A",
        max: averageRangeResult.averageSemesterOne.max ?? "N/A",
      },
      averageSemesterTwo: {
        min: averageRangeResult.averageSemesterTwo.min ?? "N/A",
        max: averageRangeResult.averageSemesterTwo.max ?? "N/A",
      },
      rank: {
        min: averageRangeResult.rank.min ?? "N/A",
        max: averageRangeResult.rank.max ?? "N/A",
      },
      rankSemesterOne: {
        min: averageRangeResult.rankSemesterOne.min ?? "N/A",
        max: averageRangeResult.rankSemesterOne.max ?? "N/A",
      },
      rankSemesterTwo: {
        min: averageRangeResult.rankSemesterTwo.min ?? "N/A",
        max: averageRangeResult.rankSemesterTwo.max ?? "N/A",
      },
    });

    setIsLoading(false);
  };

  // Fetch data when params change
  useEffect(() => {
    if (!validQuery) {
      setData([]);
      setPageCount(0);
      setTableId({});
      return;
    }
    fetchData();
  }, [validQuery]);

  return {
    data,
    pageCount,
    tableId,
    statusCounts,
    gradeCounts,
    sectionCounts,
    averageRange,
    isLoading,
    error,
    refetch: fetchData,
  };
}

export function studentsView() {
  const [views, setViews] = useState<StudentsViews[]>([]);
  const [isViewLoading, setIsViewLoading] = useState(true);
  const [viewError, setViewError] = useState<Error | null>(null);

  const fetchData = async () => {
    setIsViewLoading(true);
    setViewError(null);
    const result = await getAllStudentsViews();
    setViews(
      result.map((view) => ({
        ...view,
        searchParams: {
          page: view.searchParams.page ?? 1,
          perPage: view.searchParams.perPage ?? 10,
          joinOperator: view.searchParams.joinOperator ?? "and",
          sort: view.searchParams.sort,
          filters: view.searchParams.filters,
        },
      })),
    );
    setIsViewLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  return {
    views,
    isViewLoading,
    viewError,
    refetchViews: fetchData,
  };
}
