"use client";

import type { Table } from "@tanstack/react-table";
import * as React from "react";

import { DataTableFilterItem, DataTableViewOptions, useTableInstanceContext } from "@/components/data-table";
import { cn } from "@/lib/utils";
import { DataTableFilterCombobox } from "./data-table-filter-combobox";
import { DataTableFilterOption, SearchParams } from "@/types";
import { useQueryState, useQueryStates } from "nuqs";
import { useLocation } from "react-router-dom";
import { searchParamMap, View } from "@/lib/validations";
import { Button } from "@/components/ui/button";
import { CaretSortIcon, PlusIcon } from "@radix-ui/react-icons"
import { calcFilterParams } from "./views/utils";
import { DataTableViewsDropdown } from "@/components/data-table/views";
import { getFiltersStateParser } from "@/lib/parsers";

// import { useLocation } from "react-router-dom";


interface DataTableAdvancedToolbarProps<TData>
  extends React.ComponentProps<"div"> {
  // table: Table<TData>;
  searchParams: SearchParams;
  views: Omit<View, "createdAt" | "updatedAt">[]
}

export function DataTableAdvancedToolbar<TData>({
  // table,
  children,
  views,
  className,
  searchParams,
  ...props
}: DataTableAdvancedToolbarProps<TData>) {

  const { tableInstance: table } = useTableInstanceContext()

  const columns = React.useMemo(
    () => table.getAllColumns().filter((column) => column.getCanFilter()),
    [table],
  );

  const options = React.useMemo<DataTableFilterOption<TData>[]>(() => {
    return columns.map((column) => {
      const columnMeta = column.columnDef.meta
      return {
        id: crypto.randomUUID(),
        label: columnMeta?.label ?? "",
        variant: columnMeta?.variant ?? "default",
        value: column.id,
        options: columnMeta?.options ?? [],
      }
    })
  }, [columns])

  // console.log("options", options)

  const initialSelectedOptions = React.useMemo(() => {
    return options
      .filter((option) => searchParams[option.value] !== undefined && searchParams[option.id] !== "")
      .map((option) => {
        const value = searchParams['filterValues']
        const isMulti = searchParams["isMulti"] === "true"
        const operator = searchParams["filterOperator"] ?? "equals"
        return {
          ...option,
          filterValues: value ? value : [],
          filterOperator: operator,
          isMulti: isMulti,
        }
      })
  }, [options, searchParams])

  const [selectedOptions, setSelectedOptions] = React.useState<
    DataTableFilterOption<TData>[]
  >(initialSelectedOptions)

  const selectableOptions = options.filter(
    (option) =>
      !selectedOptions.some(
        (selectedOption) => selectedOption.value === option.value
      )
  )

  const [openFilterBuilder, setOpenFilterBuilder] = React.useState(
    initialSelectedOptions.length > 0 || false
  )
  const [openCombobox, setOpenCombobox] = React.useState(false)

  function onFilterComboboxItemSelect() {
    setOpenFilterBuilder(true)
    setOpenCombobox(true)
  }

  const multiFilterOptions = React.useMemo(
    () => selectedOptions.filter((option) => option.isMulti),
    [selectedOptions]
  )

  const [filters, setFilters] = useQueryState(
    "filters",
    getFiltersStateParser<TData>(columns.map((field) => field.id))
      .withDefault([])
      .withOptions({
        clearOnDefault: true,
      }),
  );

  // const filterParams = calcFilterParams(selectedOptions, searchParams)

  // console.log("selectedOptions", selectedOptions)
  // console.log("searchParams", searchParams)


  return (
    <div
      role="toolbar"
      aria-orientation="horizontal"
      className={cn(
        "flex w-full items-start justify-between gap-2 p-1",
        className,
      )}
      {...props}
    >
      <div className="flex flex-1 flex-wrap items-center gap-2">{children}</div>
      <div className="flex flex-col items-end justify-between gap-3 sm:flex-row sm:items-center">
        {/* <DataTableViewsDropdown views={views} filterParams={filterParams} /> */}

        <div className="flex items-center gap-2">
          {(options.length > 0 && selectedOptions.length > 0) ||
            openFilterBuilder ? (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setOpenFilterBuilder(!openFilterBuilder)}
            >
              <CaretSortIcon
                className="mr-2 size-4 shrink-0"
                aria-hidden="true"
              />
              Filter
            </Button>
          ) : (
            <DataTableFilterCombobox
              selectableOptions={selectableOptions}
              selectedOptions={selectedOptions}
              setSelectedOptions={setSelectedOptions}
              onSelect={onFilterComboboxItemSelect}
            />
          )}
        </div>
      </div>
      <div className="flex items-center justify-between">
        {openFilterBuilder && (
          <div className="flex h-8 items-center gap-2">
            {selectedOptions
              .filter((option) => !option.isMulti)
              .map((selectedOption) => (
                <DataTableFilterItem
                  key={String(selectedOption.value)}
                  selectedOption={selectedOption}
                  setSelectedOptions={setSelectedOptions}
                  searchParams={searchParams}
                  defaultOpen={openCombobox}
                  filters={filters}
                  setFilters={setFilters}
                />
              ))}
            {/* {selectedOptions.some((option) => option.isMulti) ? (
              <DataTableMultiFilter
                allOptions={options}
                options={multiFilterOptions}
                selectedOptions={selectedOptions}
                setSelectedOptions={setSelectedOptions}
                defaultOpen={openCombobox}
              />
            ) : null} */}
            {selectableOptions.length > 0 ? (
              <DataTableFilterCombobox
                selectableOptions={selectableOptions}
                selectedOptions={selectedOptions}
                setSelectedOptions={setSelectedOptions}
                onSelect={onFilterComboboxItemSelect}
              >
                <Button
                  variant="outline"
                  size="sm"
                  role="combobox"
                  className="h-7 rounded-full"
                  onClick={() => setOpenCombobox(true)}
                >
                  <PlusIcon
                    className="mr-2 size-4 opacity-50"
                    aria-hidden="true"
                  />
                  Add filter
                </Button>
              </DataTableFilterCombobox>
            ) : null}
          </div>
        )}

        {/* <div className="ml-auto flex items-center gap-2">
          {isUpdated && currentView && (
            <Button variant="ghost" size="sm" onClick={resetToCurrentView}>
              Reset
            </Button>
          )}

          {isDefaultViewUpdated && !currentView && (
            <CreateViewPopover selectedOptions={selectedOptions} />
          )}

          <UpdateViewForm
            isUpdated={isUpdated}
            currentView={currentView}
            filterParams={filterParams}
          />
        </div> */}
      </div>
    </div>
  );
}
