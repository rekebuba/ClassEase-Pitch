"use client"

import type React from "react"

import { Button } from "@/components/ui/button"
import { ArrowLeft, Home } from "lucide-react"
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

interface ErrorPageProps {
    statusCode: number
    title: string
    description: string
    illustration?: string
    actions?: {
        primary?: {
            label: string
            href?: string
            onClick?: () => void
            icon?: React.ReactNode
        }
        secondary?: {
            label: string
            href?: string
            onClick?: () => void
            icon?: React.ReactNode
        }
    }
}

export function ErrorPage({
    statusCode,
    title,
    description,
    illustration = "/illustrations/error.svg",
    actions,
}: ErrorPageProps) {
    const navigate = useNavigate()

    const handleRefresh = () => {
        window.location.reload()
    }

    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4 text-center">
            <div className="mx-auto max-w-md">
                <div className="mb-8 text-center">
                    <img
                        src={illustration || "/placeholder.svg"}
                        alt={`${statusCode} error illustration`}
                        className="mx-auto h-48 w-auto"
                    />
                </div>

                <h1 className="mb-2 text-9xl font-bold text-primary">{statusCode}</h1>
                <h2 className="mb-4 text-2xl font-semibold text-foreground">{title}</h2>
                <p className="mb-8 text-muted-foreground">{description}</p>

                <div className="flex flex-col space-y-3 sm:flex-row sm:space-x-3 sm:space-y-0">
                    {actions?.primary ? (
                        <Button asChild size="lg">
                            <Link to={actions.primary.href || "/"}>
                                {actions.primary.icon || <Home className="mr-2 h-4 w-4" />}
                                {actions.primary.label}
                            </Link>
                        </Button>
                    ) : (
                        <Button asChild size="lg">
                            <Link to="/">
                                <Home className="mr-2 h-4 w-4" />
                                Back to Home
                            </Link>
                        </Button>
                    )}

                    {actions?.secondary ? (
                        <Button variant="outline" size="lg" onClick={actions.secondary.onClick} asChild={!!actions.secondary.href}>
                            {actions.secondary.href ? (
                                <Link to={actions.secondary.href}>
                                    {actions.secondary.icon || <ArrowLeft className="mr-2 h-4 w-4" />}
                                    {actions.secondary.label}
                                </Link>
                            ) : (
                                <>
                                    {actions.secondary.icon || <ArrowLeft className="mr-2 h-4 w-4" />}
                                    {actions.secondary.label}
                                </>
                            )}
                        </Button>
                    ) : (
                        <Button variant="outline" size="lg" onClick={() => navigate(-1)}>
                            <ArrowLeft className="mr-2 h-4 w-4" />
                            Go Back
                        </Button>
                    )}
                </div>
            </div>
        </div>
    )
}
