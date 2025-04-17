"use client"
import { Button } from "@/components/ui/button"
import { Download, Mail, Trash2 } from "lucide-react"
import type { Table } from "@tanstack/react-table"
import type { Student } from "@/lib/types"
import { DataTableActionBar, DataTableActionBarAction, DataTableActionBarSelection } from "../data-table-action-bar"
import { Separator } from "@radix-ui/react-separator"
import { useCallback, useState, useTransition } from "react"

const actions = [
    "export",
    "delete",
] as const;

type Action = (typeof actions)[number];

interface StudentsTableActionBarProps {
    table: Table<Student>
}

export function StudentsTableActionBar({ table }: StudentsTableActionBarProps) {
    const selectedRows = table.getFilteredSelectedRowModel().rows
    const hasSelectedRows = selectedRows.length > 0
    const [isPending, startTransition] = useTransition();
    const [currentAction, setCurrentAction] = useState<Action | null>(null);


    const getIsActionPending = useCallback(
        (action: Action) => isPending && currentAction === action,
        [isPending, currentAction],
    );

    const handleExport = () => {
        // Export functionality would go here
        console.log("Exporting", selectedRows.length, "students")
    }

    const handleEmail = () => {
        // Email functionality would go here
        console.log("Emailing parents of", selectedRows.length, "students")
    }

    const handleDelete = () => {
        // Delete functionality would go here
        console.log("Deleting", selectedRows.length, "students")
    }

    if (!hasSelectedRows) return null

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
                    onClick={handleDelete}
                >
                    <Trash2 />
                </DataTableActionBarAction>
            </div>
        </DataTableActionBar>
    )
}
