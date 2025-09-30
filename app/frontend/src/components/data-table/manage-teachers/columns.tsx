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
import { JSX } from "react/jsx-runtime";

const columnHelper = createColumnHelper<TeacherBasicInfo>();

type TeacherBasicInfoColumnProps = (
  handleView: (yearId: string) => void,
  data: TeacherBasicInfo[],
) => ColumnDef<TeacherBasicInfo, any>[];

export const teacherBasicInfoColumns: TeacherBasicInfoColumnProps = (
  handleView,
  data,
) => {
  const createTermColumns = () => {
    // Get all unique term names from all teachers

    return ["1", "2"].map((termName) =>
      columnHelper.display({
        id: `term${termName}`,
        header: `Term ${termName}`,
        cell: (props) => {
          const yearRecords = props.row.original.years;

          // Array to collect all grade summaries for this term
          const gradeSummaries: JSX.Element[] = [];

          // Loop through each year
          yearRecords.forEach((year) => {
            // Find the academic term that matches our current column term
            const academicTerm = year.academicTerms.find(
              (term) => term.name === termName,
            );

            if (academicTerm) {
              // Loop through grades in this term
              academicTerm.grades.forEach((gradeObj) => {
                // Get unique sections for this grade and format them
                const sections = [
                  ...new Set(
                    gradeObj.sections.map((section) => section.section),
                  ),
                ];

                // Get unique subject names for this grade
                const subjects = [
                  ...new Set(gradeObj.subjects.map((subject) => subject.code)),
                ];

                // Create the summary with proper styling
                const summary = (
                  <div key={gradeObj.id} className="mb-2 last:mb-0">
                    <div className="font-semibold text-gray-800 truncate max-w-[150px]">
                      <span>Grade {gradeObj.grade}</span>
                      <span className="inline-flex items-center px-1 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                        ({sections.join(",")})
                      </span>
                      <span className="text-gray-400 mx-1">•</span>
                      <span className="text-sm text-gray-600">
                        {subjects.join(", ")}
                      </span>
                    </div>
                  </div>
                );
                gradeSummaries.push(summary);
              });
            }
          });

          // Return all summaries or a default message
          return gradeSummaries.length > 0 ? (
            <div className="space-y-2 py-1">{gradeSummaries}</div>
          ) : (
            <span className="text-gray-400 text-sm italic">No assignments</span>
          );
        },
      }),
    );
  };

  return [
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
    // Dynamic term columns
    ...createTermColumns(),
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
};
