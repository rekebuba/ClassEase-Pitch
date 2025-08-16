import React, { createContext, useContext } from "react";
import { useQueryState } from "nuqs";
import { getFiltersStateParser } from "@/lib/parsers";
import { useDebouncedCallback } from "@/hooks/use-debounced-callback";

const FilterContext = createContext<ReturnType<
  typeof useFiltersContext
> | null>(null);

export const FilterProvider = ({
  children,
  columnIds,
}: {
  children: React.ReactNode;
  columnIds: string[];
}) => {
  const value = useFiltersContext(columnIds);
  return (
    <FilterContext.Provider value={value}>{children}</FilterContext.Provider>
  );
};

export const useFilters = () => {
  const context = useContext(FilterContext);
  if (!context)
    throw new Error("useFilters must be used within a FilterProvider");
  return context;
};

// internal logic
function useFiltersContext<TData>(columnIds: string[]) {
  const [filters, setFilters] = useQueryState(
    "filters",
    getFiltersStateParser<TData>(columnIds)
      .withDefault([])
      .withOptions({ clearOnDefault: true, shallow: true, throttleMs: 50 }),
  );

  const debouncedAddFilter = useDebouncedCallback((newFilter: any) => {
    setFilters((prev) => {
      const others = prev.filter((f) => f.id !== newFilter.id);
      return [...others, newFilter];
    });
  }, 50);

  const addFilter = (newFilter: any) => {
    setFilters((prev) => {
      const others = prev.filter((f) => f.id !== newFilter.id);
      return [...others, newFilter];
    });
  };

  const removeFilter = (id: string | undefined) => {
    if (!id) return;
    setFilters((prev) => (prev ?? []).filter((f) => f.id !== id));
  };

  const clearFilters = () => setFilters([]);

  /** Get filter by id */
  const getFilter = (id: string | undefined) => {
    if (!id) return undefined;
    return filters.find((f) => f.id === id);
  };

  return {
    filters,
    setFilters,
    addFilter,
    removeFilter,
    clearFilters,
    getFilter,
    debouncedAddFilter,
  };
}
