"use client";

import { ChevronLeftIcon } from "@radix-ui/react-icons";
import { LoaderIcon } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";

import { useTableInstanceContext } from "@/components/data-table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";

import type { SearchParams } from "@/lib/types";
import type React from "react";

type CreateViewFormProps = {
  backButton?: true;
  onBack?: () => void;
  onSuccess?: () => void;
  SearchParams?: SearchParams;
  onCreateView?: (newView: any) => void;
};

export function CreateViewForm({
  backButton,
  SearchParams,
  onBack,
  onSuccess,
  onCreateView,
}: CreateViewFormProps) {
  const [pending, setPending] = useState(false);
  const [viewName, setViewName] = useState("");
  const nameInputRef = useRef<HTMLInputElement>(null);

  const { tableInstance } = useTableInstanceContext();

  const visibleColumns
    = tableInstance
      ?.getVisibleFlatColumns()
      .filter(
        column =>
          typeof column.accessorFn !== "undefined" && column.getCanHide(),
      )
      .map(column => column.id) || [];

  useEffect(() => {
    nameInputRef.current?.focus();
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!viewName.trim()) {
      toast.error("View name is required");
      return;
    }

    setPending(true);

    // Create a new view object
    const newView = {
      name: viewName,
      table_name: "students",
      columns: visibleColumns,
      searchParams: SearchParams || {},
    };

    // Simulate API call
    setTimeout(() => {
      if (onCreateView) {
        onCreateView(newView);
      }
      setPending(false);
      onSuccess?.();
    }, 500);
  };

  return (
    <div>
      {backButton && (
        <>
          <div className="flex items-center gap-1 px-1 py-1.5">
            <Button
              variant="ghost"
              size="icon"
              className="size-6"
              onClick={() => onBack?.()}
            >
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
          onChange={e => setViewName(e.target.value)}
        />
        <Button disabled={pending} size="sm" type="submit">
          {pending
            ? (
                <LoaderIcon aria-hidden="true" className="size-3.5 animate-spin" />
              )
            : (
                "Create"
              )}
        </Button>
      </form>
    </div>
  );
}
