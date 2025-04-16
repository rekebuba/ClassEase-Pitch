import { ErrorPage } from "@/components/ui/error-page"
import { Clock } from "lucide-react"

export default function ServiceUnavailablePage() {
    return (
        <ErrorPage
            statusCode={503}
            title="Service Unavailable"
            description="Our service is currently unavailable due to maintenance or high traffic. Please try again later."
            actions={{
                primary: {
                    label: "Check Status",
                    href: "/status",
                    icon: <Clock className="mr-2 h-4 w-4" />,
                },
                secondary: {
                    label: "Try Again",
                    onClick: () => window.location.reload(),
                },
            }}
        />
    )
}
