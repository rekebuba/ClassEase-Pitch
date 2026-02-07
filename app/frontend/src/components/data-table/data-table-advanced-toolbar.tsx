"use client";

import * as React from "react";

import { cn } from "@/lib/utils";

import type { SearchParams } from "@/lib/types";

type DataTableAdvancedToolbarProps<TData> = {
  searchParams: SearchParams;
} & React.ComponentProps<"div">;

export function DataTableAdvancedToolbar<TData>({
  children,
  className,
  searchParams,
  ...props
}: DataTableAdvancedToolbarProps<TData>) {
  return (
    <div
      role="toolbar"
      aria-orientation="horizontal"
      className={cn(
        "flex w-full items-start justify-between gap-2 p-1",
        className,
      )}
      {...props}
    >
      <div className="flex flex-col items-end justify-between gap-3 sm:flex-row sm:items-center">
        <div className="flex items-center gap-2">{children}</div>
      </div>
    </div>
  );
}
