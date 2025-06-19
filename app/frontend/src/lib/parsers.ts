import { createParser } from "nuqs/server";
import { z } from "zod";

import { dataTableConfig } from "@/config/data-table";

import type {
  ExtendedColumnFilter,
  ExtendedColumnSort,
} from "@/types/data-table";
import { filterItemSchema } from "./validations";

const tableIdValue = z.union([
  z.string(),
  z.array(z.tuple([z.string(), z.string()])),
]);


const sortingItemSchema = z.object({
  id: z.string(),
  desc: z.boolean(),
  tableId: tableIdValue,
});

export const getSortingStateParser = <TData>(
  columnIds?: string[] | Set<string>,
) => {
  const validKeys = columnIds
    ? columnIds instanceof Set
      ? columnIds
      : new Set(columnIds)
    : null;

  return createParser({
    parse: (value) => {
      try {
        // const decoded = decodeURIComponent(value);
        const parsed = JSON.parse(value);
        const result = z.array(sortingItemSchema).safeParse(parsed);

        if (!result.success) return null;

        if (validKeys && result.data.some((item) => !validKeys.has(item.id))) {
          return null;
        }

        return result.data as ExtendedColumnSort<TData>[];
      } catch {
        return null;
      }
    },
    // serialize: (value) => encodeURIComponent(JSON.stringify(value)),
    serialize: (value) => JSON.stringify(value),
    eq: (a, b) =>
      a.length === b.length &&
      a.every(
        (item, index) =>
          item.id === b[index]?.id &&
          item.desc === b[index]?.desc &&
          item.tableId === b[index]?.tableId,
      ),
  });
};


export type FilterItemSchema = z.infer<typeof filterItemSchema>;

export const getFiltersStateParser = <TData>(
  columnIds?: string[] | Set<string>,
) => {
  const validKeys = columnIds
    ? columnIds instanceof Set
      ? columnIds
      : new Set(columnIds)
    : null;

  return createParser({
    parse: (value) => {
      try {
        const decoded = decodeURIComponent(value);
        const parsed = JSON.parse(value);
        const result = z.array(filterItemSchema).safeParse(parsed);

        if (!result.success) return null;

        if (validKeys && result.data.some((item) => !validKeys.has(item.id))) {
          return null;
        }

        return result.data as ExtendedColumnFilter<TData>[];
      } catch {
        return null;
      }
    },
    // serialize: (value) => encodeURIComponent(JSON.stringify(value)),
    serialize: (value) => JSON.stringify(value),
    eq: (a, b) =>
      a.length === b.length &&
      a.every(
        (filter, index) =>
          filter.id === b[index]?.id &&
          filter.tableId === b[index]?.tableId &&
          filter.value === b[index]?.value &&
          filter.range === b[index]?.range &&
          filter.variant === b[index]?.variant &&
          filter.operator === b[index]?.operator &&
          filter.filterId === b[index]?.filterId,
      ),
  });
};
