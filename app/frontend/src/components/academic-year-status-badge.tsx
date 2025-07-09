
import { Badge } from "@/components/ui/badge"
import type { AcademicYear } from "@/lib/academic-year"

interface AcademicYearStatusBadgeProps {
    status: AcademicYear["status"]
    className?: string
}

export default function AcademicYearStatusBadge({ status, className }: AcademicYearStatusBadgeProps) {
    const getStatusConfig = (status: AcademicYear["status"]) => {
        switch (status) {
            case "active":
                return {
                    label: "Active",
                    className: "bg-green-100 text-green-800 border-green-200",
                }
            case "draft":
                return {
                    label: "Draft",
                    className: "bg-yellow-100 text-yellow-800 border-yellow-200",
                }
            case "completed":
                return {
                    label: "Completed",
                    className: "bg-gray-100 text-gray-800 border-gray-200",
                }
            default:
                return {
                    label: "Unknown",
                    className: "bg-gray-100 text-gray-800 border-gray-200",
                }
        }
    }

    const config = getStatusConfig(status)

    return (
        <Badge variant="outline" className={`${config.className} ${className}`}>
            {config.label}
        </Badge>
    )
}
