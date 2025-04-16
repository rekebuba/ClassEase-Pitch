"use client"

import { Button } from "@/components/ui/button"
import { ArrowLeft, Home } from "lucide-react"
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import errorIllustration from "@/assets/illustrations/error.svg";

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
    illustration = errorIllustration,
    actions,
}: ErrorPageProps) {
    const router = useNavigate()

    const handleBack = () => {
        router(-1)
    }

    return (
        <div className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-background p-4 text-center">
            {/* Large background illustration */}
            <div
                className="absolute inset-0 z-0 flex items-center justify-center opacity-[0.07] overflow-hidden"
                aria-hidden="true"
            >
                <img
                    src={illustration}
                    alt={`${statusCode} error illustration`}
                    className="max-w-3xl w-full h-auto"
                    style={{
                        filter: "blur(1px)",
                    }}
                />
            </div>

            {/* Content overlay with subtle gradient */}
            <div className="relative z-10 mx-auto max-w-md">
                <div className="mb-6 flex justify-center">
                    <div className="relative">
                        <h1 className="text-9xl font-extrabold tracking-tighter text-primary">{statusCode}</h1>
                    </div>
                </div>

                <h2 className="mb-4 text-3xl font-bold text-foreground">{title}</h2>
                <p className="mb-8 text-lg text-muted-foreground">{description}</p>

                <div className="flex flex-col space-y-3 sm:flex-row sm:space-x-3 sm:space-y-0">
                    {actions?.primary ? (
                        <Button asChild size="lg" className="shadow-lg">
                            <Link to={actions.primary.href || "/"}>
                                {actions.primary.icon || <Home className="mr-2 h-5 w-5" />}
                                {actions.primary.label}
                            </Link>
                        </Button>
                    ) : (
                        <Button asChild size="lg" className="shadow-lg">
                            <Link to="/">
                                <Home className="mr-2 h-5 w-5" />
                                Back to Home
                            </Link>
                        </Button>
                    )}

                    {actions?.secondary ? (
                        <Button
                            variant="outline"
                            size="lg"
                            onClick={actions.secondary.onClick}
                            asChild={!!actions.secondary.href}
                            className="bg-background/80 backdrop-blur-sm"
                        >
                            {actions.secondary.href ? (
                                <Link to={actions.secondary.href}>
                                    {actions.secondary.icon || <ArrowLeft className="mr-2 h-5 w-5" />}
                                    {actions.secondary.label}
                                </Link>
                            ) : (
                                <>
                                    {actions.secondary.icon || <ArrowLeft className="mr-2 h-5 w-5" />}
                                    {actions.secondary.label}
                                </>
                            )}
                        </Button>
                    ) : (
                        <Button variant="outline" size="lg" onClick={handleBack} className="bg-background/80 backdrop-blur-sm">
                            <ArrowLeft className="mr-2 h-5 w-5" />
                            Go Back
                        </Button>
                    )}
                </div>
            </div>
        </div>
    )
}
