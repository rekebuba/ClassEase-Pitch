import { StudentApplicationStatusEnum } from "@/client";
import { Badge } from "@/components/ui/badge";
import {
  Clock,
  CheckCircle,
  XCircle,
  GraduationCap,
  Pause,
  Ban,
  LogOut,
} from "lucide-react";

interface StudentStatusBadgeProps {
  status: StudentApplicationStatusEnum;
}

export default function StudentStatusBadge({
  status,
}: StudentStatusBadgeProps) {
  const statusConfig = {
    pending: {
      label: "Pending",
      variant: "secondary" as const,
      icon: Clock,
      className: "bg-yellow-100 text-yellow-800 border-yellow-200",
    },
    rejected: {
      label: "Rejected",
      variant: "secondary" as const,
      icon: XCircle,
      className: "bg-red-100 text-red-800 border-red-200",
    },
    active: {
      label: "Active",
      variant: "secondary" as const,
      icon: CheckCircle,
      className: "bg-green-100 text-green-800 border-green-200",
    },
    inactive: {
      label: "Inactive",
      variant: "secondary" as const,
      icon: Pause,
      className: "bg-green-100 text-green-800 border-green-200",
    },
    graduated: {
      label: "Graduated",
      variant: "secondary" as const,
      icon: GraduationCap,
      className: "bg-blue-100 text-blue-800 border-blue-200",
    },
    suspended: {
      label: "Suspended",
      variant: "secondary" as const,
      icon: Ban,
      className: "bg-purple-100 text-purple-800 border-purple-200",
    },
    withdrawn: {
      label: "Withdrawn",
      variant: "secondary" as const,
      icon: LogOut,
      className: "bg-purple-100 text-purple-800 border-purple-200",
    },
  };

  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <Badge variant={config.variant} className={config.className}>
      <Icon className="h-3 w-3 mr-1" />
      {config.label}
    </Badge>
  );
}
