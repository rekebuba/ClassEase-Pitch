"use client"

import * as React from "react"
import { useQueryState, parseAsStringEnum, useQueryStates } from "nuqs"

import {
  DataTable,
  DataTableAdvancedToolbar,
  DataTableFilterList,
  DataTableFilterMenu,
  DataTableSkeleton,
  DataTableSortList,
  DataTableToolbar,
} from "@/components/data-table"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"

import { useDataTable } from "@/hooks/use-data-table"
import { getStudentsTableColumns } from "./student-table-columns"
import { UpdateStudentSheet } from "./update-student-sheet"
import { DeleteStudentsDialog } from "./delete-students-dialog"
import { StudentsTableActionBar } from "./students-table-action-bar"
import { getFiltersStateParser } from "@/lib/parsers"
import { useStudentsData, studentsView } from "@/hooks/use-students-data"

import type { Student } from "@/lib/types"
import type { DataTableRowAction, ExtendedColumnSort } from "@/types/data-table"
import { searchParamMap, SearchParamMapSchema, searchParamsCache, type SearchParams } from "@/lib/validations"
import { useLocation } from "react-router-dom"
import { z, ZodError } from "zod"
import { ShieldMoonRounded } from "@mui/icons-material"
import { toast } from "sonner"
import { TableInstanceProvider } from "@/components/data-table"
import { FilterProvider } from "@/utils/filter-context"


// Constants
const INITIAL_SORTING = [{ id: "name", desc: true }]
const COLUMN_PINNING = { right: ["actions"] }

export function StudentsTable() {
  const [rowAction, setRowAction] = React.useState<DataTableRowAction<Student> | null>(null)
  // Search params state with debouncing
  const [debouncedParams, setDebouncedParams] = React.useState<SearchParams | null>(null)

  // Data fetching with the custom hook
  const {
    data,
    pageCount,
    statusCounts,
    gradeCounts,
    attendanceRange,
    gradeRange,
    isLoading,
    error,
    refetch
  } = useStudentsData(debouncedParams)
  const {
    views,
    isViewLoading,
    viewError
  } = studentsView()

  // Memoized columns
  const columns = React.useMemo(
    () =>
      getStudentsTableColumns({
        statusCounts,
        gradeCounts,
        attendanceRange,
        gradeRange,
        setRowAction,
      }),
    [statusCounts, gradeCounts, attendanceRange, gradeRange],
  )

  // Table setup
  const { table, shallow, debounceMs, throttleMs, perPage } = useDataTable({
    data,
    columns,
    pageCount,
    initialState: {
      sorting: INITIAL_SORTING as ExtendedColumnSort<Student>[],
      columnPinning: COLUMN_PINNING,
    },
    getRowId: (originalRow) => originalRow.id,
    shallow: false,
    clearOnDefault: true,
  })
  const [searchParams, setSearchParams] = useQueryStates(searchParamMap);

  const columnIds = React.useMemo(() => {
    return table
      .getAllColumns()
      .filter((column) => column.columnDef.enableColumnFilter)
      .map((column) => column.id)
  }, [table])


  // Filter out empty values
  const filteredParams = Object.fromEntries(
    Object.entries(searchParams).filter(
      ([_, value]) =>
        value !== undefined &&
        value !== null &&
        value !== "" &&
        !(Array.isArray(value) && value.length === 0)
    )
  );

  // Effect to update search params with debouncing
  React.useEffect(() => {
    try {
      const validQuery = searchParamsCache.parse(filteredParams)
      console.log("validQuery", validQuery)
      setDebouncedParams((prev) => (JSON.stringify(prev) !== JSON.stringify(validQuery) ? validQuery : prev))
    } catch (error) {
      // Zod validation error
      if (error instanceof ZodError) {
        console.error("Validation error:", error.flatten()) // Log the error instead of returning it
        toast.error("Validation error", {
          description: "Invalid search parameters",
          style: { color: 'red' }
        });
      }
    }
    return
  }, [searchParams])

  // console.log("debouncedParams", debouncedParams)

  // Handle sheet/dialog close
  const handleCloseAction = React.useCallback(() => {
    setRowAction(null)
  }, [])

  // Handle delete success
  const handleDeleteSuccess = React.useCallback(() => {
    rowAction?.row.toggleSelected(false)
    refetch()
  }, [rowAction, refetch])

  // Render error state
  if (error || viewError) {
    return (
      <Alert variant="destructive" className="my-4">
        <AlertTitle>Error loading students data</AlertTitle>
        <AlertDescription className="flex flex-col gap-2">
          <p>There was a problem loading the student data. Please try again.</p>
          <Button variant="outline" size="sm" onClick={() => refetch()} className="w-fit">
            Retry
          </Button>
        </AlertDescription>
      </Alert>
    )
  }

  return (
    <>
      <FilterProvider columnIds={columnIds}>
        <TableInstanceProvider table={table}>
          <DataTable
            table={table}
            actionBar={<StudentsTableActionBar table={table} />}
          >
            <DataTableAdvancedToolbar views={views} searchParams={filteredParams} setSearchParams={setSearchParams}>
              <DataTableSortList table={table} align="start" />
              <DataTableFilterList
                table={table}
                shallow={shallow}
                debounceMs={debounceMs}
                throttleMs={throttleMs}
                align="start"
              />
              {/* <TasksTableToolbarActions table={table} /> */}
            </DataTableAdvancedToolbar>
          </DataTable>
        </TableInstanceProvider>
      </FilterProvider>

      <UpdateStudentSheet
        open={rowAction?.variant === "update"}
        onOpenChange={handleCloseAction}
        student={rowAction?.row.original ?? null}
        onSuccess={refetch}
      />

      <DeleteStudentsDialog
        open={rowAction?.variant === "delete"}
        onOpenChange={handleCloseAction}
        students={rowAction?.row.original ? [rowAction?.row.original] : []}
        showTrigger={false}
        onSuccess={handleDeleteSuccess}
      />
    </>
  )
}
