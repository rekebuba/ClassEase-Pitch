"use client"

import { useState } from "react"
import type { DataTableFilterOption } from "@/types"

import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

import { CreateViewForm } from "./create-view-form"
import { calcFilterParams } from "./utils"
import { SearchParams } from "@/lib/types"

interface CreateViewPopoverProps<T> {
  SearchParams: SearchParams
  onCreateView?: (newView: any) => void
}

export function CreateViewPopover<T>({ SearchParams, onCreateView }: CreateViewPopoverProps<T>) {
  const [open, setOpen] = useState(false)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button size="sm">Save as new view</Button>
      </PopoverTrigger>
      <PopoverContent
        className="w-[12.5rem] p-0 dark:bg-background/95 dark:backdrop-blur-md dark:supports-[backdrop-filter]:bg-background/40"
        align="end"
      >
        <CreateViewForm SearchParams={SearchParams} onSuccess={() => setOpen(false)} onCreateView={onCreateView} />
      </PopoverContent>
    </Popover>
  )
}
