"use client"

import type React from "react"

import { useState } from "react"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { LoaderIcon } from "lucide-react"
import type { FilterParams } from "@/lib/validations"
import { useTableInstanceContext } from "@/components/data-table"
import type { View } from "@/lib/validations"

interface UpdateViewFormProps {
  isUpdated: boolean
  currentView: View | undefined
  filterParams: FilterParams
  onUpdate: (updatedView: View) => void
}

export default function UpdateViewForm({ isUpdated, currentView, filterParams, onUpdate }: UpdateViewFormProps) {
  const [isLoading, setIsLoading] = useState(false)
  const { tableInstance } = useTableInstanceContext()

  const visibleColumns =
    tableInstance
      ?.getVisibleFlatColumns()
      .filter((column) => typeof column.accessorFn !== "undefined" && column.getCanHide())
      .map((column) => column.id) || []

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!currentView) return

    setIsLoading(true)

    // Create updated view with current filters
    const updatedView: View = {
      ...currentView,
      columns: visibleColumns,
      searchParams: filterParams || {},
    }

    // Simulate API call
    setTimeout(() => {
      try {
        onUpdate(updatedView)
        toast.success("View updated successfully")
      } catch (error) {
        toast.error("Failed to update view")
      } finally {
        setIsLoading(false)
      }
    }, 500)
  }

  if (!isUpdated || !currentView) return null

  return (
    <form onSubmit={handleSubmit}>
      <Button disabled={isLoading} type="submit" size="sm" className="gap-1.5">
        {isLoading && <LoaderIcon aria-hidden="true" className="size-3.5 animate-spin" />}
        Update view
      </Button>
    </form>
  )
}
