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

import { CreateViewForm } from "./create-view-form"
import { EditViewForm } from "./edit-view-form"
import { parseAsString, useQueryState } from "nuqs"
import { SearchParams, StudentsViews, View } from "@/lib/types"
import { CreateViewPopover } from "./create-view-popover"
import UpdateViewForm from "./update-view-form"
import { createNewView, deleteView, renameView, updateView } from "@/api/adminApi"
import { toast } from "sonner"
import { searchParamsCache } from "@/lib/validations"
import isEqual from 'lodash/isEqual';

interface DataTableViewsDropdownProps {
  views: StudentsViews[]
  SearchParams: SearchParams
  setSearchParams: (params: SearchParams) => void
  refetchViews: () => void
}

export function DataTableViewsDropdown({
  views,
  SearchParams,
  setSearchParams,
  refetchViews,
}: DataTableViewsDropdownProps) {
  const [open, setOpen] = useState(false)
  const [isCreateViewFormOpen, setIsCreateViewFormOpen] = useState(false)
  const [isEditViewFormOpen, setIsEditViewFormOpen] = useState(false)
  const [selectedView, setSelectedView] = useState<StudentsViews | null>(null)
  const [currentViewId, setCurrentViewId] = useQueryState("viewId", parseAsString)
  const [allowUpdate, setAllowUpdate] = useState(false)
  const [allowCreate, setAllowCreate] = useState(false)

  const currentView = views.find((view) => view.viewId === currentViewId)

  useEffect(() => {
    console.log("Current View:", currentView?.searchParams)
    if (currentView && !isEqual(currentView.searchParams, SearchParams)) {
      // setSelectedView(currentView)
      console.log("not View:", isEqual(currentView?.searchParams, SearchParams))
      setAllowUpdate(true)
    }
    else {
      setAllowUpdate(false)
    }
    if (!currentViewId && SearchParams) {
      // If no view is selected, check if SearchParams are different from default
      const defaultSearchParams: SearchParams = {
        page: 1,
        perPage: 10,
        sort: [],
        filters: [],
        joinOperator: "and",
      };
      setAllowCreate(!isEqual(SearchParams, defaultSearchParams));
    }
    else {
      setAllowCreate(false)
    }
  }, [currentView, views, SearchParams])


  function selectView(view: StudentsViews | null) {
    if (view) {
      // Update state
      setCurrentViewId(view.viewId)
      setSearchParams(view.searchParams)
    } else {
      // Clear view selection
      setSearchParams({
        page: 1,
        perPage: 10,
        sort: [],
        filters: [],
        joinOperator: "and",
      });
      setCurrentViewId(null)
    }
  }

  const isMac = getIsMacOS()
  useHotkeys(`${isMac ? "meta" : "ctrl"}+v`, () => {
    setTimeout(() => setOpen(true), 100)
  })

  const handleCreateView = async (newView: View) => {
    const result = await createNewView(newView)
    toast.error(result.message, {
      style: { color: "green" },
    });
    refetchViews()
    setCurrentViewId(result?.viewId)
  }

  const handleUpdateView = async (updatedView: StudentsViews) => {
    const result = await updateView(updatedView)
    toast.error(result.message, {
      style: { color: "green" },
    });
    refetchViews()
    setCurrentViewId(result?.viewId)
  }

  const handleDeleteView = async (viewId: string) => {
    const result = await deleteView(viewId)

    toast.error(result.message, {
      style: { color: "green" },
    });
    refetchViews()

    if (currentViewId === viewId) {
      selectView(null)
    }
  }

  return (
    <>
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
              SearchParams={SearchParams}
              onSuccess={() => setOpen(false)}
              onCreateView={handleCreateView}
            />
          )}
          {isEditViewFormOpen && selectedView && (
            <EditViewForm
              view={selectedView}
              setIsEditViewFormOpen={setIsEditViewFormOpen}
              refetchViews={refetchViews}
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
                      refetchViews()
                      selectView(null)
                      setOpen(false)
                    }}
                  >
                    All Items
                  </CommandItem>
                  {views.map((view) => (
                    <CommandItem
                      key={view.viewId}
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
      {allowCreate ? <CreateViewPopover SearchParams={SearchParams} onCreateView={handleCreateView} /> : null}
      <UpdateViewForm
        isUpdated={allowUpdate}
        currentView={currentView as StudentsViews}
        searchParams={SearchParams}
        handleUpdateView={handleUpdateView}
      />
    </>
  )
}
