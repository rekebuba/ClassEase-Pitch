import { EmployeeApplicationStatusEnum as Status } from "@/client/types.gen";
import { Ban, CheckCircle, Clock, LogOut, Pause, XCircle } from "lucide-react";
import React from "react";
import { Button } from "./ui/button";

interface EmployeeStatusActionsProps {
  currentStatus: Status;
  onStatusChange: (newStatus: Status) => void;
}

const statusTransitions: Record<Status, Status[]> = {
  pending: ["active", "approved", "rejected"],
  rejected: ["pending", "interview-scheduled"],
  active: ["inactive", "withdrawn"],
  inactive: ["active", "withdrawn"],
  "interview-scheduled": ["approved", "rejected"],
  approved: ["active", "withdrawn"],
  withdrawn: ["pending"],
};

const statusMeta: Record<
  Status,
  { label: string; icon: React.ElementType; className?: string }
> = {
  pending: {
    label: "Pending",
    icon: Clock,
    className:
      "bg-yellow-100 text-yellow-800 border-yellow-200 hover:bg-yellow-500",
  },
  rejected: {
    label: "Reject",
    icon: XCircle,
    className: "bg-blue-100 text-blue-800 border-blue-200 hover:bg-blue-500",
  },
  active: {
    label: "Activate",
    icon: CheckCircle,
    className: "bg-green-100 hover:bg-green-500",
  },
  inactive: {
    label: "Deactivate",
    icon: Pause,
    className: "bg-red-100 hover:bg-red-500",
  },
  "interview-scheduled": {
    label: "Interview Scheduled",
    icon: Ban,
    className: "bg-purple-100 text-purple-800 hover:bg-purple-500",
  },
  approved: {
    label: "Approve",
    icon: CheckCircle,
    className: "bg-green-100 text-green-800 hover:bg-green-500",
  },
  withdrawn: {
    label: "Withdraw",
    icon: LogOut,
    className: "bg-gray-100 text-gray-800 hover:bg-gray-500",
  },
};

export function EmployeeStatusActions({
  currentStatus,
  onStatusChange,
}: EmployeeStatusActionsProps) {
  const nextStatuses = statusTransitions[currentStatus] || [];

  if (nextStatuses.length === 0) {
    return (
      <p className="text-sm text-gray-500">No further actions available</p>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
      {nextStatuses.map((status) => {
        const { label, icon: Icon, className } = statusMeta[status];
        return (
          <Button
            key={status}
            variant="outline"
            size="sm"
            onClick={() => onStatusChange(status)}
            className={`flex items-center gap-2 ${className}`}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Button>
        );
      })}
    </div>
  );
}
