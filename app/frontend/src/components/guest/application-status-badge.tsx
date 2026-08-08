import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

import type { GuestApplicationStatus } from "@/lib/guest-data";

const statusStyles: Record<GuestApplicationStatus, string> = {
  Pending: "border-amber-200 bg-amber-50 text-amber-700",
  "Under Review": "border-blue-200 bg-blue-50 text-blue-700",
  Accepted: "border-emerald-200 bg-emerald-50 text-emerald-700",
  Rejected: "border-rose-200 bg-rose-50 text-rose-700",
  Withdrawn: "border-slate-200 bg-slate-50 text-slate-700",
};

export function ApplicationStatusBadge({ status, className }: { status: GuestApplicationStatus; className?: string }) {
  return (
    <Badge variant="outline" className={cn(statusStyles[status], className)}>
      {status}
    </Badge>
  );
}
