"use client"

import type * as React from "react"
import type { ColumnDef } from "@tanstack/react-table"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { DataTableColumnHeader } from "@/components/data-table"
import { Edit, Trash2, Eye, Mail, UserCog, Ellipsis } from "lucide-react"
import type { DataTableRowAction } from "@/types/data-table"
import { AverageRange, SectionCounts, Student, TableId } from "@/lib/types"
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
import { number, object } from "zod"


interface GetStudentsTableColumnsOptions {
  tableId: TableId
  statusCounts: Record<string, number>
  gradeCounts: Record<string, number>
  sectionCounts: SectionCounts;
  averageRange: AverageRange,
  setRowAction: React.Dispatch<React.SetStateAction<DataTableRowAction<Student> | null>>
}

export function getStudentsTableColumns({
  tableId,
  statusCounts,
  sectionCounts,
  gradeCounts,
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
      id: "firstName_fatherName_grandFatherName",
      accessorKey: "firstName_fatherName_grandFatherName",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Student" />,
      cell: ({ row }) => {
        const initials = row.original.firstName_fatherName_grandFatherName
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
                alt={row.original.firstName_fatherName_grandFatherName}
              />
              <AvatarFallback>{initials}</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <span className="font-medium">{row.original.firstName_fatherName_grandFatherName}</span>
              <span className="text-xs text-muted-foreground">{row.original.identification}</span>
            </div>
          </div>
        )
      },
      meta: {
        variant: "text",
        label: "Student Name",
        placeholder: "Filter by name...",
        tableId: tableId?.firstName_fatherName_grandFatherName,
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
        tableId: tableId?.identification,
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
          <span className="ml-2 text-muted-foreground">({row.original.sectionSemesterOne})-({row.original.sectionSemesterTwo})</span>
        </div>
      ),
      enableColumnFilter: true,
      meta: {
        variant: "multiSelect",
        label: "Grade",
        options: Object.entries(gradeCounts).map(([value, count]) => ({
          label: `Grade ${value}`,
          value: value,
          count: count,
        })),
        tableId: tableId?.grade,
      },
    },
    {
      id: "sectionSemesterOne",
      accessorKey: "sectionSemesterOne",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Section I" />,
      cell: ({ row }) => <div>{row.original.sectionSemesterOne}</div>,
      enableColumnFilter: true,
      meta: {
        variant: "multiSelect",
        label: "Section I",
        options: Object.entries(sectionCounts?.sectionSemesterOne || {})
          .filter(([_, count]) => count > 0)
          .map(([value, count]) => ({
            label: `Section ${value}`,
            value: value,
            count: count,
          })),
        tableId: tableId?.sectionSemesterOne,
      },
    },
    {
      id: "sectionSemesterTwo",
      accessorKey: "sectionSemesterTwo",
      header: ({ column }) => <DataTableColumnHeader column={column} title="section II" />,
      cell: ({ row }) => <div>{row.original.sectionSemesterTwo}</div>,
      enableColumnFilter: true,
      meta: {
        variant: "multiSelect",
        label: "section II",
        options: Object.entries(sectionCounts?.sectionSemesterTwo || {})
          .filter(([_, count]) => count > 0)
          .map(([value, count]) => ({
            label: `Section ${value}`,
            value: value,
            count: count,
          })),
        tableId: tableId?.sectionSemesterTwo,
      },
    },
    {
      id: "averageSemesterOne",
      accessorKey: "averageSemesterOne",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. I" />,
      cell: ({ row }) => {
        const score = row.original.averageSemesterOne
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
        tableId: tableId?.averageSemesterOne,
        variant: "range",
        label: "Average I",
        range: averageRange.averageSemesterOne,
        unit: "%",
      },
    },
    {
      id: "averageSemesterTwo",
      accessorKey: "averageSemesterTwo",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. II" />,
      cell: ({ row }) => {
        const score = row.original.averageSemesterTwo
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
        tableId: tableId?.averageSemesterTwo,
        variant: "range",
        label: "Average II",
        range: averageRange.averageSemesterTwo,
        unit: "%",
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
            <span className="text-xs text-muted-foreground">{row.original.averageSemesterOne}%-{row.original.averageSemesterTwo}%</span>
          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        tableId: tableId?.finalScore,
        variant: "range",
        label: "Average Grade",
        range: averageRange.totalAverage,
        unit: "%",
      },
    },
    {
      id: "rankSemesterOne",
      accessorKey: "rankSemesterOne",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. rankI" />,
      cell: ({ row }) => {
        const score = row.original.rankSemesterOne
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
        tableId: tableId?.rankSemesterOne,
        variant: "range",
        label: "rank I",
        range: averageRange.rankSemesterOne,
      },
    },
    {
      id: "rankSemesterTwo",
      accessorKey: "rankSemesterTwo",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Avg. rankII" />,
      cell: ({ row }) => {
        const score = row.original.rankSemesterTwo
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
        tableId: tableId?.rankSemesterTwo,
        variant: "range",
        label: "rank II",
        range: averageRange.rankSemesterTwo,
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
            <span className="text-xs text-muted-foreground">{row.original.rankSemesterOne}-{row.original.rankSemesterTwo}</span>

          </div>
        )
      },
      enableColumnFilter: true,
      meta: {
        tableId: tableId?.rank,
        variant: "range",
        label: "rank",
        range: averageRange.rank,
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
      enableColumnFilter: true,
      meta: {
        tableId: tableId?.guardianName,
        variant: "text",
        label: "Parent Name",
        placeholder: "Filter by parent name...",
      },
    },
    {
      id: "guardianPhone",
      accessorKey: "guardianPhone",
      header: ({ column }) => <DataTableColumnHeader column={column} title="guardian Phone No." />,
      cell: ({ row }) => (
        <div className="flex items-center">
          <span>{row.original.guardianPhone}</span>
        </div>
      ),
      enableColumnFilter: true,
      meta: {
        variant: "text",
        label: "guardian Phone",
        tableId: tableId?.guardianPhone,
      },
    },
    {
      id: "createdAt",
      accessorKey: "createdAt",
      header: ({ column }) => <DataTableColumnHeader column={column} title="Joined" />,
      cell: ({ row }) => <div>{row.original.createdAt}</div>,
      enableColumnFilter: true,
      meta: {
        tableId: tableId?.createdAt,
        variant: "dateRange",
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
