"use client";

import type React from "react";

import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { LoaderIcon, Save } from "lucide-react";
import { useTableInstanceContext } from "@/components/data-table";
import { SearchParams, StudentsViews } from "@/lib/types";

interface UpdateViewFormProps {
  isUpdated: boolean;
  currentView: StudentsViews;
  searchParams: SearchParams;
  handleUpdateView: (updatedView: StudentsViews) => void;
}

export default function UpdateViewForm({
  isUpdated,
  currentView,
  searchParams,
  handleUpdateView,
}: UpdateViewFormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const { tableInstance } = useTableInstanceContext();

  const visibleColumns =
    tableInstance
      ?.getVisibleFlatColumns()
      .filter(
        (column) =>
          typeof column.accessorFn !== "undefined" && column.getCanHide(),
      )
      .map((column) => column.id) || [];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentView) return;

    setIsLoading(true);

    // Create updated view with current filters
    const updatedView: StudentsViews = {
      viewId: currentView.viewId,
      name: currentView.name,
      tableName: currentView.tableName,
      columns: visibleColumns,
      searchParams: searchParams,
    };

    // Simulate API call
    setTimeout(() => {
      handleUpdateView(updatedView);
      setIsLoading(false);
    }, 500);
  };

  if (!isUpdated || !currentView) return null;

  return (
    <form onSubmit={handleSubmit}>
      <Button variant="outline" size="sm" className="h-8 text-xs">
        <Save className="h-3 w-3 mr-1" />
        {isLoading && (
          <LoaderIcon aria-hidden="true" className="size-3.5 animate-spin" />
        )}
        Update view
      </Button>
    </form>
  );
}
