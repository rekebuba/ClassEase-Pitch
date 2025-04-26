"use client"

import type React from "react"

import { useEffect, useRef, useState } from "react"
import { ChevronLeftIcon } from "@radix-ui/react-icons"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { LoaderIcon } from "lucide-react"
import type { FilterParams } from "@/lib/validations"

import { useTableInstanceContext } from "@/components/data-table"

interface CreateViewFormProps {
  backButton?: true
  onBack?: () => void
  onSuccess?: () => void
  filterParams?: FilterParams
  onCreateView?: (newView: any) => void
}

export function CreateViewForm({ backButton, filterParams, onBack, onSuccess, onCreateView }: CreateViewFormProps) {
  const [pending, setPending] = useState(false)
  const [viewName, setViewName] = useState("")
  const nameInputRef = useRef<HTMLInputElement>(null)

  const { tableInstance } = useTableInstanceContext()

  const visibleColumns =
    tableInstance
      ?.getVisibleFlatColumns()
      .filter((column) => typeof column.accessorFn !== "undefined" && column.getCanHide())
      .map((column) => column.id) || []

  useEffect(() => {
    nameInputRef.current?.focus()
  }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!viewName.trim()) {
      toast.error("View name is required")
      return
    }

    setPending(true)

    // Create a new view object
    const newView = {
      id: `view-${Date.now()}`,
      name: viewName,
      columns: visibleColumns,
      searchParams: filterParams || {},
      createdAt: new Date().toISOString(),
    }

    // Simulate API call
    setTimeout(() => {
      if (onCreateView) {
        onCreateView(newView)
      }
      toast.success("View created successfully")
      setPending(false)
      onSuccess?.()
    }, 500)
  }

  return (
    <div>
      {backButton && (
        <>
          <div className="flex items-center gap-1 px-1 py-1.5">
            <Button variant="ghost" size="icon" className="size-6" onClick={() => onBack?.()}>
              <span className="sr-only">Close create view form</span>
              <ChevronLeftIcon aria-hidden="true" className="size-4" />
            </Button>

            <span className="text-sm">Create view</span>
          </div>

          <Separator />
        </>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-2 p-2">
        <Input
          ref={nameInputRef}
          type="text"
          name="name"
          placeholder="Name"
          autoComplete="off"
          value={viewName}
          onChange={(e) => setViewName(e.target.value)}
        />
        <Button disabled={pending} size="sm" type="submit">
          {pending ? <LoaderIcon aria-hidden="true" className="size-3.5 animate-spin" /> : "Create"}
        </Button>
      </form>
    </div>
  )
}
