import type { DataTableFilterOption } from "@/types"
import type { FilterParams } from "@/lib/validations"

export function calcFilterParams<T>(
  selectedOptions: DataTableFilterOption<T>[],
  searchParams: URLSearchParams,
): FilterParams {
  const filterParams: FilterParams = {}

  // Process selected filter options
  selectedOptions.forEach((option) => {
    if (option.value) {
      filterParams[option.id] = option.value
    }
  })

  // Add any other search params that might be relevant
  searchParams.forEach((value, key) => {
    if (!["page", "per_page", "sort", "viewId"].includes(key)) {
      try {
        // Try to parse as JSON if it looks like an object/array
        if (value.startsWith("{") || value.startsWith("[")) {
          filterParams[key] = JSON.parse(value)
        } else {
          filterParams[key] = value
        }
      } catch {
        filterParams[key] = value
      }
    }
  })

  return filterParams
}

export function calcViewSearchParamsURL(filterParams: FilterParams): string {
  const params = new URLSearchParams()

  Object.entries(filterParams).forEach(([key, value]) => {
    if (typeof value === "object") {
      params.set(key, JSON.stringify(value))
    } else {
      params.set(key, String(value))
    }
  })

  return params.toString()
}
