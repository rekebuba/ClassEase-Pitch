"use client";

import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

import { SearchParams, StudentsViews, View } from "@/lib/types";
import isEqual from "lodash/isEqual";
import { Save } from "lucide-react";
import { toast } from "sonner";
import { useTableInstanceContext } from "../table-instance-provider";
import { CreateViewForm } from "./create-view-form";
import UpdateViewForm from "./update-view-form";

interface CreateViewPopoverProps {
  SearchParams: SearchParams;
  views: StudentsViews[];
  currentViewId: string | null;
  refetchViews: () => void;
  setCurrentViewId: (viewId: string | null) => void;
}

export function CreateViewPopover({
  SearchParams,
  views,
  refetchViews,
  currentViewId,
  setCurrentViewId,
}: CreateViewPopoverProps) {
  const [open, setOpen] = useState(false);

  const [allowCreate, setAllowCreate] = useState(false);
  const [allowUpdate, setAllowUpdate] = useState(false);

  const { tableInstance } = useTableInstanceContext();

  const visibleColumns =
    tableInstance
      ?.getVisibleFlatColumns()
      .filter(
        (column) =>
          typeof column.accessorFn !== "undefined" && column.getCanHide(),
      )
      .map((column) => column.id) || [];

  const [visibleColumnsState, setVisibleColumnsState] =
    useState<String[]>(visibleColumns);

  const currentView = views.find((view) => view.viewId === currentViewId);

  useEffect(() => {
    const isCurrentViewDifferent =
      currentView && !isEqual(currentView.searchParams, SearchParams);

    const isColumnLengthDifferent =
      currentView && currentView.columns.length !== visibleColumns.length;

    // Set allowUpdate when a view is selected and either searchParams or columns changed
    if (currentView && (isCurrentViewDifferent || isColumnLengthDifferent)) {
      setAllowUpdate(true);
    } else {
      setAllowUpdate(false);
    }

    const defaultSearchParams: SearchParams = {
      page: 1,
      perPage: 10,
      sort: [],
      filters: [],
      joinOperator: "and",
    };

    // If no view is selected
    if (!currentViewId && SearchParams) {
      const isSearchParamsModified = !isEqual(
        SearchParams,
        defaultSearchParams,
      );
      const isVisibleColumnsChanged =
        currentView &&
        currentView.columns.length !== visibleColumnsState.length;

      if (
        isSearchParamsModified ||
        isVisibleColumnsChanged ||
        visibleColumnsState.length !== visibleColumns.length
      ) {
        setAllowCreate(true);
      } else {
        setAllowCreate(false);
      }
    }
  }, [
    currentView,
    views,
    SearchParams,
    visibleColumns,
    visibleColumnsState,
    currentViewId,
  ]);

  const handleCreateView = async (newView: View) => {
    // const result = await createNewView(newView);
    toast.error(result.message, {
      style: { color: "green" },
    });
    refetchViews();
    setCurrentViewId(result?.viewId);
  };

  const handleUpdateView = async (updatedView: StudentsViews) => {
    // const result = await updateView(updatedView);
    toast.error(result.message, {
      style: { color: "green" },
    });
    refetchViews();
    setCurrentViewId(result?.viewId);
  };

  return (
    <>
      {allowCreate ? (
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button variant="outline" size="sm" className="h-8 text-xs">
              <Save className="h-3 w-3 mr-1" />
              Save as new view
            </Button>
          </PopoverTrigger>
          <PopoverContent
            className="w-[12.5rem] p-0 dark:bg-background/95 dark:backdrop-blur-md dark:supports-[backdrop-filter]:bg-background/40"
            align="end"
          >
            <CreateViewForm
              SearchParams={SearchParams}
              onSuccess={() => setOpen(false)}
              onCreateView={handleCreateView}
            />
          </PopoverContent>
        </Popover>
      ) : (
        <UpdateViewForm
          isUpdated={allowUpdate}
          currentView={currentView as StudentsViews}
          searchParams={SearchParams}
          handleUpdateView={handleUpdateView}
        />
      )}
    </>
  );
}
