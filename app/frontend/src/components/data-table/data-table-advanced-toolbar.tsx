"use client";

import type { Table } from "@tanstack/react-table";
import * as React from "react";

import { DataTableToolbarFilter, DataTableViewOptions, useTableInstanceContext } from "@/components/data-table";
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

interface DataTableAdvancedToolbarProps<TData>
  extends React.ComponentProps<"div"> {
  views: View[]
  searchParams: SearchParams;
  setSearchParams: ({}) => void;
}

export function DataTableAdvancedToolbar<TData>({
  children,
  views,
  className,
  searchParams,
  setSearchParams,
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

  const initialSelectedOptions = React.useMemo(() => {
    return options
      .filter((option) => searchParams[option.value] !== undefined && searchParams[option.id] !== "")
      .map((option) => {
        return {
          ...option,
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
      <div className="flex flex-1 items-center gap-2">{children}</div>
      <div className="flex flex-col items-end justify-between gap-3 sm:flex-row sm:items-center">
        {views && <DataTableViewsDropdown views={views} filterParams={searchParams} />}
      </div>
      <div className="flex items-center justify-between">
        {openFilterBuilder && (
          <div className="flex h-8 items-center gap-2">
            {selectedOptions
              .filter((option) => !option.isMulti)
              .map((selectedOption) => {
                const column = table.getColumn(selectedOption.value);
                return (
                  <DataTableToolbarFilter
                    key={String(selectedOption.value)}
                    setSelectedOptions={setSelectedOptions}
                    column={column}
                  />
                );
              })}
          </div>
        )}
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
