"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Clock, RefreshCw, Trash2 } from "lucide-react";

interface FormRestorationDialogProps {
  isOpen: boolean;
  onRestore: () => void;
  onStartFresh: () => void;
  savedStep: number;
  savedStepName: string;
  lastSaved?: Date;
}

export default function FormRestorationDialog({
  isOpen,
  onRestore,
  onStartFresh,
  savedStep,
  savedStepName,
  lastSaved,
}: FormRestorationDialogProps) {
  const [isLoading, setIsLoading] = useState(false);
  const handleRestore = async () => {
    setIsLoading(true);
    await new Promise((resolve) => setTimeout(resolve, 500)); // Small delay for UX
    onRestore();
    setIsLoading(false);
  };

  const formatLastSaved = (date?: Date) => {
    if (!date) return "Recently";

    const now = new Date();
    const diffInMinutes = Math.floor(
      (now.getTime() - date.getTime()) / (1000 * 60),
    );

    if (diffInMinutes < 1) return "Just now";
    if (diffInMinutes < 60)
      return `${diffInMinutes} minute${diffInMinutes > 1 ? "s" : ""} ago`;

    const diffInHours = Math.floor(diffInMinutes / 60);
    if (diffInHours < 24)
      return `${diffInHours} hour${diffInHours > 1 ? "s" : ""} ago`;

    const diffInDays = Math.floor(diffInHours / 24);
    return `${diffInDays} day${diffInDays > 1 ? "s" : ""} ago`;
  };

  return (
    <AlertDialog open={isOpen} onOpenChange={() => {}}>
      <AlertDialogContent className="sm:max-w-md">
        <AlertDialogHeader>
          <AlertDialogTitle className="flex items-center gap-2">
            <RefreshCw className="h-5 w-5 text-blue-600" />
            Resume Your Registration
          </AlertDialogTitle>
          <AlertDialogDescription>
            We found a saved registration form. Would you like to continue where
            you left off?
          </AlertDialogDescription>
        </AlertDialogHeader>

        <div className="space-y-4 py-4">
          <div className="bg-blue-50 p-4 rounded-lg space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-blue-900">
                Progress Saved
              </span>
              <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                Step {savedStep} of 6
              </Badge>
            </div>
            <p className="text-sm text-blue-700">
              <strong>{savedStepName}</strong>
            </p>
            <div className="flex items-center gap-1 text-xs text-blue-600">
              <Clock className="h-3 w-3" />
              Last saved {formatLastSaved(lastSaved)}
            </div>
          </div>

          <div className="bg-gray-50 p-3 rounded text-xs text-gray-600">
            <strong>Note:</strong> Your form data is saved locally on this
            device. If you start fresh, your previous progress will be
            permanently deleted.
          </div>
        </div>

        <AlertDialogFooter className="flex gap-2 sm:gap-2">
          <Button
            variant="outline"
            onClick={onStartFresh}
            className="flex items-center gap-2"
            disabled={isLoading}
          >
            <Trash2 className="h-4 w-4" />
            Start Fresh
          </Button>
          <Button
            onClick={handleRestore}
            className="flex items-center gap-2"
            disabled={isLoading}
          >
            <RefreshCw
              className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`}
            />
            {isLoading ? "Restoring..." : "Continue"}
          </Button>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
