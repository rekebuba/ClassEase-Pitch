"use client";

import type { Table } from "@tanstack/react-table";
import { Download } from "lucide-react";

import { Button } from "@/components/ui/button";
import { exportTableToCSV } from "@/lib/export";

import { DeleteStudentsDialog } from "./delete-students-dialog";
import { Student } from "@/lib/types";

import { DownloadIcon } from "@radix-ui/react-icons"
import { useHotkeys } from "react-hotkeys-hook"

import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from "@/components/ui/tooltip"
import { Kbd } from "@/components/kbd"
import { useTableInstanceContext } from "../table-instance-provider";

export function StudentsTableToolbarActions() {
    const { tableInstance: table } = useTableInstanceContext()

    useHotkeys("shift+e", () =>
        exportTableToCSV(table, {
            filename: "tasks",
            excludeColumns: ["select", "actions"],
        })
    )

    return (
        <div className="flex items-center gap-2">
            {table.getFilteredSelectedRowModel().rows.length > 0 ? (
                <DeleteStudentsDialog
                    students={table
                        .getFilteredSelectedRowModel()
                        .rows}
                    onSuccess={() => table.toggleAllRowsSelected(false)}
                />
            ) : null}
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() =>
                                exportTableToCSV(table, {
                                    filename: "tasks",
                                    excludeColumns: ["select", "actions"],
                                })
                            }
                        >
                            <DownloadIcon className="mr-2 size-4" aria-hidden="true" />
                            Export
                        </Button>
                    </TooltipTrigger>
                    <TooltipContent className="flex items-center gap-2 border bg-accent font-semibold text-foreground dark:bg-background/95 dark:backdrop-blur-md dark:supports-[backdrop-filter]:bg-background/40">
                        Export csv
                        <div>
                            <Kbd variant="outline" className="font-sans">
                                ⇧
                            </Kbd>{" "}
                            <Kbd variant="outline" className="font-sans">
                                E
                            </Kbd>
                        </div>
                    </TooltipContent>
                </Tooltip>
            </TooltipProvider>

            {/**
           * Other actions can be added here.
           * For example, import, view, etc.
           */}
        </div>
    )
}
