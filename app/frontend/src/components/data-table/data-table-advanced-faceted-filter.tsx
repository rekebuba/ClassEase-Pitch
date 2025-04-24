import type { DataTableFilterOption, Option } from "@/types"
import { CheckIcon } from "@radix-ui/react-icons"
import type { Column } from "@tanstack/react-table"

import { cn } from "@/lib/utils"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
    CommandSeparator,
} from "@/components/ui/command"
import { Calendar } from "@/components/ui/calendar";
import * as React from "react";

import {
    BadgeCheck,
    CalendarIcon,
    Check,
    ListFilter,
    Text,
    X,
} from "lucide-react";
import { Checkbox } from "@/components/ui/checkbox"

interface DataTableAdvancedFacetedFilterProps<TData, TValue> {
    column: Column<TData, TValue>
    title?: string
    options: Option[]
    selectedValues: Set<string>
    setSelectedOptions: React.Dispatch<
        React.SetStateAction<DataTableFilterOption<TData>[]>
    >
}

export function DataTableAdvancedFacetedFilter<TData, TValue>({
    column,
    title,
    options,
    selectedValues,
    setSelectedOptions,
}: DataTableAdvancedFacetedFilterProps<TData, TValue>) {
    const [inputValue, setInputValue] = React.useState("");
    const setSelectedValues = (value) => {
        const isSelected = selectedValues.has(value)
        // setInputValue(value)

        if (isSelected) {
            selectedValues.delete(value)
        } else {
            selectedValues.add(value)
        }
        const filterValues = Array.from(selectedValues)
        setSelectedOptions((prev) => prev.map((item) => item.value === column?.id
            ? {
                ...item,
                filterValues,
            }
            : item
        )
        )
    }
    return (
        <Command className="p-1 dark:bg-transparent">
            <div className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm [&_[cmdk-input-wrapper]]:border-0 [&_[cmdk-input-wrapper]]:px-0">
                <CommandInput
                    placeholder={title}
                    className="h-full border-0 pl-0 ring-0"
                    autoFocus
                />
            </div>
            <CommandList>
                <CommandEmpty>No results found.</CommandEmpty>
                <FilterValueSelector
                    column={column}
                    value={inputValue}
                    onSelect={(value) => setSelectedValues(value)}
                />
                {selectedValues.size > 0 && (
                    <>
                        <CommandSeparator />
                        <CommandGroup>
                            <CommandItem
                                onSelect={() => {
                                    column?.setFilterValue(undefined)
                                    setSelectedOptions((prev) =>
                                        prev.map((item) =>
                                            item.value === column?.id
                                                ? {
                                                    ...item,
                                                    filterValues: [],
                                                }
                                                : item
                                        )
                                    )
                                }}
                                className="justify-center text-center"
                            >
                                Clear filters
                            </CommandItem>
                        </CommandGroup>
                    </>
                )}
            </CommandList>
        </Command>
    )
}


interface FilterValueSelectorProps<TData> {
    column: Column<TData>;
    value: string;
    onSelect: (value: string) => void;
}

function FilterValueSelector<TData>({
    column,
    value,
    onSelect,
}: FilterValueSelectorProps<TData>) {
    const variant = column.columnDef.meta?.variant ?? "text";

    switch (variant) {
        case "boolean":
            return (
                <CommandGroup>
                    <CommandItem value="true" onSelect={() => onSelect("true")}>
                        True
                    </CommandItem>
                    <CommandItem value="false" onSelect={() => onSelect("false")}>
                        False
                    </CommandItem>
                </CommandGroup>
            );

        case "select":
        case "multiSelect":
            return (
                <CommandGroup>
                    {column.columnDef.meta?.options?.map((option) => {
                        const selectedValues = Array.isArray(column.getFilterValue())
                            ? (column.getFilterValue() as string[])
                            : [];
                        const isChecked = selectedValues.includes(option.value);

                        return (
                            <CommandItem
                                key={option.value}
                                value={option.value}
                                onSelect={() => onSelect(option.value)}
                            >
                                <label className="flex items-center gap-2 w-full cursor-pointer">
                                    <Checkbox
                                        checked={isChecked}
                                        onCheckedChange={(checked) => {
                                            const newValues = checked
                                                ? [...selectedValues, option.value]
                                                : selectedValues.filter((v) => v !== option.value);
                                            // column.setFilterValue(newValues);
                                        }}
                                    />
                                    {option.icon && <option.icon />}
                                    <span className="truncate">{option.label}</span>
                                    {option.count && (
                                        <span className="ml-auto font-mono text-xs">{option.count}</span>
                                    )}
                                </label>
                            </CommandItem>
                        );
                    })}
                </CommandGroup>
            );

        case "date":
        case "dateRange":
            return (
                <Calendar
                    initialFocus
                    mode="single"
                    selected={value ? new Date(value) : undefined}
                    onSelect={(date) => onSelect(date?.getTime().toString() ?? "")}
                />
            );

        default: {
            const isEmpty = !value.trim();

            return (
                <CommandGroup>
                    <CommandItem
                        value={value}
                        onSelect={() => onSelect(value)}
                        disabled={isEmpty}
                    >
                        {isEmpty ? (
                            <>
                                <Text />
                                <span>Type to add filter...</span>
                            </>
                        ) : (
                            <>
                                <BadgeCheck />
                                <span className="truncate">Filter by &quot;{value}&quot;</span>
                            </>
                        )}
                    </CommandItem>
                </CommandGroup>
            );
        }
    }
}
function useState(arg0: string): [any, any] {
    throw new Error("Function not implemented.")
}
