"use client"

import { useState, useEffect } from "react"
import { CaretDownIcon, Pencil1Icon, PlusIcon } from "@radix-ui/react-icons"
import { useHotkeys } from "react-hotkeys-hook"

import { getIsMacOS } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Kbd } from "@/components/kbd"
import type { FilterParams, View } from "@/lib/validations"

import { CreateViewForm } from "./create-view-form"
import { EditViewForm } from "./edit-view-form"

interface DataTableViewsDropdownProps {
  views: View[]
  filterParams: FilterParams
}

export function DataTableViewsDropdown({
  views,
  filterParams,
}: DataTableViewsDropdownProps) {
  const [open, setOpen] = useState(false)
  const [isCreateViewFormOpen, setIsCreateViewFormOpen] = useState(false)
  const [isEditViewFormOpen, setIsEditViewFormOpen] = useState(false)
  const [selectedView, setSelectedView] = useState<View | null>(null)
  const [currentViewId, setCurrentViewId] = useState<string | null>(null)

  // Get current view from URL
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const viewId = params.get("viewId")
    setCurrentViewId(viewId)
  }, [window.location.search])

  const currentView = views.find((view) => view.id === currentViewId)

  function selectView(view: View | null) {
    if (view) {
      // Update URL with view's search params
      const params = new URLSearchParams()

      // Add viewId
      params.set("viewId", view.id)

      // Add all other search params from the view
      for (const [key, value] of Object.entries(view.searchParams)) {
        if (typeof value === "object") {
          params.set(key, JSON.stringify(value))
        } else {
          params.set(key, String(value))
        }
      }

      // Update URL without navigation
      window.history.replaceState({}, "", `${window.location.pathname}?${params.toString()}`)

      // Update state
      setCurrentViewId(view.id)
      console.log("Selected view:", view)
    } else {
      // Clear view selection
      const params = new URLSearchParams(window.location.search)
      params.delete("viewId")
      window.history.replaceState({}, "", `${window.location.pathname}?${params.toString()}`)

      setCurrentViewId(null)
    }
  }

  const isMac = getIsMacOS()
  useHotkeys(`${isMac ? "meta" : "ctrl"}+v`, () => {
    setTimeout(() => setOpen(true), 100)
  })

  const handleCreateView = (newView: View) => {
    console.log("New view created:", newView)
  }

  const handleUpdateView = (updatedView: View) => {
    console.log("View updated:", updatedView)
  }

  const handleDeleteView = (viewId: string) => {
    console.log("View deleted:", viewId)
    if (currentViewId === viewId) {
      selectView(null)
    }
  }

  return (
    <Popover
      open={open}
      onOpenChange={(value) => {
        setOpen(value)
        setIsCreateViewFormOpen(false)
        setIsEditViewFormOpen(false)
      }}
    >
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <PopoverTrigger asChild>
              <Button variant="outline" size="sm" className="flex w-36 shrink-0 justify-between">
                <span className="truncate">{currentView?.name || "All Items"}</span>
                <CaretDownIcon aria-hidden="true" className="size-4 shrink-0" />
              </Button>
            </PopoverTrigger>
          </TooltipTrigger>
          <TooltipContent className="flex items-center gap-2 border bg-accent font-semibold text-foreground dark:bg-background/95 dark:backdrop-blur-md dark:supports-[backdrop-filter]:bg-background/40">
            Open views
            <div>
              <Kbd variant="outline" className="font-sans">
                {isMac ? "⌘" : "ctrl"}
              </Kbd>{" "}
              <Kbd variant="outline" className="font-sans">
                V
              </Kbd>
            </div>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>

      <PopoverContent
        className="w-[12.5rem] p-0 dark:bg-background/95 dark:backdrop-blur-md dark:supports-[backdrop-filter]:bg-background/40"
        align="start"
      >
        {isCreateViewFormOpen && (
          <CreateViewForm
            backButton
            onBack={() => setIsCreateViewFormOpen(false)}
            filterParams={filterParams}
            onSuccess={() => setOpen(false)}
            onCreateView={handleCreateView}
          />
        )}

        {isEditViewFormOpen && selectedView && (
          <EditViewForm
            view={selectedView}
            setIsEditViewFormOpen={setIsEditViewFormOpen}
            onSave={handleUpdateView}
            onDelete={handleDeleteView}
          />
        )}

        {!isCreateViewFormOpen && !isEditViewFormOpen && (
          <Command className="dark:bg-transparent">
            <CommandInput placeholder="View name" />
            <CommandList>
              <CommandEmpty>No item found.</CommandEmpty>
              <CommandGroup className="max-h-48 overflow-auto">
                <CommandItem
                  value="All Items"
                  onSelect={() => {
                    selectView(null)
                    setOpen(false)
                  }}
                >
                  All Items
                </CommandItem>
                {views.map((view) => (
                  <CommandItem
                    key={view.id}
                    value={view.name}
                    className="group justify-between"
                    onSelect={() => {
                      selectView(view)
                      setOpen(false)
                    }}
                  >
                    <span className="truncate">{view.name}</span>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="invisible size-5 shrink-0 hover:bg-neutral-200 group-hover:visible dark:hover:bg-neutral-700"
                      onClick={(e) => {
                        e.stopPropagation()
                        setIsEditViewFormOpen(true)
                        setSelectedView(view)
                      }}
                    >
                      <Pencil1Icon className="size-3" />
                    </Button>
                  </CommandItem>
                ))}
              </CommandGroup>
              <Separator />
              <CommandGroup>
                <CommandItem onSelect={() => setIsCreateViewFormOpen(true)}>
                  <PlusIcon className="mr-2 size-4" aria-hidden="true" />
                  Add view
                </CommandItem>
              </CommandGroup>
            </CommandList>
          </Command>
        )}
      </PopoverContent>
    </Popover>
  )
}
