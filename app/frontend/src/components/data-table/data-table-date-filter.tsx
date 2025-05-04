"use client"

import type { Column } from "@tanstack/react-table"
import { CalendarIcon, XCircle } from "lucide-react"
import * as React from "react"
import type { DateRange } from "react-day-picker"
import { format } from "date-fns"

import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"
import { useFilters } from "@/utils/filter-context"
import { DataTableFilterOption } from "@/types"

type DateSelection = Date[] | DateRange

function getIsDateRange(value: DateSelection): value is DateRange {
  return value && typeof value === "object" && !Array.isArray(value)
}

function parseAsDate(timestamp: number | string | undefined): Date | undefined {
  if (!timestamp) return undefined
  const numericTimestamp = typeof timestamp === "string" ? Number(timestamp) : timestamp
  const date = new Date(numericTimestamp)
  return !Number.isNaN(date.getTime()) ? date : undefined
}

interface DataTableDateFilterProps<TData> {
  column: Column<TData, unknown>
  title?: string
  setSelectedOptions: React.Dispatch<
    React.SetStateAction<DataTableFilterOption<TData>[]>
  >
  multiple?: boolean
}

export function DataTableDateFilter<TData>({ column, title, setSelectedOptions, multiple = true }: DataTableDateFilterProps<TData>) {
  const { removeFilter, getFilter, debouncedAddFilter } = useFilters()

  const columnFilterValue = getFilter(column?.id);
  const [open, setOpen] = React.useState(true)

  const selectedDates = React.useMemo<DateSelection>(() => {
    if (!columnFilterValue) {
      return multiple ? { from: undefined, to: undefined } : []
    }

    if (multiple && columnFilterValue.range) {
      return {
        from: parseAsDate(columnFilterValue.range.min),
        to: parseAsDate(columnFilterValue.range.max),
      }
    }

    const date = parseAsDate(columnFilterValue.value as number)
    return date ? [date] : []
  }, [columnFilterValue, multiple])

  const onSelect = React.useCallback(
    (date: Date | DateRange | undefined) => {
      if (!date) {
        removeFilter(column.id);
        return
      }

      if (multiple && !("getTime" in date)) {
        const from = date.from?.getTime()
        const to = date.to?.getTime()
        debouncedAddFilter({
          id: column.id,
          variant: column.columnDef.meta?.variant,
          tableId: column.columnDef.meta?.tableId ?? getFilter(column.id)?.tableId ?? "",
          operator: "isBetween",
          range: {
            min: from && from !== to ? from : undefined,
            max: to && to !== from ? to : undefined,
          },
        })
      } else if (!multiple && "getTime" in date) {
        debouncedAddFilter({
          id: column.id,
          variant: column.columnDef.meta?.variant,
          tableId: column.columnDef.meta?.tableId ?? "",
          value: date.getTime(),
        })
      }
    },
    [column, multiple],
  )

  const onReset = React.useCallback(
    (event: React.MouseEvent) => {
      event.stopPropagation()
      removeFilter(column.id);
      setOpen(false);
      setSelectedOptions((prev) =>
        prev.filter((item) => item.value !== column?.id)
      );
    },
    [column],
  )

  const hasValue = React.useMemo(() => {
    if (multiple) {
      if (!getIsDateRange(selectedDates)) return false
      return selectedDates.from || selectedDates.to
    }
    if (!Array.isArray(selectedDates)) return false
    return selectedDates.length > 0
  }, [multiple, selectedDates])

  const formatDateRange = React.useCallback((range: DateRange) => {
    if (!range.from && !range.to) return ""
    if (range.from && range.to) {
      return `${format(range.from, "LLL dd, y")} - ${format(range.to, "LLL dd, y")}`
    }
    return format(range.from ?? range.to ?? new Date(), "LLL dd, y")
  }, [])

  const label = React.useMemo(() => {
    if (multiple) {
      if (!getIsDateRange(selectedDates)) return null

      const hasSelectedDates = selectedDates.from || selectedDates.to
      const dateText = hasSelectedDates ? formatDateRange(selectedDates) : "Select date range"

      return (
        <span className="flex items-center gap-2">
          <span>{title}</span>
          {hasSelectedDates && (
            <>
              <Separator orientation="vertical" className="mx-0.5 data-[orientation=vertical]:h-4" />
              <span>{dateText}</span>
            </>
          )}
        </span>
      )
    }

    if (getIsDateRange(selectedDates)) return null

    const hasSelectedDate = selectedDates.length > 0
    const dateText = hasSelectedDate ? format(selectedDates[0], "LLL dd, y") : "Select date"

    return (
      <span className="flex items-center gap-2">
        <span>{title}</span>
        {hasSelectedDate && (
          <>
            <Separator orientation="vertical" className="mx-0.5 data-[orientation=vertical]:h-4" />
            <span>{dateText}</span>
          </>
        )}
      </span>
    )
  }, [selectedDates, multiple, formatDateRange, title])

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" className="border-dashed">
          {hasValue ? (
            <div
              role="button"
              aria-label={`Clear ${title} filter`}
              tabIndex={0}
              onClick={onReset}
              className="rounded-sm opacity-70 transition-opacity hover:opacity-100 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            >
              <XCircle className="mr-2 h-4 w-4" />
            </div>
          ) : (
            <CalendarIcon className="mr-2 h-4 w-4" />
          )}
          {label}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0" align="start">
        {multiple ? (
          <Calendar
            initialFocus
            mode="range"
            selected={getIsDateRange(selectedDates) ? selectedDates : { from: undefined, to: undefined }}
            onSelect={onSelect}
            numberOfMonths={2}
            defaultMonth={getIsDateRange(selectedDates) && selectedDates.from ? selectedDates.from : undefined}
          />
        ) : (
          <Calendar
            initialFocus
            mode="single"
            selected={!getIsDateRange(selectedDates) ? selectedDates[0] : undefined}
            onSelect={onSelect}
          />
        )}
      </PopoverContent>
    </Popover>
  )
}
