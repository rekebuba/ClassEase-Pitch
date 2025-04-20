"use client"

import * as React from "react"
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
import { useSearchParams } from "react-router-dom" // Import useSearchParams from react-router-dom

import {
  getStudentsData,
  getStatusCounts,
  getGradeCounts,
  getAttendanceRange,
  getGradeRange,
} from "@/pages/admin/AdminManageStud";

import type { Student } from "@/lib/types"
import type { DataTableRowAction } from "@/types/data-table"
import { useEffect, useState } from "react"
import { useFeatureFlags } from "./feature-flags-provider"
import { useQueryState } from "nuqs"

export function StudentsTable() {
  const [search, setSearch] = useQueryState('search') // from nuqs
  const { enableAdvancedFilter, filterFlag } = useFeatureFlags()
  const [rowAction, setRowAction] = React.useState<DataTableRowAction<Student> | null>(null)

  const [data, setData] = useState<Student[]>([])
  const [pageCount, setPageCount] = useState(0)
  const [statusCounts, setStatusCounts] = useState<Record<string, number>>({})
  const [gradeCounts, setGradeCounts] = useState<Record<string, number>>({})
  const [attendanceRange, setAttendanceRange] = useState<[number, number]>([0, 0])
  const [gradeRange, setGradeRange] = useState<[number, number]>([0, 0])

  useEffect(() => {
    console.log("search", search)

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
  }, [search, rowAction, filterFlag])


  const columns = React.useMemo(() =>
    getStudentsTableColumns({
      statusCounts,
      gradeCounts,
      attendanceRange,
      gradeRange,
      setRowAction,
    }),
    [statusCounts, gradeCounts, attendanceRange, gradeRange],
  )

  const { table, shallow, debounceMs, throttleMs } = useDataTable({
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
                throttleMs={throttleMs}
                align="start"
                setSearchParams={setSearch}
              />
            ) : (
              <DataTableFilterMenu
                table={table}
                shallow={shallow}
                debounceMs={debounceMs}
                throttleMs={throttleMs} />
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
