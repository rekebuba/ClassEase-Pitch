"use client"

import type * as React from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { DataTableColumnHeader } from "@/components/data-table"
import { Edit, Trash2, Eye, Mail, UserCog, Ellipsis } from "lucide-react"
import type { DataTableRowAction } from "@/types/data-table"
import { Student, TableId } from "@/lib/types"
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
import { types } from "util"
import { number } from "zod"


interface GetStudentsTableColumnsOptions {
  tableId: TableId
  statusCounts: Record<string, number>
  gradeCounts: Record<string, number>
  attendanceRange: { min: number, max: number }
  averageRange: { min: number, max: number }
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
      id: "studentName",
      accessorKey: "studentName",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Student" />,
      cell: ({ row }) => {
        const initials = row.original.studentName
          .split(" ")
          .slice(0, 2)
          .map((n) => n[0])
          .join("")
          .toUpperCase()

        return (
          <div className="flex items-center gap-3">
            <Avatar className="h-8 w-8">
              <AvatarImage
                src={row.original.imagePath || `/placeholder.svg?height=32&width=32&text=${initials}`}
                alt={row.original.studentName}
              />
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <span className="font-medium">{row.original.studentName}</span>
              <span className="text-xs text-muted-foreground">{row.original.identification}</span>
            </div>
          </div>
        )
      },
      meta: {
        variant: "text",
        label: "Student Name",
        placeholder: "Filter by name...",
        tableId: tableId.studentName,
      },
      enableColumnFilter: true,
    },
    {
      id: "identification",
      accessorKey: "identification",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Student Id" />,
      cell: ({ row }) => (
        <div className="flex items-center">
          <span>{row.original.identification}</span>
        </div>
      ),
      enableColumnFilter: true,
      meta: {
        variant: "text",
        label: "Student Id",
        tableId: tableId.identification,
      },
      enableHiding: true,
    },
    {
      id: "grade",
      accessorKey: "grade",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Grade" />,
      cell: ({ row }) => (
        <div className="flex flex-col">
          <span className="font-medium">Grade {row.original.grade}</span>
          <span className="ml-2 text-muted-foreground">({row.original.sectionI})-({row.original.sectionII})</span>
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
        })),
        tableId: tableId.grade,
      },
    },
    {
      id: "sectionI",
      accessorKey: "sectionI",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Section I" />,
      cell: ({ row }) => <div>{row.original.sectionI}</div>,
      enableColumnFilter: true,
      meta: {
        tableId: tableId.sectionI,
        variant: "multiSelect",
        label: "Section I",
        options: [
          { label: "Section A", value: "A" },
          { label: "Section B", value: "B" },
          { label: "Section C", value: "C" },
        ],
      },
    },
    {
      id: "sectionII",
      accessorKey: "sectionII",
      header: ({ column }) => <DataTableColumnHeader column={column} title="section II" />,
      cell: ({ row }) => <div>{row.original.sectionII}</div>,
      enableColumnFilter: true,
      meta: {
        tableId: tableId.sectionII,
        variant: "multiSelect",
        label: "section II",
        options: [
          { label: "Section A", value: "A" },
          { label: "Section B", value: "B" },
          { label: "Section C", value: "C" },
        ],
      },
    },
    {
      id: "finalScore",
      accessorKey: "finalScore",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. Grade" />,
      cell: ({ row }) => {
        const score = row.original.finalScore
        let color = "text-green-600"
        if (typeof score === "number") {
          if (score < 70) color = "text-red-600"
          else if (score < 80) color = "text-amber-600"
        }

        return (
          <div className="flex flex-col">
            <span className={`font-medium ${color}`}>{score}%</span>
            <span className="text-xs text-muted-foreground">{row.original.averageI}%-{row.original.averageI}%</span>
          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        tableId: tableId.finalScore,
        variant: "range",
        label: "Average Grade",
        range: averageRange,
        unit: "%",
      },
    },
    {
      id: "averageI",
      accessorKey: "averageI",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. I" />,
      cell: ({ row }) => {
        const score = row.original.averageI
        let color = "text-green-600"
        if (typeof score === "number") {
          if (score < 70) color = "text-red-600"
          else if (score < 80) color = "text-amber-600"
        }
        return (
          <div className="flex items-center">
            <span className={color}>{score}%</span>
          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        tableId: tableId.averageI,
        variant: "range",
        label: "Average I",
        range: averageRange,
        unit: "%",
      },
    },
    {
      id: "averageII",
      accessorKey: "averageII",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. II" />,
      cell: ({ row }) => {
        const score = row.original.averageII
        let color = "text-green-600"
        if (typeof score === "number") {
          if (score < 70) color = "text-red-600"
          else if (score < 80) color = "text-amber-600"
        }
        return (
          <div className="flex items-center">
            <span className={color}>{score}%</span>
          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        tableId: tableId.averageII,
        variant: "range",
        label: "Average II",
        range: averageRange,
        unit: "%",
      },
    },
    {
      id: "rank",
      accessorKey: "rank",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. rank" />,
      cell: ({ row }) => {
        const score = row.original.rank
        let color = "text-green-600"
        if (typeof score === "number") {
          if (score < 70) color = "text-red-600"
          else if (score < 80) color = "text-amber-600"
        }
        return (
          <div className="flex flex-col">
            <span className={`font-medium ${color}`}>{score}</span>
            <span className="text-xs text-muted-foreground">{row.original.rankI}-{row.original.rankII}</span>

          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        tableId: tableId.rank,
        variant: "range",
        label: "rank",
        range: averageRange,
      },
    },
    {
      id: "rankI",
      accessorKey: "rankI",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. rankI" />,
      cell: ({ row }) => {
        const score = row.original.rankI
        let color = "text-green-600"
        if (typeof score === "number") {
          if (score < 70) color = "text-red-600"
          else if (score < 80) color = "text-amber-600"
        }
        return (
          <div className="flex items-center">
            <span className={color}>{score}%</span>
          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        tableId: tableId.rankI,
        variant: "range",
        label: "rank I",
        range: averageRange,
      },
    },
    {
      id: "rankII",
      accessorKey: "rankII",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. rankII" />,
      cell: ({ row }) => {
        const score = row.original.rankII
        let color = "text-green-600"
        if (typeof score === "number") {
          if (score < 70) color = "text-red-600"
          else if (score < 80) color = "text-amber-600"
        }
        return (
          <div className="flex items-center">
            <span className={color}>{score}%</span>
          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        tableId: tableId.rankII,
        variant: "range",
        label: "rank II",
        range: averageRange,
      },
    },
    {
      id: "guardianName",
      accessorKey: "guardianName",
      header: ({ column }) => <DataTableColumnHeader column={column} title="guardian Name" />,
      cell: ({ row }) => (
        <div className="flex flex-col">
          <span>{row.original.guardianName}</span>
          <span className="text-xs text-muted-foreground">{row.original.guardianPhone}</span>
        </div>
      ),
      meta: {
        tableId: tableId.guardianName,
        variant: "text",
        label: "Parent Name",
        placeholder: "Filter by parent name...",
      },
    },
    {
      id: "createdAt",
      accessorKey: "createdAt",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Joined" />,
      cell: ({ row }) => <div>{row.original.createdAt}</div>,
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
