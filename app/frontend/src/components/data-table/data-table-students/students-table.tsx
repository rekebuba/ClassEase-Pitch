"use client"

import * as React from "react"
import { useQueryState, parseAsStringEnum, useQueryStates, parseAsInteger, parseAsString } from "nuqs"

import {
  DataTable,
  DataTableAdvancedToolbar,
  DataTableColumnsVisibility,
  DataTableFilterList,
  DataTableFilterMenu,
  DataTableSimpleFilter,
  DataTableSkeleton,
  DataTableSortList,
} from "@/components/data-table"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"

import { useDataTable } from "@/hooks/use-data-table"
import { getStudentsTableColumns } from "./student-table-columns"
import { UpdateStudentSheet } from "./update-student-sheet"
import { DeleteStudentsDialog } from "./delete-students-dialog"
import { StudentsTableFloatingBar } from "./students-table-floating-bar"
import { getFiltersStateParser, getSortingStateParser } from "@/lib/parsers"
import { useStudentsData, studentsView } from "@/hooks/use-students-data"

import type { Student, SearchParams } from "@/lib/types"
import type { DataTableRowAction, ExtendedColumnSort } from "@/types/data-table"
import { searchParamsCache } from "@/lib/validations"
import { useLocation } from "react-router-dom"
import { z, ZodError } from "zod"
import { ShieldMoonRounded } from "@mui/icons-material"
import { toast } from "sonner"
import { TableInstanceProvider } from "@/components/data-table"
import { FilterProvider } from "@/utils/filter-context"
import { StudentsTableToolbarActions } from "./student-table-toolbar-action"
import { DataTableViewsDropdown } from "../views"


// Constants
const COLUMN_PINNING = { right: ["actions"] }

export function StudentsTable() {
  const [rowAction, setRowAction] = React.useState<DataTableRowAction<Student> | null>(null)
  // Search params state with debouncing
  const [debouncedParams, setDebouncedParams] = React.useState<SearchParams | null>(null)
  const [columnVisibility, setColumnVisibility] = React.useState({});

  // Data fetching with the custom hook
  const {
    data,
    pageCount,
    tableId,
    statusCounts,
    gradeCounts,
    sectionCounts,
    averageRange,
    isLoading,
    error,
    refetch
  } = useStudentsData(debouncedParams)
  const {
    views,
    isViewLoading,
    viewError,
    refetchViews
  } = studentsView()

  // Memoized columns
  const columns = React.useMemo(
    () =>
      getStudentsTableColumns({
        tableId,
        statusCounts,
        gradeCounts,
        sectionCounts,
        averageRange,
        setRowAction,
      }),
    [statusCounts, gradeCounts, averageRange],
  )

  // Table setup
  const { table } = useDataTable({
    data,
    columns,
    pageCount,
    initialState: {
      columnPinning: COLUMN_PINNING,
      columnVisibility: {
        // Hide Student Id column
        identification: false,
        sectionSemesterOne: false,
        sectionSemesterTwo: false,
        averageSemesterOne: false,
        averageSemesterTwo: false,
        rankSemesterOne: false,
        rankSemesterTwo: false,
        guardianPhone: false,
      },
    },
    getRowId: (originalRow) => originalRow.identification,
    shallow: false,
    clearOnDefault: true,
  })

  const searchParamMap = {
    page: parseAsInteger.withDefault(1),
    perPage: parseAsInteger.withDefault(10),
    sort: getSortingStateParser().withDefault([]),
    filters: getFiltersStateParser().withDefault([]),
    joinOperator: parseAsStringEnum(["and", "or"]).withDefault("and"),
  }

  const [searchParams, setSearchParams] = useQueryStates(searchParamMap);
  const columnIds = React.useMemo(() => {
    return table
      .getAllColumns()
      .filter((column) => column.columnDef.enableColumnFilter)
      .map((column) => column.id)
  }, [table])

  // Filter out empty values
  const filteredParams = Object.entries(searchParams || {}).reduce(
    (acc, [key, value]) => {
      if (key === "filters" && Array.isArray(value)) {
        const cleanedFilters = value.filter(
          (filter) =>
            !(typeof filter.value === "string" && filter.value === "") &&
            !(Array.isArray(filter.value) && filter.value.length === 0)
        );
        if (cleanedFilters.length > 0) {
          acc[key] = cleanedFilters;
        }
      } else if (
        !(
          typeof value === "string" && value === "" ||
          Array.isArray(value) && value.length === 0
        )
      ) {
        acc[key] = value;
      }

      return acc;
    },
    {} as Record<string, any>
  );

  // Effect to update search params with debouncing
  React.useEffect(() => {
    const validQuery = searchParamsCache.safeParse(filteredParams)
    if (!validQuery.success) {
      toast.warning("Invalid search", {
        description: "Please check your search parameters",
      });
      console.error("Invalid search params", validQuery.error)
      return
    }
    // console.log("validQuery", validQuery.data)
    setDebouncedParams((prev) => (JSON.stringify(prev) !== JSON.stringify(validQuery.data) ? validQuery.data : prev))
  }, [searchParams, refetch])

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
            floatingBar={<StudentsTableFloatingBar />}
          >
            <DataTableAdvancedToolbar searchParams={searchParams}>
              <DataTableSortList align="start" />
              <DataTableFilterList align="start" />
              <StudentsTableToolbarActions />
              <DataTableColumnsVisibility table={table} />
            </DataTableAdvancedToolbar>
            <DataTableViewsDropdown views={views} SearchParams={searchParams} setSearchParams={setSearchParams} refetchViews={refetchViews} />
            <DataTableSimpleFilter searchParams={searchParams} />
          </DataTable>
        </TableInstanceProvider>
      </FilterProvider>

      <UpdateStudentSheet
        open={rowAction?.variant === "update"}
        onOpenChange={handleCloseAction}
        student={rowAction?.row.original ?? null}
        onSuccess={refetch}
      />

      {/* <DeleteStudentsDialog
        open={rowAction?.variant === "delete"}
        onOpenChange={handleCloseAction}
        students={rowAction?.row.original ? [rowAction?.row.original] : []}
        showTrigger={false}
        onSuccess={handleDeleteSuccess}
      /> */}
    </>
  )
}
