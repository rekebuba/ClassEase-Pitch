"use client";

import * as React from "react";

import { cn } from "@/lib/utils";
import { DataTableFilterOption } from "@/types";
import type { Column } from "@tanstack/react-table";

import { Button } from "@/components/ui/button";

import {
  DataTableColumnsVisibility,
  useTableInstanceContext,
  DataTableDateFilter,
  DataTableFacetedFilter,
  DataTableInputFilter,
  DataTableSliderFilter,
  DataTableFilterCombobox,
  DataTableFilterList,
} from "@/components/data-table";
import {
  CreateViewPopover,
  DataTableViewsDropdown,
} from "@/components/data-table/views";
import { SearchParams, StudentsViews, View } from "@/lib/types";
import { Card } from "../ui/card";
import {
  ChevronDown,
  Copy,
  Download,
  Filter,
  RotateCcw,
  Save,
  Search,
  Settings2,
  X,
  Zap,
} from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { Badge } from "../ui/badge";
import { useFilters } from "@/utils/filter-context";
import { Switch } from "../ui/switch";
import { StudentsTableToolbarActions } from "./data-table-students/student-table-toolbar-action";
import { createNewView } from "@/api/adminApi";
import { toast } from "sonner";

interface DataTableSimpleFilterProps {
  searchParams: SearchParams;
  views: StudentsViews[];
  refetchViews: () => void;
  currentViewId: string | null;
  setCurrentViewId: (viewId: string | null) => void;
  setSearchParams: (params: SearchParams) => void;
}

export function DataTableSimpleFilter({
  searchParams,
  views,
  refetchViews,
  currentViewId,
  setCurrentViewId,
  setSearchParams,
}: DataTableSimpleFilterProps) {
  const { tableInstance: table } = useTableInstanceContext();
  // Toggle between simple and advanced mode
  const [isAdvancedMode, setIsAdvancedMode] = React.useState(false);

  const columns = React.useMemo(
    () => table.getAllColumns().filter((column) => column.getCanFilter()),
    [table],
  );

  const options = React.useMemo<DataTableFilterOption[]>(() => {
    return columns.map((column) => {
      const columnMeta = column.columnDef.meta;
      return {
        id: crypto.randomUUID(),
        label: columnMeta?.label ?? "",
        variant: columnMeta?.variant ?? "default",
        value: column.id,
        options: columnMeta?.options ?? [],
      };
    });
  }, [columns]);

  const [activeFilterId, setActiveFilterId] = React.useState<string | null>(
    () => (options.length > 0 ? options[0].value : null),
  );

  const { filters, removeFilter, clearFilters, getFilter, debouncedAddFilter } =
    useFilters();

  const [appliedFilters, setAppliedFilters] = React.useState<
    Record<string, any>
  >(() => {
    const initialFilters: Record<string, any> = {};
    options.forEach((option) => {
      if (
        (searchParams as Record<string, any>)[option.value] !== undefined &&
        (searchParams as Record<string, any>)[option.value] !== ""
      ) {
        initialFilters[option.value] = (searchParams as Record<string, any>)[
          option.value
        ];
      }
    });
    return initialFilters;
  });

  const activeFilterOption = React.useMemo(
    () => options.find((option) => option.value === activeFilterId),
    [options, activeFilterId],
  );

  const handleFilterTypeChange = React.useCallback((newFilterId: string) => {
    setActiveFilterId(newFilterId);
  }, []);

  const handleFilterValueChange = React.useCallback(
    (value: any) => {
      if (!activeFilterId) return;

      setAppliedFilters((prev) => {
        if (prev[activeFilterId] === value) return prev;

        return {
          ...prev,
          [activeFilterId]: value,
        };
      });
    },
    [activeFilterId, isAdvancedMode],
  );

  const resetFilters = React.useCallback(() => {
    setAppliedFilters({});
    clearFilters();
  }, [columns, table]);

  const removeFilterBadges = React.useCallback(
    (columnId: string) => {
      setAppliedFilters((prev) => {
        const newFilters = { ...prev };
        delete newFilters[columnId];
        return newFilters;
      });

      const tableColumn = table.getColumn(columnId);
      if (tableColumn && typeof tableColumn.setFilterValue === "function") {
        removeFilter(tableColumn?.id);
      }
    },
    [table],
  );

  React.useEffect(() => {
    Object.entries(appliedFilters).forEach(([columnId, value]) => {
      const column = table.getColumn(columnId);

      if (column && typeof column.setFilterValue === "function") {
        if (value === null) return removeFilter(columnId);
        debouncedAddFilter({
          id: column.id,
          value: value?.value ?? "",
          variant: column.columnDef.meta?.variant,
          tableId:
            column.columnDef.meta?.tableId ?? getFilter(column.id)?.tableId,
          operator: value?.operator,
        });
      }
    });
  }, [appliedFilters, table]);

  const hasActiveFilters = React.useMemo(() => filters.length > 0, [filters]);

  const activeFilterBadges = React.useMemo(
    () =>
      filters
        .filter(({ value }) => value !== undefined && value !== "")
        .map(({ id, operator, value }) => {
          const column = table.getColumn(id);
          return {
            columnId: id,
            operator,
            value,
            variant: column?.columnDef.meta?.variant || "default",
            label: column?.columnDef?.meta?.label || id,
          };
        }),
    [filters, appliedFilters, options],
  );

  function formatValue(value: unknown): string {
    if (typeof value === "string") return value;

    if (Array.isArray(value)) {
      const sorted = [...value].sort((a, b) => {
        const aNum = parseFloat(a);
        const bNum = parseFloat(b);

        const aIsNum = !isNaN(aNum);
        const bIsNum = !isNaN(bNum);

        if (aIsNum && bIsNum) return aNum - bNum;
        return String(a).localeCompare(String(b));
      });

      return sorted.join(", ");
    }

    if (
      value &&
      typeof value === "object" &&
      "min" in value &&
      "max" in value
    ) {
      const { min, max } = value as {
        min: number | string;
        max: number | string;
      };

      const isDate =
        typeof min === "number" &&
        typeof max === "number" &&
        min > 1000000000000;

      if (isDate) {
        const formattedMin = new Date(min).toLocaleDateString();
        const formattedMax = new Date(max).toLocaleDateString();
        return `${formattedMin} - ${formattedMax}`;
      }

      return `${min} - ${max}`;
    }

    return "";
  }

  return (
    <div className="space-y-4">
      <div className="space-y-4">
        {/* Header with Mode Toggle */}
        <Card className="p-4 bg-gradient-to-r from-slate-50 to-gray-50 border-0 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <Filter className="h-5 w-5 text-muted-foreground" />
                <span className="text-lg font-semibold">Data Filters</span>
              </div>
              <Badge variant="outline" className="text-xs">
                {hasActiveFilters
                  ? `${activeFilterBadges.length} active`
                  : "No filters"}
              </Badge>
            </div>

            <div className="flex items-center gap-4">
              {/* Mode Toggle */}
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 text-sm">
                  <Zap
                    className={cn(
                      "h-4 w-4",
                      !isAdvancedMode
                        ? "text-blue-500"
                        : "text-muted-foreground",
                    )}
                  />
                  <span
                    className={cn(
                      !isAdvancedMode ? "font-medium" : "text-muted-foreground",
                    )}
                  >
                    Simple
                  </span>
                </div>
                <Switch
                  checked={isAdvancedMode}
                  onCheckedChange={setIsAdvancedMode}
                  className="data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-blue-500 data-[state=checked]:to-purple-500"
                />
                <div className="flex items-center gap-2 text-sm">
                  <Settings2
                    className={cn(
                      "h-4 w-4",
                      isAdvancedMode
                        ? "text-purple-500"
                        : "text-muted-foreground",
                    )}
                  />
                  <span
                    className={cn(
                      isAdvancedMode ? "font-medium" : "text-muted-foreground",
                    )}
                  >
                    Advanced
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2">
                <CreateViewPopover
                  SearchParams={searchParams}
                  views={views}
                  refetchViews={refetchViews}
                  currentViewId={currentViewId}
                  setCurrentViewId={setCurrentViewId}
                />
                <DataTableViewsDropdown
                  views={views}
                  SearchParams={searchParams}
                  setSearchParams={setSearchParams}
                  refetchViews={refetchViews}
                  currentViewId={currentViewId}
                  setCurrentViewId={setCurrentViewId}
                />
                <StudentsTableToolbarActions />
              </div>
            </div>
          </div>
        </Card>
      </div>

      <Card className="p-4 space-y-3 bg-gradient-to-r from-slate-50 to-gray-50 border-0 shadow-sm">
        {/* Simple Filter Controls */}
        <div className="flex items-center gap-3 space-x-2">
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-muted-foreground" />
            <span className="text-sm font-medium text-muted-foreground">
              Filter by:
            </span>
          </div>

          <Select
            value={activeFilterId || ""}
            onValueChange={handleFilterTypeChange}
          >
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
          {activeFilterOption && table.getColumn(activeFilterOption.value) && (
            <DataTableToolbarFilter
              key={activeFilterOption.value}
              column={table.getColumn(activeFilterOption.value)!}
              onFilterChange={handleFilterValueChange}
              isActive={!!appliedFilters[activeFilterOption.value]}
              isAdvancedMode={isAdvancedMode}
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
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
              Active Filters ({activeFilterBadges.length})
            </span>
            <div className="flex-1 h-px bg-border" />
          </div>

          <div className="flex flex-wrap gap-2">
            {activeFilterBadges.map(
              ({ columnId, operator, value, label, variant }) => (
                <Badge
                  key={columnId}
                  variant="secondary"
                  className={cn(
                    "group flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium transition-all duration-200 hover:scale-105",
                    variant === "select" &&
                      "bg-blue-100 text-blue-800 hover:bg-blue-200",
                    variant === "number" &&
                      "bg-green-100 text-green-800 hover:bg-green-200",
                    variant === "date" &&
                      "bg-purple-100 text-purple-800 hover:bg-purple-200",
                    variant === "default" &&
                      "bg-gray-100 text-gray-800 hover:bg-gray-200",
                  )}
                >
                  <div
                    className={cn(
                      "w-1.5 h-1.5 rounded-full",
                      variant === "text" && "bg-gray-500",
                      (variant === "select" || variant === "multiSelect") &&
                        "bg-blue-500",
                      variant === "number" && "bg-green-500",
                      variant === "date" && "bg-purple-500",
                      variant === "range" && "bg-yellow-500",
                      variant === "default" && "bg-gray-500",
                    )}
                  />
                  <span className="font-medium">{label}</span>
                  <span className="max-w-[200px] truncate">
                    {`(${operator}) : ${formatValue(value)}`}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-4 w-4 p-0 ml-1 opacity-60 hover:opacity-100 hover:bg-red-100 hover:text-red-600 group-hover:opacity-100"
                    onClick={() => removeFilterBadges(columnId)}
                  >
                    <X className="h-2.5 w-2.5" />
                  </Button>
                </Badge>
              ),
            )}
          </div>
        </div>

        {/* Empty State */}
        {activeFilterBadges.length === 0 && (
          <div className="text-center">
            <div className="inline-flex items-center gap-2 text-sm text-muted-foreground">
              <Search className="h-4 w-4" />
              <span>
                No filters applied. Select a filter type above to get started.
              </span>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}

interface DataTableToolbarFilterProps<TData> {
  column: Column<TData>;
  onFilterChange?: (value: any) => void;
  isActive?: boolean;
  isAdvancedMode?: boolean;
}

export function DataTableToolbarFilter<TData>({
  column,
  onFilterChange,
  isActive = false,
  isAdvancedMode = false,
}: DataTableToolbarFilterProps<TData>) {
  const { getFilter } = useFilters();

  const columnFilter = getFilter(column?.id);
  const columnMeta = column.columnDef.meta;
  const onFilterRender = React.useCallback(() => {
    const commonProps = {
      column,
      onFilterChange,
      isActive,
      isAdvancedMode,
    };
    if (!columnMeta?.variant) return null;

    switch (columnMeta.variant) {
      case "text":
      case "number":
      case "range":
        return (
          <DataTableInputFilter
            {...commonProps}
            title={columnMeta.label ?? column.id}
            type={columnMeta.variant}
          ></DataTableInputFilter>
        );

      case "date":
      case "dateRange":
        return (
          <DataTableDateFilter
            {...commonProps}
            title={columnMeta.label ?? column.id}
            multiple={
              columnFilter?.operator === "isBetween" ||
              columnFilter?.operator === "isNotBetween"
                ? true
                : false
            }
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
  }, [column, columnMeta, onFilterChange, isActive]);

  return onFilterRender();
}
