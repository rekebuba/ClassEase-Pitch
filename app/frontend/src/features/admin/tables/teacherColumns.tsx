import { Button } from "@/components/ui/button";
import { ArrowUpDown } from "lucide-react";
import { MoreHorizontal } from "lucide-react";
import { FaUserCircle } from "react-icons/fa";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuPortal,
} from "@/components/ui/dropdown-menu";

import {
  Dialog,
  DialogPortal,
  DialogTrigger,
  DialogContent,
  DialogDescription,
} from "@/components/ui/dialog";
import { AdminTeacherProfile } from "@/features/admin";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";

export const teacherColumn = [
  {
    accessorKey: "profile",
    id: "actions",
    cell: ({ row }) => {
      const teacher = row.original;

      return (
        <Avatar>
          <AvatarImage src={teacher.image_path} />
          <AvatarFallback>
            <FaUserCircle />
          </AvatarFallback>
        </Avatar>
      );
    },
  },
  {
    accessorKey: "id",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          ID
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
  },
  {
    accessorKey: "firstName",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          first Name
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
  },
  {
    accessorKey: "lastName",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          last Name
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
  },
  {
    accessorKey: "email",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          email
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
  },
  {
    accessorKey: "markList",
    header: ({ column }) => {
      return (
        <Button
          variant="mark List"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          mark List
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const teacher = row.original;

      return (
        <Dialog>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="h-8 w-8 p-0">
                <span className="sr-only">Open menu</span>
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuPortal>
              <DropdownMenuContent>
                <DialogTrigger>
                  <DropdownMenuItem>Detail</DropdownMenuItem>
                </DialogTrigger>
              </DropdownMenuContent>
            </DropdownMenuPortal>
          </DropdownMenu>
          <DialogPortal>
            <DialogContent className="overflow-scroll max-w-5xl max-h-[90vh]">
              <DialogDescription>
                <AdminTeacherProfile teacherData={teacher} />
              </DialogDescription>
            </DialogContent>
          </DialogPortal>
        </Dialog>
      );
    },
  },
];
