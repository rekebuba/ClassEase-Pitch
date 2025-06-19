"use client"

import type { Column } from "@tanstack/react-table"
import { Search, X } from "lucide-react"

import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button"
import * as React from "react"
import { useFilters } from "@/utils/filter-context"
import { dataTableConfig } from "@/config/data-table"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { DataTableSliderFilter } from "./data-table-slider-filter";

interface DataTableInputFilterProps<TData, TValue> {
    column: Column<TData, TValue>
    title: string
    onFilterChange?: (value: any) => void,
    isActive?: boolean
    isAdvancedMode?: boolean
    type: "text" | "number" | "range"
}

export function DataTableInputFilter<TData, TValue>({
    column,
    title,
    onFilterChange,
    isActive,
    isAdvancedMode,
    type
}: DataTableInputFilterProps<TData, TValue>) {
    const { getFilter } = useFilters()
    const columnFilter = getFilter(column?.id)
    const textFilterValue = columnFilter?.value

    const filterValue = textFilterValue ?? (type === "range" || type === "number" ? 0 : "")
    const [isFocused, setIsFocused] = React.useState(false)

    const comparisonOperators = type === "text" ? dataTableConfig.textOperators : dataTableConfig.numericOperators;

    const selectedOperator = columnFilter?.operator || comparisonOperators[0].value;

    const defaultRange = column.columnDef.meta?.range;
    const unit = column.columnDef.meta?.unit;

    const handleValueChange = React.useCallback((value: String | Number, operator: String) => {
        if (defaultRange?.max && (type === "range" || type === "number") && value >= defaultRange.max) {
            value = defaultRange.max;
        }
        console.log("handleValueChange", value, operator)
        onFilterChange?.({ value, operator })
    }, [filterValue, selectedOperator, onFilterChange],
    );

    return (
        <>
            {isAdvancedMode && (
                <Select value={selectedOperator} onValueChange={operator => handleValueChange(filterValue, operator)}>
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
            {(selectedOperator !== "isBetween" &&
                selectedOperator !== "isNotBetween" &&
                selectedOperator !== "isEmpty" &&
                selectedOperator !== "isNotEmpty"
            ) ? (
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
                    <Input
                        type={(type === "range" || type === "number") ? "number" : type}
                        placeholder={`Filter by ${title.toLowerCase()}...`}
                        value={defaultRange?.max ? (defaultRange?.max > filterValue ? filterValue : defaultRange?.max) : filterValue}
                        onChange={(e) => handleValueChange((type === "range" || type === "number") ? Number(e.target.value) : e.target.value, selectedOperator)}
                        onFocus={() => setIsFocused(true)}
                        onBlur={() => setIsFocused(false)}
                        max={defaultRange?.max}
                        className={cn(
                            "h-9 w-[180px] pl-9 transition-all duration-200",
                            isActive && filterValue && "ring-2 ring-blue-500/20 border-blue-300",
                            isFocused && "ring-2 ring-blue-500/20",
                        )}
                    />
                    {unit && (
                        <span className="absolute top-0 right-0 bottom-0 flex items-center rounded-r-md bg-accent px-3 text-muted-foreground text-sm">
                            {unit}
                        </span>
                    )}
                    {filterValue ? (
                        <Button
                            variant="ghost"
                            size="sm"
                            className="absolute right-2 top-1/2 -translate-y-1/2 h-5 w-5 p-0 hover:bg-red-100 hover:text-red-600"
                            onClick={() => handleValueChange((type === "range" || type === "number") ? 0 : "", selectedOperator)}
                        >
                            <X className="h-3 w-3" />
                        </Button>
                    ) : null}
                </div>) :
                <DataTableSliderFilter
                    column={column}
                    title={title}
                    onFilterChange={onFilterChange}
                    isActive={isActive}
                    selectedOperator={selectedOperator}
                />
            }
        </>
    )
}
