"use client";

import * as React from "react";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";

import { Loader, LoaderIcon, Trash, TrashIcon } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";

import type { Student } from "@/lib/types";
import { useMediaQuery } from "@/hooks/use-media-query";
import { Row, Table } from "@tanstack/react-table";

interface DeleteStudentsDialogProps<TData> {
  students: Row<Student>[];
  showTrigger?: boolean;
  onSuccess?: () => void;
  onOpenChange?: (isOpen: boolean) => void;
}

export function DeleteStudentsDialog({
  students,
  showTrigger = true,
  onSuccess,
  ...props
}: DeleteStudentsDialogProps<Student>) {
  const [isDeleting, setIsDeleting] = React.useState(false);
  const isDesktop = useMediaQuery("(min-width: 640px)");

  function handleDelete() {
    startDeleteTransition(() => {
      new Promise<{ error?: string }>((resolve) =>
        setTimeout(() => resolve({}), 1000),
      ).then(({ error }) => {
        if (error) {
          toast.error(error);
          return;
        }

        // Close the dialog
        props.onOpenChange?.(false);
        toast.success(`${students.length > 1 ? "Tasks" : "Task"} deleted`);
        onSuccess?.();
      });
    });
  }

  const [isDeletePending, startDeleteTransition] = React.useTransition();

  return (
    <Dialog {...props}>
      {showTrigger ? (
        <DialogTrigger asChild>
          <Button variant="outline" size="sm">
            <TrashIcon className="mr-2 size-4" aria-hidden="true" />
            Delete ({students.length})
          </Button>
        </DialogTrigger>
      ) : null}
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you absolutely sure?</DialogTitle>
          <DialogDescription>
            This action cannot be undone. This will permanently delete your{" "}
            <span className="font-medium">{students.length}</span>
            {students.length === 1 ? " task" : " tasks"} from our servers.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter className="gap-2 sm:space-x-0">
          <DialogClose asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button
            aria-label="Delete selected rows"
            variant="destructive"
            onClick={() => handleDelete()}
            disabled={isDeletePending}
          >
            {isDeletePending && (
              <LoaderIcon
                className="mr-1.5 size-4 animate-spin"
                aria-hidden="true"
              />
            )}
            Delete
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
