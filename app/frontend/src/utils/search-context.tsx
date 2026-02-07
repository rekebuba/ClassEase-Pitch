import {
  parseAsInteger,
  parseAsString,
  parseAsStringEnum,
  useQueryStates,
} from "nuqs";
import React, { createContext, useContext } from "react";

import { useTableInstanceContext } from "@/components/data-table";
import { getFiltersStateParser, getSortingStateParser } from "@/lib/parsers";

type SearchParamsContextType = ReturnType<
  typeof useQueryStates<typeof searchParamMap>
>;

const SearchParamsContext = createContext<SearchParamsContextType | null>(null);

export function SearchParamsProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { tableInstance: table } = useTableInstanceContext();

  const columnIds = React.useMemo(() => {
    return table
      .getAllColumns()
      .filter(column => column.columnDef.enableColumnFilter)
      .map(column => column.id);
  }, [table]);

  const searchParamMap = {
    page: parseAsInteger.withDefault(1),
    perPage: parseAsInteger.withDefault(10),
    sort: getSortingStateParser().withDefault([]),
    filters: getFiltersStateParser(columnIds)
      .withDefault([])
      .withOptions({ clearOnDefault: true, shallow: true, throttleMs: 50 }),
    joinOperator: parseAsStringEnum(["and", "or"]).withDefault("and"),
    viewId: parseAsString,
  };
  const queryState = useQueryStates(searchParamMap);
  return (
    <SearchParamsContext.Provider value={queryState}>
      {children}
    </SearchParamsContext.Provider>
  );
}

export function useSearchParamsContext() {
  const context = useContext(SearchParamsContext);
  if (!context) {
    throw new Error(
      "useSearchParamsContext must be used within a SearchParamsProvider",
    );
  }
  return context;
}
