"use client"

import {
  DataTable,
  DataTableAdvancedToolbar,
  DataTableFilterList,
  DataTableFilterMenu,
  DataTableSortList,
  DataTableToolbar,
} from "@/components/data-table"

import { useDataTable } from "@/hooks/use-data-table"
import { getStudentsTableColumns } from "./student-table-columns"
import { UpdateStudentSheet } from "./update-student-sheet"
import { DeleteStudentsDialog } from "./delete-students-dialog"
import { StudentsTableActionBar } from "./students-table-action-bar"

import {
  getStudentsData,
  getStatusCounts,
  getGradeCounts,
  getAttendanceRange,
  getGradeRange,
} from "@/pages/admin/AdminManageStud";

import type { Student } from "@/lib/types"
import type { DataTableRowAction } from "@/types/data-table"
import { useEffect, useMemo, useState } from "react"
import { useFeatureFlags } from "./feature-flags-provider"
import { parseAsStringEnum, useQueryState } from "nuqs"
import { getFiltersStateParser } from "@/lib/parsers";
import { SearchParams } from "@/lib/validations"

const FILTERS_KEY = "filters";
const JOIN_OPERATOR_KEY = "joinOperator";
export function StudentsTable() {
  const { enableAdvancedFilter, filterFlag } = useFeatureFlags()
  const [rowAction, setRowAction] = useState<DataTableRowAction<Student> | null>(null)

  const [data, setData] = useState<Student[]>([])
  const [pageCount, setPageCount] = useState(0)
  const [statusCounts, setStatusCounts] = useState<Record<string, number>>({})
  const [gradeCounts, setGradeCounts] = useState<Record<string, number>>({})
  const [attendanceRange, setAttendanceRange] = useState<[number, number]>([0, 0])
  const [gradeRange, setGradeRange] = useState<[number, number]>([0, 0])
  const [searchParams, setSearchParams] = useState<SearchParams | null>(null)

  const columns = useMemo(() =>
    getStudentsTableColumns({
      statusCounts,
      gradeCounts,
      attendanceRange,
      gradeRange,
      setRowAction,
    }),
    [statusCounts, gradeCounts, attendanceRange, gradeRange],
  )

  const { table, shallow, debounceMs, throttleMs, page, perPage, sorting } = useDataTable({
    data,
    columns,
    pageCount,
    enableAdvancedFilter,
    initialState: {
      sorting: [{ id: "name", desc: true }],
      columnPinning: { right: ["actions"] },
    },
    getRowId: (originalRow) => originalRow.id,
    shallow: false,
    clearOnDefault: true,
  });

  const [filters, setFilters] = useQueryState(
    FILTERS_KEY,
    getFiltersStateParser(columns.map((field) => field.id).filter((id): id is string => id !== undefined))
      .withDefault([])
      .withOptions({
        clearOnDefault: true,
        shallow,
        throttleMs,
      }),
  );

  const [joinOperator, setJoinOperator] = useQueryState(
    JOIN_OPERATOR_KEY,
    parseAsStringEnum(["and", "or"]).withDefault("and").withOptions({
      clearOnDefault: true,
      shallow,
    }),
  );

  // Effect to update search params - separated from data fetching
  useEffect(() => {
    const params: SearchParams = {
      filterFlag,
      page,
      perPage,
      filters,
      joinOperator,
      sort: sorting,
    }

    // Only update if params have changed
    if (JSON.stringify(searchParams) !== JSON.stringify(params)) {
      setSearchParams(params)
    }
  }, [filterFlag, page, perPage, filters, joinOperator, sorting, searchParams])

  useEffect(() => {
    const fetchData = async () => {
      const [
        { data, pageCount },
        statusCounts,
        gradeCounts,
        attendanceRange,
        gradeRange
      ] = await Promise.all([
        getStudentsData(),
        getStatusCounts(),
        getGradeCounts(),
        getAttendanceRange(),
        getGradeRange()
      ])

      setData(data)
      setPageCount(pageCount)
      setStatusCounts(statusCounts)
      setGradeCounts(gradeCounts)
      setAttendanceRange(attendanceRange)
      setGradeRange(gradeRange)
    }

    fetchData()
  }, [searchParams])

  return (
    <>
      <DataTable
        table={table}
        actionBar={<StudentsTableActionBar table={table} />}
      >
        {enableAdvancedFilter ? (
          <DataTableAdvancedToolbar table={table}>
            <DataTableSortList table={table} align="start" />
            {filterFlag === "advancedFilters" ? (
              <DataTableFilterList
                table={table}
                shallow={shallow}
                debounceMs={debounceMs}
                align="start"
                filters={filters}
                setFilters={setFilters}
                joinOperator={joinOperator}
                setJoinOperator={setJoinOperator}
              />
            ) : (
              <DataTableFilterMenu
                table={table}
                shallow={shallow}
                debounceMs={debounceMs}
                filters={filters}
                setFilters={setFilters}
              />
            )}
          </DataTableAdvancedToolbar>
        ) : (
          <DataTableToolbar table={table}>
            <DataTableSortList table={table} align="end" />
          </DataTableToolbar>
        )}
      </DataTable>
      <UpdateStudentSheet
        open={rowAction?.variant === "update"}
        onOpenChange={() => setRowAction(null)}
        student={rowAction?.row.original ?? null}
      />
      <DeleteStudentsDialog
        open={rowAction?.variant === "delete"}
        onOpenChange={() => setRowAction(null)}
        students={rowAction?.row.original ? [rowAction?.row.original] : []}
        showTrigger={false}
        onSuccess={() => rowAction?.row.toggleSelected(false)}
      />
    </>
  )
}
