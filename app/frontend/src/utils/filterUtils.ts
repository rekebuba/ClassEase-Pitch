import { ExtendedColumnFilter } from "@/types/data-table";

type UpdateFilterOptions<TData> = {
  filters: ExtendedColumnFilter<TData>[];
  setFilters: (
    updater: (
      prev: ExtendedColumnFilter<TData>[],
    ) => ExtendedColumnFilter<TData>[],
  ) => void;
};

export function createFilterUtils<TData>({
  filters,
  setFilters,
}: UpdateFilterOptions<TData>) {
  return {
    /** Add or update a filter */
    setFilter: (newFilter: ExtendedColumnFilter<TData>) => {
      setFilters((prev) => {
        const others = prev.filter((f) => f.id !== newFilter.id);
        return [...others, newFilter];
      });
    },

    /** Remove a filter by id */
    removeFilter: (filterId: string) => {
      setFilters((prev) => prev.filter((f) => f.id !== filterId));
    },

    /** Clear all filters */
    clearFilters: () => {
      setFilters(() => []);
    },

    /** Get filter by id */
    getFilter: (filterId: string) => {
      return filters.find((f) => f.id === filterId);
    },
  };
}
