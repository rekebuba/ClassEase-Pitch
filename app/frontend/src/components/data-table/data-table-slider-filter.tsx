"use client";

import type { Column } from "@tanstack/react-table";
import * as React from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";
import { Slider } from "@/components/ui/slider";
import { cn } from "@/lib/utils";
import { FormInput, PlusCircle, XCircle } from "lucide-react";
import { TrashIcon } from "@radix-ui/react-icons"
import { useFilters } from "@/utils/filter-context";
import { DataTableFilterOption } from "@/types";

interface Range {
  min: number;
  max: number;
}

type RangeValue = {
  min: number;
  max: number;
};

function getIsValidRange(value: Range | undefined): value is Range {
  if (!value) return false;
  return (
    Object(value) &&
    'min' in value && 'max' in value &&
    typeof value.min === "number" &&
    typeof value.max === "number"
  );
}

interface DataTableSliderFilterProps<TData> {
  column: Column<TData, unknown>;
  title?: string;
  setSelectedOptions: React.Dispatch<
    React.SetStateAction<DataTableFilterOption<TData>[]>
  >
}

export function DataTableSliderFilter<TData>({
  column,
  title,
  setSelectedOptions,
}: DataTableSliderFilterProps<TData>) {
  const id = React.useId();

  const { addFilter, removeFilter, getFilter } = useFilters();
  const [open, setOpen] = React.useState(true);

  const columnFilter = getFilter(column?.id);
  const columnFilterValue = getIsValidRange(columnFilter?.range)
    ? (columnFilter?.range as RangeValue)
    : undefined;

  const defaultRange = column.columnDef.meta?.range;
  const unit = column.columnDef.meta?.unit;

  const { min, max, step } = React.useMemo<Range & { step: number }>(() => {
    let minValue = 0;
    let maxValue = 100;

    if (defaultRange && getIsValidRange(defaultRange)) {
      minValue = defaultRange.min;
      maxValue = defaultRange.max;
    } else {
      const values = column.getFacetedMinMaxValues();
      if (values && Array.isArray(values) && values.length === 2) {
        const [facetMinValue, facetMaxValue] = values;
        if (
          typeof facetMinValue === "number" &&
          typeof facetMaxValue === "number"
        ) {
          minValue = facetMinValue;
          maxValue = facetMaxValue;
        }
      }
    }

    const rangeSize = maxValue - minValue;
    const step =
      rangeSize <= 20
        ? 1
        : rangeSize <= 100
          ? Math.ceil(rangeSize / 20)
          : Math.ceil(rangeSize / 50);

    return { min: minValue, max: maxValue, step };
  }, [column, defaultRange]);

  const range = React.useMemo((): RangeValue => {
    return columnFilterValue ?? { min: min, max: max };
  }, [columnFilterValue, min, max]);

  const formatValue = React.useCallback((value: number) => {
    return value.toLocaleString(undefined, { maximumFractionDigits: 0 });
  }, []);

  const [fromInput, setFromInput] = React.useState({ min: range.min.toString(), max: range.max.toString() });

  React.useEffect(() => {
    setFromInput({ min: range.min.toString(), max: range.max.toString() });
  }, [range.min, range.max]);

  const onFromInputChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const value = event.target.value;
      setFromInput((prev) => ({ ...prev, min: value }));

      const numValue = Number(value);

      if (
        value !== "" &&
        !Number.isNaN(numValue) &&
        numValue >= min &&
        numValue <= range.max
      ) {
        addFilter({
          id: column.id,
          variant: column.columnDef.meta?.variant,
          tableId: column.columnDef.meta?.tableId,
          range: { min: numValue, max: range.max },
        })
      }
    },
    [column, min, range],
  );

  const onToInputChange = React.useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const value = event.target.value;
      setFromInput((prev) => ({ ...prev, max: value }));

      const numValue = Number(value);
      if (
        value !== "" &&
        !Number.isNaN(numValue) &&
        numValue <= max &&
        numValue >= range.min
      ) {
        addFilter({
          id: column.id,
          variant: column.columnDef.meta?.variant,
          tableId: column.columnDef.meta?.tableId,
          range: { min: range.min, max: numValue },
        })
      }
    },
    [column, max, range],
  );

  const onSliderValueChange = React.useCallback(
    (value: RangeValue) => {
      addFilter({
        id: column.id,
        variant: column.columnDef.meta?.variant,
        tableId: column.columnDef.meta?.tableId,
        range: value,
      });
    },
    [column]
  );

  const onReset = React.useCallback(
    (event: React.MouseEvent | undefined, remove: boolean) => {
      if (event?.target instanceof HTMLDivElement) {
        event?.stopPropagation();
      }
      removeFilter(column.id);
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
          {columnFilterValue ? (
            <div
              role="button"
              aria-label={`Clear ${title} filter`}
              tabIndex={0}
              className="rounded-sm opacity-70 transition-opacity hover:opacity-100 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
              onClick={() => onReset(undefined, true)}
            >
              <XCircle />
            </div>
          ) : (
            <PlusCircle />
          )}
          <span>{title}</span>
          {columnFilterValue ? (
            <>
              <Separator
                orientation="vertical"
                className="mx-0.5 data-[orientation=vertical]:h-4"
              />
              {formatValue(columnFilterValue.min)} -{" "}
              {formatValue(columnFilterValue.max)}
              {unit ? ` ${unit}` : ""}
            </>
          ) : null}
        </Button>
      </PopoverTrigger>
      <PopoverContent align="start" className="flex w-auto flex-col gap-4">
        <div className="flex flex-col gap-3">
          <div className="flex items-center space-x-1 pl-1 pr-0.5">
            <div className="flex flex-1 items-center space-x-1">
              <div className="text-xs capitalize text-muted-foreground">
                {title}
              </div>
            </div>
            <Button aria-label="Remove filter" variant="ghost" size="icon" className="size-7 text-muted-foreground" onClick={() => onReset(undefined, true)}>
              <TrashIcon className="size-4" aria-hidden="true" />
            </Button>
          </div>
          <div className="flex items-center gap-4">
            <Label htmlFor={`${id}-from`} className="sr-only">
              From
            </Label>
            <div className="relative">
              <Input
                id={`${id}-from`}
                type="number"
                aria-valuemin={min}
                aria-valuemax={max}
                inputMode="numeric"
                pattern="[0-9]*"
                placeholder={min.toString()}
                min={min}
                max={max}
                value={fromInput.min}
                onChange={onFromInputChange}
                className={cn("h-8 w-24", unit && "pr-8")}
              />
              {unit && (
                <span className="absolute top-0 right-0 bottom-0 flex items-center rounded-r-md bg-accent px-2 text-muted-foreground text-sm">
                  {unit}
                </span>
              )}
            </div>
            <Label htmlFor={`${id}-to`} className="sr-only">
              to
            </Label>
            <div className="relative">
              <Input
                id={`${id}-to`}
                type="number"
                aria-valuemin={min}
                aria-valuemax={max}
                inputMode="numeric"
                pattern="[0-9]*"
                placeholder={max.toString()}
                min={min}
                max={max}
                value={fromInput.max}
                onChange={onToInputChange}
                className={cn("h-8 w-24", unit && "pr-8")}
              />
              {unit && (
                <span className="absolute top-0 right-0 bottom-0 flex items-center rounded-r-md bg-accent px-2 text-muted-foreground text-sm">
                  {unit}
                </span>
              )}
            </div>
          </div>
          <Label htmlFor={`${id}-slider`} className="sr-only">
            {title} slider
          </Label>
          <Slider
            id={`${id}-slider`}
            min={min}
            max={max}
            step={step}
            value={[range.min, range.max]}
            onValueChange={(value) => {
              if (Array.isArray(value) && value.length === 2) {
                onSliderValueChange({ min: value[0], max: value[1] });
              }
            }}
          />
        </div>
        <Button
          aria-label={`Clear ${title} filter`}
          variant="outline"
          size="sm"
          onClick={() => onReset(undefined, false)}
        >
          Clear
        </Button>
      </PopoverContent>
    </Popover>
  );
}
