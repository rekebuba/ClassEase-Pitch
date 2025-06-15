"use client"

import type { Column } from "@tanstack/react-table"
import { Search, X } from "lucide-react"

import { Button } from "@/components/ui/button"
import * as React from "react"
import { useFilters } from "@/utils/filter-context"
import { dataTableConfig } from "@/config/data-table"
import { useState } from "react"
import type { DataTableFilterOption } from "@/types"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"

interface DataTableInputFilterProps<TData, TValue> {
    column: Column<TData, TValue>
    title: string
    setSelectedOptions: React.Dispatch<React.SetStateAction<DataTableFilterOption<TData>[]>>,
    onFilterChange?: (value: any) => void,
    isActive?: boolean
}

export function DataTableInputFilter<TData, TValue>({
    column,
    title,
    setSelectedOptions,
    onFilterChange,
    isActive
}: DataTableInputFilterProps<TData, TValue>) {
    const { getFilter } = useFilters()
    const columnFilter = getFilter(column?.id)
    const textFilterValue = columnFilter?.value as string | undefined

    const [filterValue, setFilterValue] = React.useState(textFilterValue ?? "")
    const [isFocused, setIsFocused] = React.useState(false)

    const comparisonOperators = dataTableConfig.textOperators

    const operator = comparisonOperators.find((operator) => operator.value === columnFilter?.id) ?? comparisonOperators[0]

    const [selectedOperator, setSelectedOperator] = useState<string>(operator.value)

    const handleValueChange = (value: string) => {
        setFilterValue(value)
        onFilterChange?.({ value: value, operator: selectedOperator })
    }

    const clearFilter = () => {
        handleValueChange("")
    }

    // const onOperatorSelect = React.useCallback(
    //     (value: string) => {
    //         if (!column) return
    //         setSelectedOperator(value)

    //         if (selectedText) {
    //             addFilter({
    //                 id: column.id,
    //                 variant: column.columnDef.meta?.variant,
    //                 tableId: column.columnDef.meta?.tableId ?? getFilter(column.id)?.tableId,
    //                 value: selectedText,
    //                 operator: value,
    //             })
    //         }
    //     },
    //     [column, addFilter, selectedText],
    // )

    return (
        <div className="relative">
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
                <Input
                    type="text"
                    placeholder={`Filter by ${title.toLowerCase()}...`}
                    value={filterValue}
                    onChange={(e) => handleValueChange(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    className={cn(
                        "h-9 w-[180px] pl-9 transition-all duration-200",
                        isActive && filterValue && "ring-2 ring-blue-500/20 border-blue-300",
                        isFocused && "ring-2 ring-blue-500/20",
                    )}
                />
                {filterValue && (
                    <Button
                        variant="ghost"
                        size="sm"
                        className="absolute right-2 top-1/2 -translate-y-1/2 h-5 w-5 p-0 hover:bg-red-100 hover:text-red-600"
                        onClick={clearFilter}
                    >
                        <X className="h-3 w-3" />
                    </Button>
                )}
            </div>
        </div>
    )
}
