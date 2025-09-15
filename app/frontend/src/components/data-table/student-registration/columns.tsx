import { StudentBasicInfo } from "@/client";
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
import { ColumnDef, createColumnHelper } from "@tanstack/react-table";
import {
  AlertTriangle,
  CheckCircle,
  Heart,
  Mail,
  MapPin,
  MoreHorizontalIcon,
  Phone,
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { formatDate } from "@/lib/format";
import { Badge } from "@/components/ui/badge";
import StudentStatusBadge from "@/components/student-status-badge";

const columnHelper = createColumnHelper<StudentBasicInfo>();

type StudentBasicInfoColumnProps = (
  handleView: (yearId: string) => void,
  handleDelete: (yearId: string) => void
) => ColumnDef<StudentBasicInfo, any>[];

const getInitials = (fullName: string) => {
  const name = fullName.split(" ");
  return `${name[0].charAt(0)}${name[1].charAt(0)}`.toUpperCase();
};

const calculateAge = (dateOfBirth: string) => {
  const today = new Date();
  const birthDate = new Date(dateOfBirth);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  if (
    monthDiff < 0 ||
    (monthDiff === 0 && today.getDate() < birthDate.getDate())
  ) {
    age--;
  }
  return age;
};

export const studentBasicInfoColumns: StudentBasicInfoColumnProps = (
  handleView,
  handleDelete
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
      const fatherPhone = props.row.original.fatherPhone;
      const siblingInSchool = props.row.original.siblingInSchool;
      const address = props.row.original.address;

      return (
        <div>
          <div className="flex items-center gap-3">
            <Avatar className="h-10 w-10">
              <AvatarImage src={"/placeholder.svg"} />
              <AvatarFallback>{getInitials(fullName)}</AvatarFallback>
            </Avatar>
            <div className="flex flex-col">
              <span className="font-medium">{fullName}</span>
              <div className="space-y-1 text-sm text-gray-500">
                <div className="flex items-center gap-1 text-sm">
                  <Phone className="h-3 w-3" />
                  <span>{fatherPhone}</span>
                </div>
                <div className="flex items-center gap-1 text-sm">
                  <MapPin className="h-3 w-3" />
                  <span className="truncate max-w-[150px]">{address}</span>
                </div>
                {siblingInSchool && (
                  <Badge variant="outline" className="text-xs">
                    Has Sibling
                  </Badge>
                )}
              </div>
            </div>
          </div>
        </div>
      );
    },
    enableSorting: true,
  }),
  columnHelper.accessor("dateOfBirth", {
    header: "Date of Birth",
    cell: (props) => (
      <div>
        <div>{formatDate(props.getValue())}</div>
        <div className="text-sm text-gray-500">
          Age: {calculateAge(props.getValue())}
        </div>
      </div>
    ),
    enableSorting: true,
  }),
  columnHelper.accessor("grade.grade", {
    header: "Grade",
    cell: (props) => {
      const grade = props.getValue();
      const isTransfer = props.row.original.isTransfer;

      return (
        <div className="flex flex-col">
          <Badge className="bg-blue-100 text-blue-800 mb-1">
            Grade {grade}
          </Badge>
          {isTransfer && (
            <Badge
              variant="outline"
              className="bg-orange-100 text-orange-800 text-xs"
            >
              Transfer
            </Badge>
          )}
        </div>
      );
    },
  }),
  columnHelper.accessor("hasMedicalCondition", {
    header: "Medical Condition",
    cell: (props) => {
      const hasMedicalCondition = props.getValue();
      const hasDisability = props.row.original.hasDisability;

      return (
        <div className="space-y-1">
          {hasMedicalCondition && (
            <Badge
              variant="destructive"
              className="text-xs flex items-center gap-1 w-fit"
            >
              <Heart className="h-3 w-3" />
              Medical
            </Badge>
          )}
          {hasDisability && (
            <Badge
              variant="destructive"
              className="text-xs flex items-center gap-1 w-fit"
            >
              <AlertTriangle className="h-3 w-3" />
              Disability
            </Badge>
          )}
          {!hasMedicalCondition && !hasDisability && (
            <Badge className="bg-green-100 text-green-800 text-xs flex items-center gap-1 w-fit">
              <CheckCircle className="h-3 w-3" />
              Healthy
            </Badge>
          )}
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
      return <StudentStatusBadge status={props.getValue()} />;
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
