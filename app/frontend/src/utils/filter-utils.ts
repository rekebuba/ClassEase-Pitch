import { useDebouncedCallback } from "@/hooks/use-debounced-callback";
import { ColumnFiltersState, Updater } from "@tanstack/react-table";


type FiltersState<TData> = (updater: Updater<ColumnFiltersState>) => void;

export function filterUtils<TData>(onFilterChange: FiltersState<TData>) {
    const debouncedAddFilter = useDebouncedCallback(
        (newFilter: any) => {
            debugger;
            console.log("handleValueChange", newFilter)
            onFilterChange((prev) => {
                const others = prev.filter((f) => f.id !== newFilter.id);
                return [...others, newFilter];
            });
        },
        50
    );
    
    const addFilter = (newFilter: any) => {
        onFilterChange((prev) => {
            const others = prev.filter((f) => f.id !== newFilter.id);
            return [...others, newFilter];
        });
    };

    const removeFilter = (id: string | undefined) => {
        if (!id) return;
        onFilterChange((prev) => (prev ?? []).filter((f) => f.id !== id));
    };

    const clearFilters = () => onFilterChange([]);

    /** Get filter by id */
    const getFilter = (filters: ColumnFiltersState, id: string | undefined) => {
        if (!id) return undefined;
        return filters.find((f) => f.id === id);
    };

    return { addFilter, removeFilter, clearFilters, getFilter, debouncedAddFilter };
}
