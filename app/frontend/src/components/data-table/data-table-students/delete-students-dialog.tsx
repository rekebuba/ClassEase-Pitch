"use client"

import * as React from "react"
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

import { Loader, Trash } from "lucide-react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button"

import type { Student } from "@/lib/types"
import { useMediaQuery } from "@/hooks/use-media-query"

interface DeleteStudentsDialogProps {
    open: boolean
    onOpenChange: (open: boolean) => void
    students: Student[]
    showTrigger?: boolean
    onSuccess?: () => void
}

export function DeleteStudentsDialog({
    open,
    students,
    showTrigger = true,
    onSuccess,
    ...props
}: DeleteStudentsDialogProps) {
    const [isDeletePending, startDeleteTransition] = React.useTransition();
    const [isDeleting, setIsDeleting] = React.useState(false)
    const isDesktop = useMediaQuery("(min-width: 640px)");

    function handleDelete() {
        startDeleteTransition(() => {
            new Promise<{ error?: string }>((resolve) => setTimeout(() => resolve({}), 1000)).then(({ error }) => {

                if (error) {
                    toast.error(error);
                    return;
                }
                
                // Close the dialog
                props.onOpenChange?.(false);
                toast.success("Tasks deleted");
                onSuccess?.();
            });
        });
    }


    if (isDesktop) {
        return (
            <Dialog {...props}>
                {showTrigger ? (
                    <DialogTrigger asChild>
                        <Button variant="outline" size="sm">
                            <Trash className="mr-2 size-4" aria-hidden="true" />
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
                            onClick={handleDelete}
                            disabled={isDeletePending}
                        >
                            {isDeletePending && (
                                <Loader
                                    className="mr-2 size-4 animate-spin"
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

    return (
        <Drawer {...props}>
            {showTrigger ? (
                <DrawerTrigger asChild>
                    <Button variant="outline" size="sm">
                        <Trash className="mr-2 size-4" aria-hidden="true" />
                        Delete ({students.length})
                    </Button>
                </DrawerTrigger>
            ) : null}
            <DrawerContent>
                <DrawerHeader>
                    <DrawerTitle>Are you absolutely sure?</DrawerTitle>
                    <DrawerDescription>
                        This action cannot be undone. This will permanently delete your{" "}
                        <span className="font-medium">{students.length}</span>
                        {students.length === 1 ? " student" : " students"} from our servers.
                    </DrawerDescription>
                </DrawerHeader>
                <DrawerFooter className="gap-2 sm:space-x-0">
                    <DrawerClose asChild>
                        <Button variant="outline">Cancel</Button>
                    </DrawerClose>
                    <Button
                        aria-label="Delete selected rows"
                        variant="destructive"
                        onClick={handleDelete}
                        disabled={isDeletePending}
                    >
                        {isDeletePending && (
                            <Loader className="mr-2 size-4 animate-spin" aria-hidden="true" />
                        )}
                        Delete
                    </Button>
                </DrawerFooter>
            </DrawerContent>
        </Drawer>
    );
}
