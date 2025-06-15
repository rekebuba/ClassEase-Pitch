"use client";

import type { Option } from "@/types/data-table";
import type { Column } from "@tanstack/react-table";
import { Check, PlusCircle, X, XCircle } from "lucide-react";
import { TrashIcon } from "@radix-ui/react-icons";

import { Badge, badgeVariants } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";
import * as React from "react";
import { useFilters } from "@/utils/filter-context";
import { addPointerInfo } from "motion/dist/react";
import { dataTableConfig } from "@/config/data-table";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useState } from "react";
import { DataTableFilterOption } from "@/types";

interface DataTableFacetedFilterProps<TData> {
  column: Column<TData>
  title: string
  setSelectedOptions: React.Dispatch<React.SetStateAction<DataTableFilterOption[]>>
  options: any[]
  multiple?: boolean
  onFilterChange?: (value: any) => void
  isActive?: boolean
}

export function DataTableFacetedFilter<TData>({
  column,
  title,
  setSelectedOptions,
  options,
  multiple,
  onFilterChange,
  isActive,
}: DataTableFacetedFilterProps<TData>) {
  const [open, setOpen] = useState(true);
  const { addFilter, removeFilter, getFilter } = useFilters();

  const columnFilter = getFilter(column?.id);
  const columnFilterValue = columnFilter?.value as string[] | undefined;
  const selectedValues = new Set(
    Array.isArray(columnFilterValue) ? columnFilterValue : [],
  );

  const comparisonOperators = dataTableConfig.multiSelectOperators;

  const operator = React.useMemo(
    () =>
      comparisonOperators.find(
        (op) => op.value === columnFilter?.toString()
      ) ?? comparisonOperators[0],
    [column, comparisonOperators]
  );

  const [selectedOperator, setSelectedOperator] = useState<string>(operator.value);

  const onItemSelect = React.useCallback(
    (option: Option, isSelected: boolean) => {
      if (!column) return;

      if (multiple) {
        const newSelectedValues = new Set(selectedValues);
        if (isSelected) {
          newSelectedValues.delete(option.value);
        } else {
          newSelectedValues.add(option.value);
        }
        const filterValues = Array.from(newSelectedValues);
        onFilterChange?.({ value: filterValues, operator: selectedOperator })
      } else {
        removeFilter(column.id)
      }
    },
    [column, multiple, selectedValues, selectedOperator],
  );

  // const onOperatorSelect = React.useCallback(
  //   (value: string) => {
  //     if (!column) return;

  //     setSelectedOperator(value);
  //     const filterValues = Array.from(selectedValues);
  //     onFilterChange?.({ value: filterValues, operator: selectedOperator })
  //   },
  //   [column, selectedValues],
  // );

  const onReset = React.useCallback(() => {
    onFilterChange?.({ value: [], operator: selectedOperator })

  },
    [column],
  );

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" className={cn(
          "h-9 w-[180px] rounded-md border border-input bg-background text-sm ring-offset-background transition-all duration-200",
          "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
          isActive && selectedValues && "ring-2 ring-blue-500/20 border-blue-300",
        )}>
          <PlusCircle />
          {title}

          {selectedValues?.size > 0 && (
            <>
              <Separator
                orientation="vertical"
                className="mx-0.5 data-[orientation=vertical]:h-4"
              />
              <Badge
                variant="secondary"
                className="rounded-sm px-1 font-normal lg:hidden"
              >
                {selectedValues.size}
              </Badge>
              <div className="hidden items-center gap-1 lg:flex">
                {selectedValues.size > 2 ? (
                  <Badge
                    variant="secondary"
                    className="rounded-sm px-1 font-normal"
                  >
                    {selectedValues.size} selected
                  </Badge>

                ) : (
                  options
                    .filter((option) => selectedValues.has(option.value))
                    .map((option) => (
                      <Badge
                        variant="secondary"
                        key={option.value}
                        className="rounded-sm px-1 font-normal"
                      >
                        {option.value}
                      </Badge>
                    ))
                )}
              </div>
            </>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[12.5rem] p-0" align="start">
        <Command>
          <CommandInput placeholder={title} />
          <CommandList className="max-h-full">
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup className="max-h-[18.75rem] overflow-y-auto overflow-x-hidden">
              {options.map((option) => {
                const isSelected = selectedValues.has(option.value);

                return (
                  <CommandItem
                    key={option.value}
                    onSelect={() => onItemSelect(option, isSelected)}
                  >
                    <div
                      className={cn(
                        "flex size-4 items-center justify-center rounded-sm border border-primary",
                        isSelected
                          ? "bg-primary"
                          : "opacity-50 [&_svg]:invisible",
                      )}
                    >
                      <Check />
                    </div>
                    {option.icon && <option.icon />}
                    <span className="truncate">{option.label}</span>
                    {option.count !== undefined && (
                      <span className="ml-auto font-mono text-xs">
                        {option.count}
                      </span>
                    )}
                  </CommandItem>
                );
              })}
            </CommandGroup>
            {selectedValues.size > 0 && (
              <>
                <CommandSeparator />
                <CommandGroup>
                  <CommandItem
                    onSelect={() => onReset()}
                    className="justify-center text-center"
                  >
                    Clear filters
                  </CommandItem>
                </CommandGroup>
              </>
            )}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover >
  );
}
