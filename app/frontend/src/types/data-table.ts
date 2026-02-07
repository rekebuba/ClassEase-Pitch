import type { DataTableConfig } from "@/config/data-table";
import type { FilterItemSchema } from "@/lib/parsers";
import type { RangeSchema, TableIdValue } from "@/lib/types";
import type { ColumnSort, Row, RowData } from "@tanstack/react-table";

declare module "@tanstack/react-table" {
  // biome-ignore lint/correctness/noUnusedVariables: <explanation>
  type ColumnMeta<TData extends RowData, TValue> = {
    tableId?: TableIdValue;
    label?: string;
    placeholder?: string;
    variant?: FilterVariant;
    options?: Option[];
    range?: RangeSchema;
    unit?: string;
    icon?: React.FC<React.SVGProps<SVGSVGElement>>;
  };

  type ColumnSort = {
    tableId: TableIdValue;
  };
}

export type Option = {
  label: string;
  value: string;
  operator?: string;
  count?: number;
  icon?: React.FC<React.SVGProps<SVGSVGElement>>;
};

export type FilterOperator = DataTableConfig["operators"][number];
export type FilterVariant = DataTableConfig["filterVariants"][number];
export type JoinOperator = DataTableConfig["joinOperators"][number];

export type ExtendedColumnSort<TData> = {
  id: Extract<keyof TData, string>;
  // tableId: string;
} & Omit<ColumnSort, "id">;

export type ExtendedColumnFilter<TData> = {
  id: Extract<keyof TData, string>;
} & FilterItemSchema;

export type DataTableRowAction<TData> = {
  row: Row<TData>;
  variant: "update" | "delete" | "view";
};
