"use client"

import type { Column } from "@tanstack/react-table"
import { CalendarIcon, X, XCircle } from "lucide-react"
import * as React from "react"
import type { DateRange } from "react-day-picker"
import { format } from "date-fns"

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"
import { useFilters } from "@/utils/filter-context"
import { DataTableFilterOption } from "@/types"
import { on } from "events"
import { cn } from "@/lib/utils"
import { dataTableConfig } from "@/config/data-table"

type DateSelection = Date | Date[] | DateRange

type DateSelectionRange = {
  min: Number | undefined
  max: Number | undefined
}

type DateSelectionValueRange = {
  from: Date | undefined
  to: Date | undefined
}

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
  multiple?: boolean
  onFilterChange?: (value: any) => void,
  isActive?: boolean,
  isAdvancedMode?: boolean
}

export function DataTableDateFilter<TData>({
  column,
  title,
  onFilterChange,
  isActive,
  multiple = true,
  isAdvancedMode
}: DataTableDateFilterProps<TData>) {
  const { removeFilter, getFilter } = useFilters()

  const columnFilterValue = getFilter(column?.id);

  const comparisonOperators = dataTableConfig.dateOperators
  const selectedOperator = columnFilterValue?.operator || comparisonOperators[0].value;

  const selectedDateRange = React.useMemo<DateSelectionValueRange | undefined>(() => {
    if (!columnFilterValue) {
      return multiple ? { from: undefined, to: undefined } : undefined
    }
    if (multiple) {
      return {
        from: parseAsDate(columnFilterValue.value.min),
        to: parseAsDate(columnFilterValue.value.max),
      }
    }
    return undefined
  }, [columnFilterValue, multiple])

  const selectedDate = React.useMemo<Date | undefined>(() => {
    if (!columnFilterValue) {
      return undefined
    }
    if (!multiple) {
      const date = parseAsDate(columnFilterValue.value as number)
      return date ? date : undefined
    }
    return undefined
  }, [columnFilterValue, multiple])

  const selectedDates = React.useMemo<DateSelection>(() => {
    if (!columnFilterValue) {
      return multiple ? { from: undefined, to: undefined } : []
    }

    if (multiple) {
      return {
        from: parseAsDate(columnFilterValue.value.min),
        to: parseAsDate(columnFilterValue.value.max),
      }
    }

    const date = parseAsDate(columnFilterValue.value as number)
    return date ? [date] : []
  }, [columnFilterValue, multiple])

  const onSelect = React.useCallback(
    (date: DateSelectionRange | Number | undefined, operator: String) => {
      onFilterChange?.({
        value: date || "",
        operator,
      })
    },
    [column, multiple],
  )

  const formatDateRange = React.useCallback((range: DateRange) => {
    if (!range.from && !range.to) return ""
    if (range.from && range.to) {
      return `${format(range.from, "LLL dd, y")} - ${format(range.to, "LLL dd, y")}`
    }
    return format(range.from ?? range.to ?? new Date(), "LLL dd, y")
  }, [])

  const label = React.useMemo(() => {
    if (multiple) {
      if (!selectedDateRange) return null

      const hasSelectedDates = selectedDateRange.from || selectedDateRange.to
      const dateText = hasSelectedDates ? formatDateRange(selectedDateRange) : "Select date range"

      return (
        <span className="flex items-center gap-2 mr-5">
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

    const dateText = selectedDate ? format(selectedDate, "LLL dd, y") : "Select date"

    return (
      <span className="flex items-center gap-2 mr-5">
        <span>{title}</span>
        {selectedDate && (
          <>
            <Separator orientation="vertical" className="mx-0.5 data-[orientation=vertical]:h-4" />
            <span>{dateText}</span>
          </>
        )}
      </span>
    )
  }, [selectedDates, multiple, formatDateRange, title])

  return (
    <>
      {isAdvancedMode && (
        <Select
          value={selectedOperator}
          onValueChange={operator => {
            if (operator === "isBetween" || operator === "isNotBetween") {
              onSelect({
                min: selectedDateRange?.from?.getTime(),
                max: selectedDateRange?.to?.getTime(),
              }, operator);
              return;
            }
            onSelect(selectedDate?.getTime(), operator);
            return;
          }}
        >
          <SelectTrigger className="h-9 w-[150px] bg-white border-2 hover:border-blue-300 transition-colors">
            <SelectValue placeholder={selectedOperator} />
          </SelectTrigger>
          <SelectContent>
            {comparisonOperators.map(({ value, label }) => (
              <SelectItem key={value} value={value}>
                {label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      )}

      <Popover>
        <PopoverTrigger asChild>
          <div className="relative">
            <div className="relative">
              <Button variant="outline" size="sm" className={cn(
                "h-9 min-w-[180px] pl-3 transition-all duration-200",
                isActive && selectedDates && "ring-2 ring-blue-500/20 border-blue-300"
              )}>
                <CalendarIcon className="h-4 w-4" />
                {label}
              </Button>
            </div>
            {selectedDates && (
              <Button
                variant="ghost"
                size="sm"
                className="absolute right-2 top-1/2 -translate-y-1/2 h-5 w-5 p-0 hover:bg-red-100 hover:text-red-600"
                onClick={() => onFilterChange?.(null)}
              >
                <X className="h-3 w-3" />
              </Button>
            )}
          </div>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          {multiple ? (
            <Calendar
              initialFocus
              mode="range"
              selected={
                columnFilterValue?.value.min || columnFilterValue?.value.max
                  ? {
                    from: parseAsDate(columnFilterValue?.value.min),
                    to: parseAsDate(columnFilterValue?.value.max),
                  }
                  : undefined
              }
              onSelect={(date) => {
                const from = date?.from?.getTime()
                const to = date?.to?.getTime()
                onSelect({
                  min: from && from !== to ? from : undefined,
                  max: to && to !== from ? to : undefined,
                }, selectedOperator)
              }}
              numberOfMonths={2}
              defaultMonth={parseAsDate(columnFilterValue?.value.min) || undefined}
            />
          ) : (
            <Calendar
              initialFocus
              mode="single"
              selected={parseAsDate(columnFilterValue?.value as number) || undefined}
              onSelect={(date) => onSelect(date?.getTime(), selectedOperator)}
            />
          )}
        </PopoverContent>
      </Popover>
    </>
  )
}
