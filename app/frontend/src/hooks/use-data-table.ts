"use client";

import {
  type ColumnFiltersState,
  type PaginationState,
  type RowSelectionState,
  type SortingState,
  type TableOptions,
  type TableState,
  type Updater,
  type VisibilityState,
  getCoreRowModel,
  getFacetedMinMaxValues,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useSearchParams, useNavigate } from "react-router-dom";
import * as React from "react";

import { useDebouncedCallback } from "@/hooks/use-debounced-callback";
import type { ExtendedColumnSort } from "@/types/data-table";

const PAGE_KEY = "page";
const PER_PAGE_KEY = "perPage";
const SORT_KEY = "sort";
const ARRAY_SEPARATOR = ",";
const DEBOUNCE_MS = 300;
const THROTTLE_MS = 50;

interface UseDataTableProps<TData>
  extends Omit<
    TableOptions<TData>,
    | "state"
    | "pageCount"
    | "getCoreRowModel"
    | "manualFiltering"
    | "manualPagination"
    | "manualSorting"
  >,
  Required<Pick<TableOptions<TData>, "pageCount">> {
  initialState?: Omit<Partial<TableState>, "sorting"> & {
    sorting?: ExtendedColumnSort<TData>[];
  };
  history?: "push" | "replace";
  debounceMs?: number;
  throttleMs?: number;
  clearOnDefault?: boolean;
  enableAdvancedFilter?: boolean;
  scroll?: boolean;
  shallow?: boolean;
}

export function useDataTable<TData>(props: UseDataTableProps<TData>) {
  const {
    columns,
    pageCount = -1,
    initialState,
    history = "replace",
    debounceMs = DEBOUNCE_MS,
    throttleMs = THROTTLE_MS,
    clearOnDefault = false,
    enableAdvancedFilter = false,
    scroll = false,
    shallow = true,
    ...tableProps
  } = props;

  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const [rowSelection, setRowSelection] = React.useState<RowSelectionState>(
    initialState?.rowSelection ?? {},
  );
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>(initialState?.columnVisibility ?? {});

  // Get pagination state from URL
  const page = parseInt(searchParams.get(PAGE_KEY) || "1");
  const perPage = parseInt(searchParams.get(PER_PAGE_KEY) || (initialState?.pagination?.pageSize || 10).toString());

  const pagination: PaginationState = React.useMemo(() => ({
    pageIndex: page - 1,
    pageSize: perPage,
  }), [page, perPage]);

  const updateURL = React.useCallback((updater: (prev: URLSearchParams) => URLSearchParams) => {
    const newParams = updater(new URLSearchParams(searchParams));
    if (history === "replace") {
      setSearchParams(newParams, { replace: true });
    } else {
      navigate(`?${newParams.toString()}`, { replace: false });
    }
  }, [searchParams, history, setSearchParams, navigate]);

  const onPaginationChange = React.useCallback(
    (updaterOrValue: Updater<PaginationState>) => {
      updateURL((prev) => {
        const newParams = new URLSearchParams(prev);
        const newPagination = typeof updaterOrValue === "function"
          ? updaterOrValue(pagination)
          : updaterOrValue;

        newParams.set(PAGE_KEY, (newPagination.pageIndex + 1).toString());
        newParams.set(PER_PAGE_KEY, newPagination.pageSize.toString());
        return newParams;
      });
    },
    [pagination, updateURL]
  );

  const columnIds = React.useMemo(() => {
    return new Set(
      columns.map((column) => column.id).filter(Boolean) as string[],
    );
  }, [columns]);

  // Get sorting state from URL
  const sorting = React.useMemo(() => {
    const sortParam = searchParams.get(SORT_KEY);
    if (!sortParam) return initialState?.sorting ?? [];

    try {
      return JSON.parse(sortParam) as ExtendedColumnSort<TData>[];
    } catch {
      return initialState?.sorting ?? [];
    }
  }, [searchParams, initialState?.sorting]);

  const onSortingChange = React.useCallback(
    (updaterOrValue: Updater<SortingState>) => {
      updateURL((prev) => {
        const newParams = new URLSearchParams(prev);
        const newSorting = typeof updaterOrValue === "function"
          ? updaterOrValue(sorting)
          : updaterOrValue;

        newParams.set(SORT_KEY, JSON.stringify(newSorting));
        return newParams;
      });
    },
    [sorting, updateURL]
  );

  const filterableColumns = React.useMemo(() =>
    enableAdvancedFilter ? [] : columns.filter((column) => column.enableColumnFilter),
    [columns, enableAdvancedFilter]
  );

  // Get filter values from URL
  const filterValues = React.useMemo(() => {
    const values: Record<string, string | string[]> = {};
    filterableColumns.forEach((column) => {
      const value = searchParams.get(column.id ?? "");
      if (value !== null) {
        values[column.id ?? ""] = column.meta?.options
          ? value.split(ARRAY_SEPARATOR)
          : value;
      }
    });
    return values;
  }, [searchParams, filterableColumns]);

  const debouncedSetFilterValues = useDebouncedCallback(
    (values: Record<string, string | string[] | null>) => {
      updateURL((prev) => {
        const newParams = new URLSearchParams(prev);
        newParams.set(PAGE_KEY, "1"); // Reset to first page

        Object.entries(values).forEach(([key, value]) => {
          if (value === null || value === "") {
            newParams.delete(key);
          } else {
            newParams.set(
              key,
              Array.isArray(value) ? value.join(ARRAY_SEPARATOR) : value
            );
          }
        });

        return newParams;
      });
    },
    debounceMs
  );

  const initialColumnFilters: ColumnFiltersState = React.useMemo(() => {
    if (enableAdvancedFilter) return [];

    return Object.entries(filterValues).reduce<ColumnFiltersState>(
      (filters, [key, value]) => {
        if (value !== null) {
          const processedValue = Array.isArray(value)
            ? value
            : typeof value === "string" && /[^a-zA-Z0-9]/.test(value)
              ? value.split(/[^a-zA-Z0-9]+/).filter(Boolean)
              : [value];

          filters.push({
            id: key,
            value: processedValue,
          });
        }
        return filters;
      },
      []
    );
  }, [filterValues, enableAdvancedFilter]);

  const [columnFilters, setColumnFilters] =
    React.useState<ColumnFiltersState>(initialColumnFilters);

  const onColumnFiltersChange = React.useCallback(
    (updaterOrValue: Updater<ColumnFiltersState>) => {
      if (enableAdvancedFilter) return;

      setColumnFilters((prev) => {
        const next =
          typeof updaterOrValue === "function"
            ? updaterOrValue(prev)
            : updaterOrValue;

        const filterUpdates = next.reduce<
          Record<string, string | string[] | null>
        >((acc, filter) => {
          if (filterableColumns.find((column) => column.id === filter.id)) {
            acc[filter.id] = filter.value as string | string[];
          }
          return acc;
        }, {});

        for (const prevFilter of prev) {
          if (!next.some((filter) => filter.id === prevFilter.id)) {
            filterUpdates[prevFilter.id] = null;
          }
        }

        debouncedSetFilterValues(filterUpdates);
        return next;
      });
    },
    [debouncedSetFilterValues, filterableColumns, enableAdvancedFilter]
  );

  const table = useReactTable({
    ...tableProps,
    columns,
    initialState,
    pageCount,
    state: {
      pagination,
      sorting,
      columnVisibility,
      rowSelection,
      columnFilters,
    },
    defaultColumn: {
      ...tableProps.defaultColumn,
      enableColumnFilter: false,
    },
    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
    onPaginationChange,
    onSortingChange,
    onColumnFiltersChange,
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
    getFacetedMinMaxValues: getFacetedMinMaxValues(),
    manualPagination: true,
    manualSorting: true,
    manualFiltering: true,
  });

  return { table, shallow, debounceMs, throttleMs };
}
