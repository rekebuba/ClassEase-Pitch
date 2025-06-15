"use client";

import * as React from "react";

import { cn } from "@/lib/utils";
// import { View } from "@/lib/validations";
import { PlusIcon } from "@radix-ui/react-icons"
import UpdateViewForm from "./views/update-view-form";

import { DataTableFilterOption } from "@/types";
import type { Column } from "@tanstack/react-table";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import {
    DataTableColumnsVisibility,
    useTableInstanceContext,
    DataTableDateFilter,
    DataTableFacetedFilter,
    DataTableInputFilter,
    DataTableSliderFilter,
    DataTableFilterCombobox,
} from "@/components/data-table";
import { CreateViewPopover, DataTableViewsDropdown } from "@/components/data-table/views";
import { SearchParams } from "@/lib/types";
import { Data } from "@dnd-kit/core";
import { Card } from "../ui/card";
import { ChevronDown, Filter, RotateCcw, Search, X } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Badge } from "../ui/badge";
import { useFilters } from "@/utils/filter-context";


interface DataTableSimpleFilterProps {
    searchParams: SearchParams;
}


export function DataTableSimpleFilter({ searchParams }: DataTableSimpleFilterProps) {
    const { tableInstance: table } = useTableInstanceContext()

    const columns = React.useMemo(() => table.getAllColumns().filter((column) => column.getCanFilter()), [table])

    const options = React.useMemo<DataTableFilterOption[]>(() => {
        return columns.map((column) => {
            const columnMeta = column.columnDef.meta
            return {
                id: crypto.randomUUID(),
                label: columnMeta?.label ?? "",
                variant: columnMeta?.variant ?? "default",
                value: column.id,
                options: columnMeta?.options ?? [],
            }
        })
    }, [columns])

    const [activeFilterId, setActiveFilterId] = React.useState<string | null>(() =>
        options.length > 0 ? options[0].value : null,
    )

    const { filters, addFilter, removeFilter, clearFilters, getFilter, debouncedAddFilter } = useFilters()

    const [appliedFilters, setAppliedFilters] = React.useState<Record<string, any>>(() => {
        const initialFilters: Record<string, any> = {}
        options.forEach((option) => {
            if (searchParams[option.value] !== undefined && searchParams[option.value] !== "") {
                initialFilters[option.value] = searchParams[option.value]
            }
        })
        return initialFilters
    })

    const [isExpanded, setIsExpanded] = React.useState(false)

    const activeFilterOption = React.useMemo(
        () => options.find((option) => option.value === activeFilterId),
        [options, activeFilterId],
    )

    const handleFilterTypeChange = React.useCallback((newFilterId: string) => {
        setActiveFilterId(newFilterId)
        setIsExpanded(false)
    }, [])

    const handleFilterValueChange = React.useCallback(
        (value: any) => {
            if (!activeFilterId) return

            setAppliedFilters((prev) => {
                if (prev[activeFilterId] === value) return prev

                return {
                    ...prev,
                    [activeFilterId]: value,
                }
            })
        },
        [activeFilterId],
    )

    const resetFilters = React.useCallback(() => {
        setAppliedFilters({})
        clearFilters()
        // columns.forEach((column) => {
        //     const tableColumn = table.getColumn(column.id)
        //     if (tableColumn && typeof tableColumn.setFilterValue === "function") {
        //     }
        // })
    }, [columns, table])

    const removeFilterBadges = React.useCallback(
        (columnId: string) => {
            setAppliedFilters((prev) => {
                const newFilters = { ...prev }
                delete newFilters[columnId]
                return newFilters
            })

            const tableColumn = table.getColumn(columnId)
            if (tableColumn && typeof tableColumn.setFilterValue === "function") {
                removeFilter(tableColumn?.id)
            }
        },
        [table],
    )

    React.useEffect(() => {
        const timeoutId = setTimeout(() => {
            Object.entries(appliedFilters).forEach(([columnId, value]) => {
                const column = table.getColumn(columnId)
                const columnFilter = getFilter(column?.id)
                console.log("columnFilter:", columnFilter)

                if (column && typeof column.setFilterValue === "function") {
                    if (
                        value?.value === undefined ||
                        value?.value === null ||
                        value?.value === "" ||
                        (Array.isArray(value?.value) && value.value.length === 0)
                    ) {
                        removeFilter(column.id)
                    } else {
                        debouncedAddFilter({
                            id: column.id,
                            value: value?.value,
                            variant: column.columnDef.meta?.variant,
                            tableId: column.columnDef.meta?.tableId ?? getFilter(column.id)?.tableId,
                            operator: value?.operator,
                        })
                    }
                }
            })
        }, 0)

        return () => clearTimeout(timeoutId)
    }, [appliedFilters, table])

    const hasActiveFilters = React.useMemo(
        () => Object.values(appliedFilters).some((value) => value && value !== ""),
        [appliedFilters],
    )

    const activeFilterBadges = React.useMemo(
        () =>
            Object.entries(appliedFilters)
                .filter(([_, value]) => value && value !== "")
                .map(([columnId, value]) => {
                    const option = options.find((opt) => opt.value === columnId)
                    return {
                        columnId,
                        operator: value?.operator,
                        value: value?.value,
                        label: option?.label || columnId,
                        variant: option?.variant || "default",
                    }
                }),
        [appliedFilters, options],
    )

    return (
        <Card className="p-4 bg-gradient-to-r from-slate-50 to-gray-50 border-0 shadow-sm">
            <div className="space-y-4">
                {/* Main Filter Controls */}
                <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2">
                        <Filter className="h-4 w-4 text-muted-foreground" />
                        <span className="text-sm font-medium text-muted-foreground">Filter by:</span>
                    </div>

                    {/* Filter Type Selector */}
                    <Select value={activeFilterId || ""} onValueChange={handleFilterTypeChange}>
                        <SelectTrigger className="h-9 w-[150px] bg-white border-2 hover:border-blue-300 transition-colors">
                            <SelectValue placeholder="Select filter" />
                        </SelectTrigger>
                        <SelectContent>
                            {options.map((option) => (
                                <SelectItem key={option.value} value={option.value}>
                                    <div className="flex items-center gap-2">
                                        <div
                                            className={cn(
                                                "w-2 h-2 rounded-full",
                                                option.variant === "select" && "bg-blue-500",
                                                option.variant === "number" && "bg-green-500",
                                                option.variant === "date" && "bg-purple-500",
                                                option.variant === "default" && "bg-gray-500",
                                            )}
                                        />
                                        {option.label}
                                    </div>
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>

                    {/* Active Filter Input */}
                    {activeFilterOption && (
                        <DataTableToolbarFilter
                            key={activeFilterOption.value}
                            column={table.getColumn(activeFilterOption.value)}
                            filterOption={activeFilterOption}
                            onFilterChange={handleFilterValueChange}
                            isActive={!!appliedFilters[activeFilterOption.value]}
                        />
                    )}

                    {/* Reset Button */}
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={resetFilters}
                        disabled={!hasActiveFilters}
                        className="h-9 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition-colors"
                    >
                        <RotateCcw className="h-3.5 w-3.5 mr-1.5" />
                        Reset
                    </Button>
                </div>

                {/* Applied Filters */}
                {activeFilterBadges.length > 0 && (
                    <div className="space-y-2">
                        <div className="flex items-center gap-2">
                            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                                Active Filters ({activeFilterBadges.length})
                            </span>
                            <div className="flex-1 h-px bg-border" />
                        </div>

                        <div className="flex flex-wrap gap-2">
                            {activeFilterBadges.map(({ columnId, operator, value, label, variant }) => (
                                <Badge
                                    key={columnId}
                                    variant="secondary"
                                    className={cn(
                                        "group flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium transition-all duration-200 hover:scale-105",
                                        variant === "select" && "bg-blue-100 text-blue-800 hover:bg-blue-200",
                                        variant === "number" && "bg-green-100 text-green-800 hover:bg-green-200",
                                        variant === "date" && "bg-purple-100 text-purple-800 hover:bg-purple-200",
                                        variant === "default" && "bg-gray-100 text-gray-800 hover:bg-gray-200",
                                    )}
                                >
                                    <div
                                        className={cn(
                                            "w-1.5 h-1.5 rounded-full",
                                            variant === "select" && "bg-blue-500",
                                            variant === "number" && "bg-green-500",
                                            variant === "date" && "bg-purple-500",
                                            variant === "default" && "bg-gray-500",
                                        )}
                                    />
                                    <span className="font-medium">{label}</span>
                                    <span className="max-w-[100px] truncate">{`(${operator}) : ${value}`}</span>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        className="h-4 w-4 p-0 ml-1 opacity-60 hover:opacity-100 hover:bg-red-100 hover:text-red-600 group-hover:opacity-100"
                                        onClick={() => removeFilterBadges(columnId)}
                                    >
                                        <X className="h-2.5 w-2.5" />
                                    </Button>
                                </Badge>
                            ))}
                        </div>
                    </div>
                )}

                {/* Empty State */}
                {!hasActiveFilters && (
                    <div className="text-center py-4">
                        <div className="inline-flex items-center gap-2 text-sm text-muted-foreground">
                            <Search className="h-4 w-4" />
                            <span>No filters applied. Select a filter type above to get started.</span>
                        </div>
                    </div>
                )}
            </div>
        </Card>
    )
}


interface DataTableToolbarFilterProps<TData> {
    column: Column<TData>
    setSelectedOptions: React.Dispatch<React.SetStateAction<DataTableFilterOption[]>>
    onFilterChange?: (value: any) => void
    isActive?: boolean
}


export function DataTableToolbarFilter<TData>({
    column,
    setSelectedOptions,
    onFilterChange,
    isActive = false,
}: DataTableToolbarFilterProps<TData>) {
    const columnMeta = column.columnDef.meta;
    const onFilterRender = React.useCallback(() => {
        const commonProps = {
            column,
            setSelectedOptions,
            onFilterChange,
            isActive,
        }
        if (!columnMeta?.variant) return null;

        switch (columnMeta.variant) {
            case "text":
                return (
                    <DataTableInputFilter
                        {...commonProps}
                        title={columnMeta.label ?? column.id}
                    >
                    </DataTableInputFilter>
                );

            case "number":
                return (
                    <div className="relative">
                        <Input
                            type="number"
                            inputMode="numeric"
                            placeholder={columnMeta.placeholder ?? columnMeta.label}
                            value={(column.getFilterValue() as string) ?? ""}
                            onChange={(event) => column.setFilterValue(event.target.value)}
                            className={cn("h-8 w-[120px]", columnMeta.unit && "pr-8")}
                        />
                        {columnMeta.unit && (
                            <span className="absolute top-0 right-0 bottom-0 flex items-center rounded-r-md bg-accent px-2 text-muted-foreground text-sm">
                                {columnMeta.unit}
                            </span>
                        )}
                    </div>
                );

            case "range":
                return (
                    <DataTableSliderFilter
                        column={column}
                        title={columnMeta.label ?? column.id}
                        setSelectedOptions={setSelectedOptions}
                    />
                );

            case "date":
            case "dateRange":
                return (
                    <DataTableDateFilter
                        column={column}
                        title={columnMeta.label ?? column.id}
                        setSelectedOptions={setSelectedOptions}
                        multiple={columnMeta.variant === "dateRange"}
                    />
                );

            case "select":
            case "multiSelect":
                return (
                    <DataTableFacetedFilter
                        {...commonProps}
                        title={columnMeta.label ?? column.id}
                        options={columnMeta.options ?? []}
                        multiple={columnMeta.variant === "multiSelect"}
                    />
                );

            default:
                return null;
        }
    }, [column, columnMeta, onFilterChange, setSelectedOptions, isActive]);

    return onFilterRender();
}
