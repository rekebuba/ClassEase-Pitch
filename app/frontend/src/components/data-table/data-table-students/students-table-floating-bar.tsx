"use client";
import { Separator } from "@radix-ui/react-separator";
import { Download, Trash2 } from "lucide-react";
import { useCallback, useState, useTransition } from "react";
import { toast } from "sonner";

import {
  DataTableActionBar,
  DataTableActionBarAction,
  DataTableActionBarSelection,
  useTableInstanceContext,
} from "@/components/data-table";

const actions = ["export", "delete"] as const;

type Action = (typeof actions)[number];

export function StudentsTableFloatingBar() {
  const { tableInstance: table } = useTableInstanceContext();

  const selectedRows = table.getFilteredSelectedRowModel().rows;
  const hasSelectedRows = selectedRows.length > 0;
  const [isPending, startTransition] = useTransition();
  const [currentAction, setCurrentAction] = useState<Action | null>(null);

  const getIsActionPending = useCallback(
    (action: Action) => isPending && currentAction === action,
    [isPending, currentAction],
  );

  const handleExport = () => {
    // Export functionality would go here
    console.log("Exporting", selectedRows.length, "students");
  };

  const onTaskDelete = useCallback(() => {
    setCurrentAction("delete");
    startTransition(() => {
      new Promise<{ error?: string }>(resolve =>
        setTimeout(() => resolve({}), 1000),
      ).then(({ error }) => {
        if (error) {
          toast.error(error);
        }
      });
      table.toggleAllRowsSelected(false);
    });
  }, [selectedRows, table]);

  if (!hasSelectedRows)
    return null;

  return (
    <DataTableActionBar table={table} visible={selectedRows.length > 0}>
      <DataTableActionBarSelection table={table} />
      <Separator
        orientation="vertical"
        className="hidden data-[orientation=vertical]:h-5 sm:block"
      />
      <div className="flex items-center gap-1.5">
        <DataTableActionBarAction
          size="icon"
          tooltip="Export tasks"
          isPending={getIsActionPending("export")}
          onClick={handleExport}
        >
          <Download />
        </DataTableActionBarAction>
        <DataTableActionBarAction
          size="icon"
          tooltip="Delete tasks"
          isPending={getIsActionPending("delete")}
          onClick={onTaskDelete}
        >
          <Trash2 />
        </DataTableActionBarAction>
      </div>
    </DataTableActionBar>
  );
}
