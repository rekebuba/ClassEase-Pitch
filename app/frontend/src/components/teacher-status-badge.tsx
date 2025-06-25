import { Badge } from "@/components/ui/badge"
import { Clock, Eye, Calendar, CheckCircle, XCircle } from "lucide-react"

interface TeacherStatusBadgeProps {
    status: "pending" | "under-review" | "interview-scheduled" | "approved" | "rejected"
}

export default function TeacherStatusBadge({ status }: TeacherStatusBadgeProps) {
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
        "interview-scheduled": {
            label: "Interview Scheduled",
            variant: "secondary" as const,
            icon: Calendar,
            className: "bg-purple-100 text-purple-800 border-purple-200",
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
    }

    const config = statusConfig[status]
    const Icon = config.icon

    return (
        <Badge variant={config.variant} className={config.className}>
            <Icon className="h-3 w-3 mr-1" />
            {config.label}
        </Badge>
    )
}
