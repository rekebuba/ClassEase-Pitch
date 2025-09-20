import { TeacherBasicInfo } from "@/client/types.gen";
import { EmployeeApplicationStatusBadge } from "@/components/enum-badge";
import { AlertDialog } from "@/components/ui/alert-dialog";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
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
import { getInitials } from "@/utils/utils";
import { ColumnDef, createColumnHelper } from "@tanstack/react-table";
import { MoreHorizontalIcon } from "lucide-react";

const columnHelper = createColumnHelper<TeacherBasicInfo>();

type TeacherBasicInfoColumnProps = (
  handleView: (yearId: string) => void,
) => ColumnDef<TeacherBasicInfo, any>[];

export const teacherBasicInfoColumns: TeacherBasicInfoColumnProps = (
  handleView,
) => [
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
  columnHelper.accessor("fullName", {
    header: "Teacher Name",
    cell: (props) => {
      // Access the current value
      const fullName = props.getValue();

      // Access other values from the same row
      const firstName = props.row.original.firstName;
      const fatherName = props.row.original.fatherName;

      return (
        <div>
          <div className="flex items-center gap-3">
            <Avatar className="h-10 w-10">
              <AvatarImage src={"/placeholder.svg"} />
              <AvatarFallback>
                {getInitials(firstName, fatherName)}
              </AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <span className="font-medium">{fullName}</span>
            </div>
          </div>
        </div>
      );
    },
    enableSorting: true,
  }),
  columnHelper.accessor("subjects", {
    header: "Subjects",
    cell: (props) => {
      const subjects = props.row.original.subjects
        .map((sub) => sub.name)
        .join(", ");

      return <div className="flex flex-col">{subjects}</div>;
    },
    enableSorting: true,
  }),
  columnHelper.accessor("status", {
    header: "Status",
    cell: (props) => {
      return <EmployeeApplicationStatusBadge status={props.getValue()} />;
    },
    enableSorting: true,
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
          </DropdownMenuContent>
        </DropdownMenu>
      </AlertDialog>
    ),
  }),
];
