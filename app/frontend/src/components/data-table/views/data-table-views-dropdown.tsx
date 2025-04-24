import { useState } from "react"
import { usePathname, useRouter, useSearchParams } from "next/navigation"
import type { View } from "@/db/schema"
import { CaretDownIcon, Pencil1Icon, PlusIcon } from "@radix-ui/react-icons"
import { useHotkeys } from "react-hotkeys-hook"

import { getIsMacOS } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { Kbd } from "@/components/kbd"
import type { FilterParams } from "@/lib/validations"

import { CreateViewForm } from "./create-view-form"
import { EditViewForm } from "./edit-view-form"
import { calcViewSearchParamsURL } from "./utils"

export type ViewItem = Omit<View, "createdAt" | "updatedAt">

interface DataTableViewsDropdownProps {
  views: ViewItem[]
  filterParams: FilterParams
}

export function DataTableViewsDropdown({
  views,
  filterParams,
}: DataTableViewsDropdownProps) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const [open, setOpen] = useState(false)
  const [isCreateViewFormOpen, setIsCreateViewFormOpen] = useState(false)
  const [isEditViewFormOpen, setIsEditViewFormOpen] = useState(false)
  const [selectedView, setSelectedView] = useState<ViewItem | null>(null)

  const currentView = views.find(
    (view) => view.id === searchParams.get("viewId")
  )

  function selectView(view: ViewItem) {
    const searchParamsURL = calcViewSearchParamsURL(view)
    router.push(`${pathname}?${searchParamsURL}`, {
      scroll: false,
    })
  }

  const isMac = getIsMacOS()
  useHotkeys(`${isMac ? "meta" : "ctrl"}+v`, () => {
    setTimeout(() => setOpen(true), 100)
  })

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
              <Button
                variant="outline"
                size="sm"
                className="flex w-36 shrink-0 justify-between"
              >
                <span className="truncate">
                  {currentView?.name || "All tasks"}
                </span>
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
          />
        )}

        {isEditViewFormOpen && selectedView && (
          <EditViewForm
            view={selectedView}
            setIsEditViewFormOpen={setIsEditViewFormOpen}
          />
        )}

        {!isCreateViewFormOpen && !isEditViewFormOpen && (
          <Command className="dark:bg-transparent">
            <CommandInput placeholder="View name" />
            <CommandList>
              <CommandEmpty>No item found.</CommandEmpty>
              <CommandGroup className="max-h-48 overflow-auto">
                <CommandItem
                  value="All tasks"
                  onSelect={() => {
                    router.push(pathname, { scroll: false })
                    setOpen(false)
                  }}
                >
                  All tasks
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
