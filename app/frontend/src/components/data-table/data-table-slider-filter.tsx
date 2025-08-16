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
import { PlusCircle } from "lucide-react";
import { useFilters } from "@/utils/filter-context";
import { RangeSchema } from "@/lib/types";

interface Range {
  min: number;
  max: number;
}

type RangeValue = {
  min: number;
  max: number;
};

function getIsValidRange(value: RangeSchema | undefined): value is Range {
  if (!value) return false;
  return (
    Object(value) &&
    "min" in value &&
    "max" in value &&
    typeof value.min === "number" &&
    typeof value.max === "number" &&
    value.min <= value.max
  );
}

interface DataTableSliderFilterProps<TData> {
  column: Column<TData>;
  title: string;
  onFilterChange?: (value: any) => void;
  isActive?: boolean;
  selectedOperator: string;
}

export function DataTableSliderFilter<TData>({
  column,
  title,
  onFilterChange,
  isActive,
  selectedOperator,
}: DataTableSliderFilterProps<TData>) {
  const id = React.useId();

  const { getFilter } = useFilters();

  const columnFilter = getFilter(column?.id);
  const columnFilterValue = getIsValidRange(columnFilter?.value)
    ? (columnFilter?.value as RangeValue)
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

  const onFromInputChange = React.useCallback(
    (value: String, operator: String) => {
      const numValue = Number(value);

      if (value !== "" && !Number.isNaN(numValue)) {
        onFilterChange?.({
          value: { min: numValue, max: range.max },
          operator,
        });
      }
    },
    [column, min, range, selectedOperator],
  );

  const onToInputChange = React.useCallback(
    (value: String, operator: String) => {
      const numValue = Number(value);

      if (value !== "" && !Number.isNaN(numValue)) {
        onFilterChange?.({
          value: { min: range.min, max: numValue },
          operator,
        });
      }
    },
    [column, max, range, selectedOperator],
  );

  const onSliderValueChange = React.useCallback(
    (value: RangeValue, operator: String) => {
      onFilterChange?.({ value, operator });
    },
    [column, selectedOperator],
  );

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          size="sm"
          className={cn(
            "h-9 min-w-[180px] rounded-md border border-input bg-background text-sm ring-offset-background transition-all duration-200",
            "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
            isActive && range && "ring-2 ring-blue-500/20 border-blue-300",
          )}
        >
          <PlusCircle />
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
                value={range.min}
                onChange={(e) =>
                  onFromInputChange(e.target.value, selectedOperator)
                }
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
                value={range.max}
                onChange={(e) =>
                  onToInputChange(e.target.value, selectedOperator)
                }
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
                onSliderValueChange(
                  { min: value[0], max: value[1] },
                  selectedOperator,
                );
              }
            }}
          />
        </div>
        <Button
          aria-label={`Clear ${title} filter`}
          variant="outline"
          size="sm"
          onClick={() =>
            onFilterChange?.({ value: {}, operator: selectedOperator })
          }
        >
          Clear
        </Button>
      </PopoverContent>
    </Popover>
  );
}
