import {
  Ban,
  CheckCircle,
  Clock,
  GraduationCap,
  LogOut,
  Pause,
  XCircle,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";

import type { StudentApplicationStatusEnum } from "@/client";

type StudentApplicationStatusBadgeProps = {
  status: StudentApplicationStatusEnum;
};

type StatusConfig = {
  [key in StudentApplicationStatusEnum]: {
    label: string;
    variant: "secondary";
    icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
    className: string;
  };
};

export default function StudentApplicationStatusBadge({
  status,
}: StudentApplicationStatusBadgeProps) {
  const statusConfig: StatusConfig = {
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
