import { EmployeeBasicInfo } from "@/client/types.gen";
import { EmployeeApplicationStatusBadge } from "@/components/enum-badge";
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
import { formatDate } from "@/lib/format";
import { getInitials } from "@/utils/utils";
import { ColumnDef, createColumnHelper } from "@tanstack/react-table";
import { MapPin, MoreHorizontalIcon, Phone } from "lucide-react";

const columnHelper = createColumnHelper<EmployeeBasicInfo>();

type EmployeeBasicInfoColumnProps = (
  handleView: (yearId: string) => void,
  handleDelete: (yearId: string) => void,
) => ColumnDef<EmployeeBasicInfo, any>[];

export const employeeBasicInfoColumns: EmployeeBasicInfoColumnProps = (
  handleView,
  handleDelete,
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
    header: "Full Name",
    cell: (props) => {
      // Access the current value
      const fullName = props.getValue();

      // Access other values from the same row
      const firstName = props.row.original.firstName;
      const fatherName = props.row.original.fatherName;
      const primaryPhone = props.row.original.primaryPhone;
      const address = props.row.original.address;

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
              <div className="space-y-1 text-sm text-gray-500">
                <div className="flex items-center gap-1 text-sm">
                  <Phone className="h-3 w-3" />
                  <span className="truncate max-w-[150px]">{primaryPhone}</span>
                </div>
                <div className="flex items-center gap-1 text-sm">
                  <MapPin className="h-3 w-3" />
                  <span className="truncate max-w-[150px]">{address}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
    },
    enableSorting: true,
  }),
  columnHelper.accessor("position", {
    header: "Position",
    cell: (props) => {
      const position = props.getValue();

      const yearsOfExperience = props.row.original.yearsOfExperience;
      return (
        <div className="flex flex-col">
          <div className="font-medium">{position}</div>
          <div className="space-y-1 text-sm text-gray-500">
            <p>{yearsOfExperience} Years</p>
          </div>
        </div>
      );
    },
    enableSorting: true,
  }),
  columnHelper.accessor("highestEducation", {
    header: "Education",
    cell: (props) => {
      const highestEducation = props.getValue();
      const university = props.row.original.university;
      const gpa = props.row.original.gpa;

      return (
        <div className="flex flex-col">
          <div className="font-medium">{highestEducation}</div>
          <div className="space-y-1 text-sm text-gray-500">
            <p className="truncate max-w-[150px]">{university}</p>
          </div>
          <div className="space-y-1 text-sm text-gray-500">
            <p>GPA: {gpa}</p>
          </div>
        </div>
      );
    },
    enableSorting: true,
  }),
  columnHelper.accessor("createdAt", {
    header: "Registration",
    cell: (props) => <div>{formatDate(props.getValue())}</div>,
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
              This action cannot be undone. This will permanently delete The
              Student account and remove your data from our servers.
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
