"use client";

import type { Option } from "@/types/data-table";
import type { Column } from "@tanstack/react-table";
import { Check, PlusCircle, XCircle } from "lucide-react";
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

interface DataTableFacetedFilterProps<TData, TValue> {
  column?: Column<TData, TValue>;
  title: string;
  options: Option[];
  multiple?: boolean;
  setSelectedOptions: React.Dispatch<
    React.SetStateAction<DataTableFilterOption<TData>[]>
  >;
}

export function DataTableFacetedFilter<TData, TValue>({
  column,
  title,
  options,
  multiple,
  setSelectedOptions,
}: DataTableFacetedFilterProps<TData, TValue>) {
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
        addFilter({
          id: column.id,
          variant: column.columnDef.meta?.variant,
          tableId: column.columnDef.meta?.tableId,
          value: filterValues,
          operator: selectedOperator,
        }
        )
      } else {
        removeFilter(column.id)
      }
    },
    [column, multiple, selectedValues, selectedOperator],
  );

  const onOperatorSelect = React.useCallback(
    (value: string) => {
      if (!column) return;

      setSelectedOperator(value);
      const filterValues = Array.from(selectedValues);
      addFilter({
        id: column.id,
        variant: column.columnDef.meta?.variant,
        tableId: column.columnDef.meta?.tableId,
        value: filterValues,
        operator: value,
      });
    },
    [column, selectedValues],
  );

  const onReset = React.useCallback(
    (event: React.MouseEvent | undefined, remove: boolean) => {
      event?.stopPropagation();
      removeFilter(column?.id);
      selectedValues.clear();
      if (remove) {
        setSelectedOptions((prev) =>
          prev.filter((item) => item.value !== column?.id)
        );
      };
    },
    [column],
  );

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" className="border-dashed">
          {selectedValues?.size > 0 ? (
            <div
              role="button"
              aria-label={`Clear ${title} filter`}
              tabIndex={0}
              onClick={() => onReset(undefined, true)}
              className="rounded-sm opacity-70 transition-opacity hover:opacity-100 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            >
              <XCircle />
            </div>
          ) : (
            <PlusCircle />
          )}
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
          <FilterHeader
            title={title}
            comparisonOperators={comparisonOperators}
            selectedOperator={selectedOperator}
            onOperatorSelect={onOperatorSelect}
            onReset={onReset}
          />
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
                    {option.count && (
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
                    onSelect={() => onReset(undefined, false)}
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

interface FilterHeaderProps {
  title: string;
  selectedOperator: string;
  onOperatorSelect: (value: string) => void;
  onReset: (event: React.MouseEvent | undefined, remove: boolean) => void;
  comparisonOperators: {
    value: string;
    label: string;
  }[];
}
function FilterHeader({ title, selectedOperator, onOperatorSelect, onReset, comparisonOperators }: FilterHeaderProps) {
  return (
    <div className="flex items-center space-x-1 pl-1 pr-0.5 mt-1">
      <div className="flex flex-1 items-center space-x-1">
        <div className="text-xs capitalize text-muted-foreground">
          {title}
        </div>
        <Select value={selectedOperator} onValueChange={value => onOperatorSelect(value)}>
          <SelectTrigger className="h-auto w-fit truncate border-none px-2 py-0.5 text-xs hover:bg-muted/50">
            <SelectValue placeholder={comparisonOperators.find(op => op.value === selectedOperator)?.label || "Select operator"} />
          </SelectTrigger>
          <SelectContent className="dark:bg-background/95 dark:backdrop-blur-md dark:supports-[backdrop-filter]:bg-background/40">
            <SelectGroup>
              {comparisonOperators.map(({
                value,
                label
              }) => <SelectItem key={value} value={value} className="py-1">
                  {label}
                </SelectItem>)}
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
      <Button aria-label="Remove filter" variant="ghost" size="icon" className="size-7 text-muted-foreground" onClick={() => onReset(undefined, true)}>
        <TrashIcon className="size-4" aria-hidden="true" />
      </Button>
    </div>
  );
}
