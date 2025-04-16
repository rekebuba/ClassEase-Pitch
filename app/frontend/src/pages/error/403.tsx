import { ErrorPage } from "@/components/ui/error-page"
import { ShieldAlert } from "lucide-react"

export default function ForbiddenPage() {
    return (
        <ErrorPage
            statusCode={403}
            title="Access Forbidden"
            description="You don't have permission to access this page. If you believe this is an error, please contact your administrator."
            actions={{
                primary: {
                    label: "Contact Support",
                    href: "/contact",
                    icon: <ShieldAlert className="mr-2 h-4 w-4" />,
                },
                secondary: {
                    label: "Back to Home",
                    href: "/",
                },
            }}
        />
    )
}
