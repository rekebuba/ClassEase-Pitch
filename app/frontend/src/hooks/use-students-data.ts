"use client"

import { useState, useEffect } from "react"

import type {
    AverageRange,
    GradeCounts,
    StatusCount,
    Student,
    StudentsDataResult,
    SearchParams,
    StudentsViews,
    TableId,
    SectionCounts
} from "@/lib/types"

import { toast } from "sonner"
import {
    getStudents,
    getStudentsStatusCounts,
    getGradeCounts,
    getStudentsAverageRange,
    getAllStudentsViews,
    getSectionCounts
} from "@/api/adminApi";


export function useStudentsData(validQuery: SearchParams): StudentsDataResult {
    const [data, setData] = useState<Student[]>([])
    const [pageCount, setPageCount] = useState(0)
    const [tableId, setTableId] = useState<TableId>({})
    const [statusCounts, setStatusCounts] = useState<StatusCount>({})
    const [gradeCounts, setGradeCounts] = useState<GradeCounts>({})
    const [sectionCounts, setSectionCounts] = useState<SectionCounts>({})
    const [averageRange, setAverageRange] = useState<AverageRange>({
        totalAverage: { min: "N/A", max: "N/A" },
        averageSemesterOne: { min: "N/A", max: "N/A" },
        averageSemesterTwo: { min: "N/A", max: "N/A" },
        rank: { min: "N/A", max: "N/A" },
        rankSemesterOne: { min: "N/A", max: "N/A" },
        rankSemesterTwo: { min: "N/A", max: "N/A" },
    })
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<Error | null>(null)

    // Function to fetch all data
    const fetchData = async () => {
        setIsLoading(true)
        setError(null)

        // Pass params to API calls if needed
        const [studentsResult, statusCountsResult, gradeCountsResult, sectionCounts, averageRangeResult] =
            await Promise.all([
                getStudents(validQuery),
                getStudentsStatusCounts(),
                getGradeCounts(),
                getSectionCounts(),
                getStudentsAverageRange(),
            ])

        setData(studentsResult.data)
        setPageCount(studentsResult.pageCount)
        setTableId(studentsResult.tableId)
        setStatusCounts(statusCountsResult)
        setGradeCounts(gradeCountsResult)
        setSectionCounts(sectionCounts)
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
        })

        setIsLoading(false)
    }

    // Fetch data when params change
    useEffect(() => {
        fetchData()
    }, [validQuery])

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
    }
}

export function studentsView() {
    const [views, setViews] = useState<StudentsViews[]>()
    const [isViewLoading, setIsViewLoading] = useState(true)
    const [viewError, setViewError] = useState<Error | null>(null)


    const fetchData = async () => {
        setIsViewLoading(true)
        setViewError(null)
        try {
            const result = await getAllStudentsViews()
            setViews(result)
        }
        catch (err) {
            toast.error("Failed to fetch View Table", {
                description: "Please try again later.",
                style: { color: "red" }
            })
            setViewError(err instanceof Error ? err : new Error("Failed to fetch students data"))
        } finally {
            setIsViewLoading(false)
        }
    }

    useEffect(() => {
        fetchData()
    }, [])

    return {
        views,
        isViewLoading,
        viewError,
        refetch: fetchData,
    }
}
