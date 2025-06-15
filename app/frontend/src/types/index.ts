import type { SQL } from "drizzle-orm";

export type Prettify<T> = {
  [K in keyof T]: T[K];
} & {};

export type EmptyProps<T extends React.ElementType> = Omit<
  React.ComponentProps<T>,
  keyof React.ComponentProps<T>
>;

// export interface SearchParams {
//   [key: string]: string | string[] | undefined;
// }

export interface QueryBuilderOpts {
  where?: SQL;
  orderBy?: SQL;
  distinct?: boolean;
  nullish?: boolean;
}

export interface Option {
  label: string
  value: string
  icon?: React.ComponentType<{ className?: string }>
  withCount?: boolean
}

export interface DataTableFilterOption {
  id: string
  label: string
  value: string
  variant: string
  options: Option[]
  filterValues?: string[]
  filterOperator?: string
  isMulti?: boolean
}
