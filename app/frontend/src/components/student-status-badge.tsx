import { Badge } from "@/components/ui/badge";
import {
  Clock,
  Eye,
  FileText,
  CheckCircle,
  XCircle,
  GraduationCap,
} from "lucide-react";

interface StudentStatusBadgeProps {
  status:
    | "pending"
    | "under-review"
    | "documents-required"
    | "approved"
    | "rejected"
    | "enrolled";
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
    "under-review": {
      label: "Under Review",
      variant: "secondary" as const,
      icon: Eye,
      className: "bg-blue-100 text-blue-800 border-blue-200",
    },
    "documents-required": {
      label: "Documents Required",
      variant: "secondary" as const,
      icon: FileText,
      className: "bg-orange-100 text-orange-800 border-orange-200",
    },
    approved: {
      label: "Approved",
      variant: "secondary" as const,
      icon: CheckCircle,
      className: "bg-green-100 text-green-800 border-green-200",
    },
    rejected: {
      label: "Rejected",
      variant: "secondary" as const,
      icon: XCircle,
      className: "bg-red-100 text-red-800 border-red-200",
    },
    enrolled: {
      label: "Enrolled",
      variant: "secondary" as const,
      icon: GraduationCap,
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
