"use client"

import { useState, useEffect } from "react"

import type {
    AttendanceRange,
    AverageRange,
    GradeCounts,
    StatusCount,
    Student,
    StudentsDataResult,
    SearchParams,
    StudentsViews,
    TableId
} from "@/lib/types"

import { toast } from "sonner"
import {
    getStudents,
    getStudentsStatusCounts,
    getGradeCounts,
    getStudentsAttendanceRange,
    getStudentsAverageRange,
    getAllStudentsViews
} from "@/api/adminApi";


export function useStudentsData(validQuery: SearchParams): StudentsDataResult {
    const [data, setData] = useState<Student[]>([])
    const [pageCount, setPageCount] = useState(0)
    const [tableId, setTableId] = useState<TableId | null>({})
    const [statusCounts, setStatusCounts] = useState<StatusCount>({})
    const [gradeCounts, setGradeCounts] = useState<GradeCounts>({})
    const [attendanceRange, setAttendanceRange] = useState<AttendanceRange>({ min: 0, max: 0 })
    const [averageRange, setAverageRange] = useState<AverageRange>({ min: 0, max: 0 })
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<Error | null>(null)

    // Function to fetch all data
    const fetchData = async () => {
        setIsLoading(true)
        setError(null)

        // Pass params to API calls if needed
        const [studentsResult, statusCountsResult, gradeCountsResult, attendanceRangeResult, averageRangeResult] =
            await Promise.all([
                getStudents(validQuery),
                getStudentsStatusCounts(),
                getGradeCounts(),
                getStudentsAttendanceRange(),
                getStudentsAverageRange(),
            ])

        setData(studentsResult.data)
        setPageCount(studentsResult.pageCount)
        setTableId(studentsResult.tableId)
        setStatusCounts(statusCountsResult)
        setGradeCounts(gradeCountsResult)
        setAttendanceRange(attendanceRangeResult)
        setAverageRange(averageRangeResult)

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
        attendanceRange,
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
