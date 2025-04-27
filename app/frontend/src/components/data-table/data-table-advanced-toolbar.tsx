"use client";

import * as React from "react";

import { cn } from "@/lib/utils";
import { View } from "@/lib/validations";
import { PlusIcon } from "@radix-ui/react-icons"
import UpdateViewForm from "./views/update-view-form";

import { DataTableFilterOption, SearchParams } from "@/types";
import type { Column } from "@tanstack/react-table";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import {
  DataTableColumnsVisibility,
  useTableInstanceContext,
  DataTableDateFilter,
  DataTableFacetedFilter,
  DataTableInputFilter,
  DataTableSliderFilter,
  DataTableFilterCombobox,
} from "@/components/data-table";
import { CreateViewPopover, DataTableViewsDropdown } from "@/components/data-table/views";


interface DataTableAdvancedToolbarProps<TData>
  extends React.ComponentProps<"div"> {
  views: View[]
  searchParams: SearchParams;
}

export function DataTableAdvancedToolbar<TData>({
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
  // const currentView = views.find((view) => view.id === viewId)

  const [openFilterBuilder, setOpenFilterBuilder] = React.useState(
    initialSelectedOptions.length > 0 || false
  )
  const [openCombobox, setOpenCombobox] = React.useState(false)

  function onFilterComboboxItemSelect() {
    setOpenFilterBuilder(true)
    setOpenCombobox(true)
  }

  function resetToCurrentView() {
    console.log("Resetting to current view")
  }

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
      <div className="flex flex-col items-end justify-between gap-3 sm:flex-row sm:items-center">
        {views && <DataTableViewsDropdown views={views} filterParams={searchParams} />}
        <div className="flex items-center gap-2">
          {children}
          <DataTableColumnsVisibility table={table} />
        </div>
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

        <div className="ml-auto flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={resetToCurrentView}>
            Reset
          </Button>

          <CreateViewPopover selectedOptions={selectedOptions} />

          <UpdateViewForm
            isUpdated={false}
            currentView={undefined}
            filterParams={searchParams}
          />
        </div>
      </div>
    </div>
  );
}


interface DataTableToolbarFilterProps<TData> {
  column: Column<TData>;
  setSelectedOptions: React.Dispatch<
    React.SetStateAction<DataTableFilterOption<TData>[]>
  >
}

export function DataTableToolbarFilter<TData>({
  column,
  setSelectedOptions,
}: DataTableToolbarFilterProps<TData>) {
  {
    const columnMeta = column.columnDef.meta;

    const onFilterRender = React.useCallback(() => {
      if (!columnMeta?.variant) return null;

      switch (columnMeta.variant) {
        case "text":
          return (
            <DataTableInputFilter
              column={column}
              title={columnMeta.label ?? column.id}
              setSelectedOptions={setSelectedOptions}
            >
            </DataTableInputFilter>
          );

        case "number":
          return (
            <div className="relative">
              <Input
                type="number"
                inputMode="numeric"
                placeholder={columnMeta.placeholder ?? columnMeta.label}
                value={(column.getFilterValue() as string) ?? ""}
                onChange={(event) => column.setFilterValue(event.target.value)}
                className={cn("h-8 w-[120px]", columnMeta.unit && "pr-8")}
              />
              {columnMeta.unit && (
                <span className="absolute top-0 right-0 bottom-0 flex items-center rounded-r-md bg-accent px-2 text-muted-foreground text-sm">
                  {columnMeta.unit}
                </span>
              )}
            </div>
          );

        case "range":
          return (
            <DataTableSliderFilter
              column={column}
              title={columnMeta.label ?? column.id}
              setSelectedOptions={setSelectedOptions}
            />
          );

        case "date":
        case "dateRange":
          return (
            <DataTableDateFilter
              column={column}
              title={columnMeta.label ?? column.id}
              multiple={columnMeta.variant === "dateRange"}
            />
          );

        case "select":
        case "multiSelect":
          return (
            <DataTableFacetedFilter
              column={column}
              title={columnMeta.label ?? column.id}
              setSelectedOptions={setSelectedOptions}
              options={columnMeta.options ?? []}
              multiple={columnMeta.variant === "multiSelect"}
            />
          );

        default:
          return null;
      }
    }, [column, columnMeta]);

    return onFilterRender();
  }
}
