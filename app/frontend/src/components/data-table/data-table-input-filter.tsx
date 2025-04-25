"use client"

import type { Column } from "@tanstack/react-table"
import { PlusCircle, XCircle } from "lucide-react"
import { TrashIcon } from "@radix-ui/react-icons"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Command, CommandGroup, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"
import * as React from "react"
import { useFilters } from "@/utils/filter-context"
import { dataTableConfig } from "@/config/data-table"
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useState } from "react"
import type { DataTableFilterOption } from "@/types"
import { Input } from "@/components/ui/input"

interface DataTableInputFilterProps<TData, TValue> {
    column?: Column<TData, TValue>
    title: string
    setSelectedOptions: React.Dispatch<React.SetStateAction<DataTableFilterOption<TData>[]>>
}

export function DataTableInputFilter<TData, TValue>({
    column,
    title,
    setSelectedOptions,
}: DataTableInputFilterProps<TData, TValue>) {
    const [open, setOpen] = useState(true)
    const { addFilter, removeFilter, getFilter, debouncedAddFilter } = useFilters()

    const columnFilter = getFilter(column?.id)
    const textFilterValue = columnFilter?.value as string | undefined

    const comparisonOperators = dataTableConfig.multiSelectOperators

    const operator = comparisonOperators.find((operator) => operator.value === columnFilter?.id) ?? comparisonOperators[0]

    const [selectedOperator, setSelectedOperator] = useState<string>(operator.value)
    const [selectedText, setSelectedText] = useState<string>(textFilterValue ?? "")

    const onTextChange = React.useCallback(
        (value: string) => {
            if (!column) return
            setSelectedText(value)
            if (value === "") {
                removeFilter(column.id)
            } else {
                debouncedAddFilter({
                    id: column.id,
                    value: value,
                    operator: selectedOperator,
                })
            }
        },
        [column, removeFilter, debouncedAddFilter, selectedOperator],
    )

    const onOperatorSelect = React.useCallback(
        (value: string) => {
            if (!column) return
            setSelectedOperator(value)

            if (selectedText) {
                addFilter({
                    id: column.id,
                    value: selectedText,
                    operator: value,
                })
            }
        },
        [column, addFilter, selectedText],
    )

    const onReset = React.useCallback(
        (event: React.MouseEvent | undefined, remove: boolean) => {
            event?.stopPropagation()
            removeFilter(column?.id)
            if (remove) {
                setSelectedOptions((prev) => prev.filter((item) => item.value !== column?.id))
            }
        },
        [column],
    )

    return (
        <Popover open={open} onOpenChange={setOpen}>
            <PopoverTrigger asChild>
                <Button variant="outline" size="sm" className="border-dashed">
                    {textFilterValue && textFilterValue?.length > 0 ? (
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
                    {textFilterValue && textFilterValue?.length > 0 && (
                        <>
                            <Separator orientation="vertical" className="mx-0.5 data-[orientation=vertical]:h-4" />
                            <div className="hidden items-center gap-1 lg:flex">
                                <Badge variant="secondary" className="rounded-sm px-1 font-normal">
                                    <span
                                    className=" max-w-14 truncate overflow-clip"
                                    >{textFilterValue}</span>
                                </Badge>
                            </div>
                        </>
                    )}
                </Button>
            </PopoverTrigger>
            <PopoverContent className="w-[13.5rem] p-0" align="start">
                <Command>
                    <FilterHeader
                        title={title}
                        comparisonOperators={comparisonOperators}
                        selectedOperator={selectedOperator}
                        onOperatorSelect={onOperatorSelect}
                        onReset={onReset}
                    />
                    <CommandList className="max-h-full">
                        <CommandGroup className="max-h-[18.75rem] overflow-y-auto overflow-x-hidden">
                            <Input
                                placeholder={title}
                                value={selectedText}
                                onChange={(e) => onTextChange(e.target.value)}
                                className="h-8 w-14 lg:w-full"
                            />
                        </CommandGroup>
                    </CommandList>
                </Command>
            </PopoverContent>
        </Popover>
    )
}

interface FilterHeaderProps {
    title: string
    selectedOperator: string
    onOperatorSelect: (value: string) => void
    onReset: (event: React.MouseEvent | undefined, remove: boolean) => void
    comparisonOperators: {
        value: string
        label: string
    }[]
}
function FilterHeader({ title, selectedOperator, onOperatorSelect, onReset, comparisonOperators }: FilterHeaderProps) {
    return (
        <div className="flex items-center space-x-1 pl-1 pr-0.5 mt-1">
            <div className="flex flex-1 items-center space-x-1">
                <div className="text-xs capitalize text-muted-foreground max-w-14 truncate overflow-clip">{title}</div>
                <Select value={selectedOperator} onValueChange={(value) => onOperatorSelect(value)}>
                    <SelectTrigger className="h-auto w-fit truncate border-none px-2 py-0.5 text-xs hover:bg-muted/50">
                        <SelectValue
                            placeholder={comparisonOperators.find((op) => op.value === selectedOperator)?.label || "Select operator"}
                        />
                    </SelectTrigger>
                    <SelectContent className="dark:bg-background/95 dark:backdrop-blur-md dark:supports-[backdrop-filter]:bg-background/40">
                        <SelectGroup>
                            {comparisonOperators.map(({ value, label }) => (
                                <SelectItem key={value} value={value} className="py-1">
                                    {label}
                                </SelectItem>
                            ))}
                        </SelectGroup>
                    </SelectContent>
                </Select>
            </div>
            <Button
                aria-label="Remove filter"
                variant="ghost"
                size="icon"
                className="size-7 text-muted-foreground"
                onClick={() => onReset(undefined, true)}
            >
                <TrashIcon className="size-4" aria-hidden="true" />
            </Button>
        </div>
    )
}
