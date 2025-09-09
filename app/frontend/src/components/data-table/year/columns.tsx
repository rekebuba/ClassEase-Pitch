import { YearSummary } from "@/client";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { formatDate } from "@/lib/format";
import { ColumnDef, createColumnHelper } from "@tanstack/react-table";
import { MoreHorizontalIcon } from "lucide-react";

const columnHelper = createColumnHelper<YearSummary>();

type yearColumnProps = (
  handleView: (yearId: string) => void,
  handleDelete: (yearId: string) => void,
) => ColumnDef<YearSummary, any>[];

export const yearColumns: yearColumnProps = (handleView, handleDelete) => [
  // Display Column
  columnHelper.display({
    id: "checkbox",
    cell: (props) => (
      <Checkbox
        checked={props.row.getIsSelected()}
        onCheckedChange={(value) => props.row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
  }),

  columnHelper.accessor("name", {
    header: "Year Name",
    cell: (props) => <span className="font-medium">{props.getValue()}</span>,
    enableSorting: false,
  }),
  columnHelper.accessor("status", {
    header: "Status",
    cell: (props) => (
      <Badge>
        {props.getValue().charAt(0).toUpperCase() + props.getValue().slice(1)}
      </Badge>
    ),
  }),
  columnHelper.accessor("calendarType", {
    header: "Calendar Type",
    cell: (props) => props.getValue(),
  }),
  columnHelper.accessor("startDate", {
    header: "Start Date",
    cell: (props) => formatDate(props.getValue()),
  }),
  columnHelper.accessor("endDate", {
    header: "End Date",
    cell: (props) => formatDate(props.getValue()),
  }),

  columnHelper.display({
    id: "actions",
    header: "Actions",
    cell: ({ row }) => (
      <AlertDialog>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontalIcon className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem
              onClick={() => navigator.clipboard.writeText(row.original.id)}
            >
              Copy ID
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => handleView(row.original.id)}>
              View
            </DropdownMenuItem>
            <AlertDialogTrigger asChild>
              <DropdownMenuItem
                onSelect={(e) => e.preventDefault()}
                className="text-destructive focus:text-destructive"
              >
                Delete
              </DropdownMenuItem>
            </AlertDialogTrigger>
          </DropdownMenuContent>
        </DropdownMenu>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
            <AlertDialogDescription>
              This action cannot be undone. This will permanently delete
              Academic Year account and remove your data from our servers.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={() => handleDelete(row.original.id)}>
              Continue
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    ),
  }),
];
