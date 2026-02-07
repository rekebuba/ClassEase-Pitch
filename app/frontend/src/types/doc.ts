import type { DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import type { EmptyProps } from "@/types";
import type { ExtendedColumnFilter, Option } from "@/types/data-table";
import type { Column, Table, TableOptions } from "@tanstack/react-table";
import type { motion } from "motion/react";
import type * as React from "react";

export type UseDataTableProps<TData> = {
  /**
   * Determines how query updates affect history.
   * `push` creates a new history entry; `replace` (default) updates the current entry.
   * @default "replace"
   */
  history?: "push" | "replace";

  /**
   * Debounce time (ms) for filter updates to enhance performance during rapid input.
   * @default 300
   */
  debounceMs?: number;

  /**
   * Maximum time (ms) to wait between URL query string updates.
   * Helps with browser rate-limiting. Minimum effective value is 50ms.
   * @default 50
   */
  throttleMs?: number;

  /**
   * Clear URL query key-value pair when state is set to default.
   * Keep URL meaning consistent when defaults change.
   * @default false
   */
  clearOnDefault?: boolean;

  /**
   * Enable notion like column filters.
   * Advanced filters and column filters cannot be used at the same time.
   * @default false
   * @type boolean
   */
  enableAdvancedFilter?: boolean;

  /**
   * Whether the page should scroll to the top when the URL changes.
   * @default false
   */
  scroll?: boolean;

  /**
   * Whether to keep query states client-side, avoiding server calls.
   * Setting to `false` triggers a network request with the updated querystring.
   * @default true
   */
  shallow?: boolean;

  /**
   * Observe Server Component loading states for non-shallow updates.
   * Pass `startTransition` from `React.useTransition()`.
   * Sets `shallow` to `false` automatically.
   * So shallow: true` and `startTransition` cannot be used at the same time.
   * @see https://react.dev/reference/react/useTransition
   */
  startTransition?: React.TransitionStartFunction;
} & Required<Pick<TableOptions<TData>, "pageCount">> & Pick<
  TableOptions<TData>,
      "data" | "columns" | "getRowId" | "defaultColumn" | "initialState"
>;

export type DataTableProps<TData> = {
  /** The table instance. */
  table: Table<TData>;

  /** The action bar to display above the table. */
  actionBar?: React.ReactNode;
} & EmptyProps<"div">;

export type DataTableToolbarProps<TData> = {
  /** The table instance. */
  table: Table<TData>;
} & EmptyProps<"div">;

export type DataTableAdvancedToolbarProps<TData> = {
  /** The table instance. */
  table: Table<TData>;
} & EmptyProps<"div">;

export type DataTableActionBarProps<TData> = {
  /** The table instance. */
  table: Table<TData>;

  /** Whether the action bar is visible. */
  visible?: boolean;

  /**
   * The container to mount the portal into.
   * @default document.body
   */
  container?: Element | DocumentFragment | null;
} & EmptyProps<typeof motion.div>;

export type DataTableColumnHeaderProps<TData, TValue> = {
  /** The column instance. */
  column: Column<TData, TValue>;

  /** The column title. */
  title: string;
} & EmptyProps<typeof DropdownMenuTrigger>;

export type DataTableDateFilterProps<TData> = {
  /** The column instance. */
  column: Column<TData, unknown>;

  /** The title of the date picker. */
  title?: string;

  /** Whether to enable range selection. */
  multiple?: boolean;
};

export type DataTableFacetedFilterProps<TData, TValue> = {
  /** The column instance. */
  column?: Column<TData, TValue>;

  /** The title of the filter. */
  title?: string;

  /** The options of the filter. */
  options: Option[];

  /** Whether to enable multiple selection. */
  multiple?: boolean;
};

export type DataTableSliderFilterProps<TData> = {
  /** The column instance. */
  column: Column<TData, unknown>;

  /** The title of the slider filter. */
  title?: string;
};

export type DataTableRangeFilterProps<TData> = {
  /** The extended column filter. */
  filter: ExtendedColumnFilter<TData>;

  /** The column instance. */
  column: Column<TData>;

  /** The input id for screen readers. */
  inputId: string;

  /** The function to update the filter. */
  onFilterUpdate: (
    filterId: string,
    updates: Partial<Omit<ExtendedColumnFilter<TData>, "filterId">>,
  ) => void;
} & EmptyProps<"div">;

export type DataTableFilterListProps<TData> = {
  /** The table instance. */
  table: Table<TData>;

  /**
   * Debounce time (ms) for filter updates to enhance performance during rapid input.
   * @default 300
   */
  debounceMs?: number;

  /**
   * Maximum time (ms) to wait between URL query string updates.
   * Helps with browser rate-limiting. Minimum effective value is 50ms.
   * @default 50
   */
  throttleMs?: number;

  /**
   * Whether to keep query states client-side, avoiding server calls.
   * Setting to `false` triggers a network request with the updated querystring.
   * @default true
   */
  shallow?: boolean;
};

export type DataTableFilterMenuProps<TData> = {} & DataTableFilterListProps<TData>;

export type DataTableSortListProps<TData> = {} & DataTableFilterListProps<TData>;

export type DataTablePaginationProps<TData> = {
  /** The table instance. */
  table: Table<TData>;

  /**
   * The options of the pagination.
   * @default [10, 20, 30, 40, 50]
   */
  pageSizeOptions?: number[];
} & EmptyProps<"div">;

export type DataTableColumnsVisibilityProps<TData> = {
  /** The table instance. */
  table: Table<TData>;
};

export type DataTableSkeletonProps = {
  /** The number of columns in the table. */
  columnCount: number;

  /**
   * The number of rows in the table.
   * @default 10
   */
  rowCount?: number;

  /**
   * The number of filters in the table.
   * @default 0
   */
  filterCount?: number;

  /**
   * Array of CSS width values for each table column.
   * The maximum length of the array must match columnCount, extra values will be ignored.
   * @default ["auto"]
   */
  cellWidths?: string[];

  /**
   * Whether to show the view options.
   * @default true
   */
  withViewOptions?: boolean;

  /**
   * Whether to show the pagination bar.
   * @default true
   */
  withPagination?: boolean;

  /**
   * Whether to prevent the table cells from shrinking.
   * @default false
   */
  shrinkZero?: boolean;
} & EmptyProps<"div">;
