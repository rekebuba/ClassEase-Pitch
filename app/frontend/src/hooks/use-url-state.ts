"use client"

import * as React from "react"

// A custom hook to replace React Router's useSearchParams
export function useUrlState() {
    const [searchParams, setSearchParamsState] = React.useState<URLSearchParams>(
        typeof window !== "undefined" ? new URLSearchParams(window.location.search) : new URLSearchParams(),
    )

    React.useEffect(() => {
        const handlePopState = () => {
            setSearchParamsState(new URLSearchParams(window.location.search))
        }

        window.addEventListener("popstate", handlePopState)

        return () => {
            window.removeEventListener("popstate", handlePopState)
        }
    }, [])

    // Update the URL when searchParams change
    React.useEffect(() => {
        if (typeof window === "undefined") return

        const newUrl = searchParams.toString()
            ? `${window.location.pathname}?${searchParams.toString()}`
            : window.location.pathname

        window.history.replaceState(null, "", newUrl)
    }, [searchParams])

    // Function to update search params
    const setSearchParams = React.useCallback(
        (newParams: URLSearchParams | ((prev: URLSearchParams) => URLSearchParams)) => {
            setSearchParamsState((prev) => {
                if (typeof newParams === "function") {
                    return newParams(prev)
                }
                return newParams
            })
        },
        [],
    )

    return [searchParams, setSearchParams] as const
}
