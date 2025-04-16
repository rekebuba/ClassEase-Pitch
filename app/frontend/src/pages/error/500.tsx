import { ErrorPage } from "@/components/ui/error-page"
import { ServerCrash } from "lucide-react"

export default function ServerErrorPage() {
    return (
        <ErrorPage
            statusCode={500}
            title="Server Error"
            description="We're experiencing some technical difficulties on our end. Our team has been notified and is working to resolve the issue."
            actions={{
                primary: {
                    label: "Try Again",
                    onClick: () => window.location.reload(),
                    icon: <ServerCrash className="mr-2 h-4 w-4" />,
                },
                secondary: {
                    label: "Back to Home",
                    href: "/",
                },
            }}
        />
    )
}
