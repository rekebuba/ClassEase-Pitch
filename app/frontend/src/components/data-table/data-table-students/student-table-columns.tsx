"use client"

import type * as React from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { DataTableColumnHeader } from "@/components/data-table"
import { Edit, Trash2, Eye, Mail, UserCog, Ellipsis } from "lucide-react"
import type { DataTableRowAction } from "@/types/data-table"
import { Student } from "@/lib/types"
import { MoreHorizontal, Pencil, Trash, User } from "lucide-react"

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { useTransition } from "react"


interface GetStudentsTableColumnsOptions {
  tableId: Record<string, number>
  statusCounts: Record<string, number>
  gradeCounts: Record<string, number>
  attendanceRange: {min: number, max: number}
  averageRange: {min: number, max: number}
  setRowAction: React.Dispatch<React.SetStateAction<DataTableRowAction<Student> | null>>
}

export function getStudentsTableColumns({
  tableId,
  statusCounts,
  gradeCounts,
  attendanceRange,
  averageRange,
  setRowAction,
}: GetStudentsTableColumnsOptions): ColumnDef<Student>[] {
  return [
    {
      id: "select",
      header: ({ table }) => (
        <Checkbox
          checked={table.getIsAllPageRowsSelected() || (table.getIsSomePageRowsSelected() && "indeterminate")}
          onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
          aria-label="Select all"
        />
      ),
      cell: ({ row }) => (
        <Checkbox
          checked={row.getIsSelected()}
          onCheckedChange={(value) => row.toggleSelected(!!value)}
          aria-label="Select row"
        />
      ),
      enableSorting: false,
      enableHiding: false,
      size: 40,
    },
    {
      id: "name",
      accessorKey: "name",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Student" />,
      cell: ({ row }) => {
        const initials = row.original.name
          .split(" ")
          .map((n) => n[0])
          .join("")
          .toUpperCase()

        return (
          <div className="flex items-center gap-3">
            <Avatar className="h-8 w-8">
              <AvatarImage
                src={row.original.avatarUrl || `/placeholder.svg?height=32&width=32&text=${initials}`}
                alt={row.original.name}
              />
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <span className="font-medium">{row.original.name}</span>
              <span className="text-xs text-muted-foreground">{row.original.id}</span>
            </div>
          </div>
        )
      },
      meta: {
        variant: "text",
        label: "Student Name",
        placeholder: "Filter by name...",
      },
      enableColumnFilter: true,
    },
    {
      id: "grade",
      accessorKey: "grade",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Grade" />,
      cell: ({ row }) => (
        <div className="flex items-center">
          <span>{row.original.grade}</span>
          <span className="ml-2 text-muted-foreground">({row.original.section})</span>
        </div>
      ),
      enableColumnFilter: true,
      meta: {
        variant: "multiSelect",
        label: "Grade",
        options: Object.entries(gradeCounts).map(([value, count]) => ({
          label: `Grade ${value}`,
          value: value,
          count,
        }))
      },
    },
    {
      id: "section",
      accessorKey: "section",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Section" />,
      cell: ({ row }) => <div>{row.original.section}</div>,
      enableColumnFilter: true,
      meta: {
        variant: "multiSelect",
        label: "Section",
        options: [
          { label: "Section A", value: "A" },
          { label: "Section B", value: "B" },
          { label: "Section C", value: "C" },
        ],
      },
    },
    {
      id: "status",
      accessorKey: "status",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => {
        const status = row.original.status
        const statusMap = {
          active: { label: "Active", variant: "success" },
          inactive: { label: "Inactive", variant: "secondary" },
          suspended: { label: "Suspended", variant: "destructive" },
        }
        const { label, variant } = statusMap[status]

        return (
          <Badge variant={variant as any} className="capitalize">
            {label}
          </Badge>
        )
      },
      enableColumnFilter: true,
      meta: {
        variant: "select",
        label: "Status",
        options: Object.entries(statusCounts).map(([value, count]) => ({
          label: value.charAt(0).toUpperCase() + value.slice(1),
          value: value,
          count,
        })),
      },
    },
    {
      id: "attendance",
      accessorKey: "attendance",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Attendance" />,
      cell: ({ row }) => {
        const attendance = row.original.attendance
        let color = "text-green-600"
        if (attendance < 80) color = "text-red-600"
        else if (attendance < 90) color = "text-amber-600"

        return (
          <div className="flex items-center">
            <span className={color}>{attendance}%</span>
          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        variant: "range",
        label: "Attendance",
        range: attendanceRange,
        unit: "%",
      },
    },
    {
      id: "averageGrade",
      accessorKey: "averageGrade",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. Grade" />,
      cell: ({ row }) => {
        const grade = row.original.averageGrade
        let color = "text-green-600"
        if (grade < 70) color = "text-red-600"
        else if (grade < 80) color = "text-amber-600"

        return (
          <div className="flex items-center">
            <span className={color}>{grade}%</span>
          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        variant: "range",
        label: "Average Grade",
        range: averageRange,
        unit: "%",
      },
    },
    {
      id: "parent",
      accessorKey: "parentName",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Parent" />,
      cell: ({ row }) => (
        <div className="flex flex-col">
          <span>{row.original.parentName}</span>
          <span className="text-xs text-muted-foreground">{row.original.parentPhone}</span>
        </div>
      ),
      meta: {
        variant: "text",
        label: "Parent Name",
        placeholder: "Filter by parent name...",
      },
    },
    {
      id: "joinedDate",
      accessorKey: "joinedDate",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Joined" />,
      cell: ({ row }) => <div>{row.original.joinedDate}</div>,
      enableSorting: true,
      enableHiding: true,
      meta: {
        variant: "date",
        label: "Joined Date",
      },
    },
    {
      id: "actions",
      cell: function Cell({ row }) {
        const [isUpdatePending, startUpdateTransition] = useTransition();

        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                aria-label="Open menu"
                variant="ghost"
                className="flex size-8 p-0 data-[state=open]:bg-muted"
              >
                <Ellipsis className="size-4" aria-hidden="true" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-40">
              <DropdownMenuItem
                onSelect={() => setRowAction({ row, variant: "view" })}
              >
                <User className="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
                View
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onSelect={() => setRowAction({ row, variant: "delete" })}
              >
                <Trash className="mr-2 h-3.5 w-3.5 text-muted-foreground/70" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ]
}
