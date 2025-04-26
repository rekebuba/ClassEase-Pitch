"use client"

import { useState, useEffect } from "react"

import {
    getStudentsData,
    getStatusCounts,
    getGradeCounts,
    getAttendanceRange,
    getGradeRange,
    getStudentsViews,
} from "@/pages/admin/AdminManageStud"

import type { Student } from "@/lib/types"
import type { SearchParams, View } from "@/lib/validations"
import { toast } from "sonner"

interface StudentsDataResult {
    data: Student[]
    pageCount: number
    statusCounts: Record<string, number>
    gradeCounts: Record<string, number>
    attendanceRange: { min: number, max: number }
    gradeRange: { min: number, max: number }
    isLoading: boolean
    error: Error | null
    refetch: () => Promise<void>
}

export function useStudentsData(params: SearchParams | null): StudentsDataResult {
    const [data, setData] = useState<Student[]>([])
    const [pageCount, setPageCount] = useState(0)
    const [statusCounts, setStatusCounts] = useState<Record<string, number>>({})
    const [gradeCounts, setGradeCounts] = useState<Record<string, number>>({})
    const [attendanceRange, setAttendanceRange] = useState<{ min: number, max: number }>({ min: 0, max: 0 })
    const [gradeRange, setGradeRange] = useState<{ min: number, max: number }>({ min: 0, max: 0 })
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<Error | null>(null)

    // Function to fetch all data
    const fetchData = async () => {
        setIsLoading(true)
        setError(null)

        try {
            // Pass params to API calls if needed
            const [studentsResult, statusCountsResult, gradeCountsResult, attendanceRangeResult, gradeRangeResult] =
                await Promise.all([
                    getStudentsData(params),
                    getStatusCounts(),
                    getGradeCounts(),
                    getAttendanceRange(),
                    getGradeRange(),
                ])

            setData(studentsResult.data)
            setPageCount(studentsResult.pageCount)
            setStatusCounts(statusCountsResult)
            setGradeCounts(gradeCountsResult)
            setAttendanceRange(attendanceRangeResult)
            setGradeRange(gradeRangeResult)
        } catch (err) {
            console.error("Error fetching students data:", err)
            setError(err instanceof Error ? err : new Error("Failed to fetch students data"))
        } finally {
            setIsLoading(false)
        }
    }

    // Fetch data when params change
    useEffect(() => {
        fetchData()
    }, [params])

    return {
        data,
        pageCount,
        statusCounts,
        gradeCounts,
        attendanceRange,
        gradeRange,
        isLoading,
        error,
        refetch: fetchData,
    }
}

export function studentsView() {
    const [views, setViews] = useState<View[]>()
    const [isViewLoading, setIsViewLoading] = useState(true)
    const [viewError, setViewError] = useState<Error | null>(null)


    const fetchData = async () => {
        setIsViewLoading(true)
        setViewError(null)
        try {
            const result = await getStudentsViews()
            setViews(result)
        }
        catch (err) {
            toast.error("Failed to fetch students data", {
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
