"use client"

import { useState } from "react"
import type { DataTableFilterOption } from "@/types"

import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

import { CreateViewForm } from "./create-view-form"
import { calcFilterParams } from "./utils"

interface CreateViewPopoverProps<T> {
  selectedOptions: DataTableFilterOption<T>[]
  onCreateView?: (newView: any) => void
}

export function CreateViewPopover<T>({ selectedOptions, onCreateView }: CreateViewPopoverProps<T>) {
  const [open, setOpen] = useState(false)

  // Use window.location.search to get current search params
  const searchParams = new URLSearchParams(window.location.search)

  const filterParams = calcFilterParams(selectedOptions, searchParams)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button size="sm">Save as new view</Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-[12.5rem] p-0 dark:bg-background/95 dark:backdrop-blur-md dark:supports-[backdrop-filter]:bg-background/40"
        align="end"
      >
        <CreateViewForm filterParams={filterParams} onSuccess={() => setOpen(false)} onCreateView={onCreateView} />
      </PopoverContent>
    </Popover>
  )
}
