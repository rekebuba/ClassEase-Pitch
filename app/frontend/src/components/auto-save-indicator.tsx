"use client"

import { useEffect, useState } from "react"
import { Badge } from "@/components/ui/badge"
import { Check, Cloud, CloudOff } from "lucide-react"

interface AutoSaveIndicatorProps {
    lastSaved?: Date
    isOnline?: boolean
}

export default function AutoSaveIndicator({ lastSaved, isOnline = true }: AutoSaveIndicatorProps) {
    const [showSaved, setShowSaved] = useState(false)

    useEffect(() => {
        if (lastSaved) {
            setShowSaved(true)
            const timer = setTimeout(() => setShowSaved(false), 3000)
            return () => clearTimeout(timer)
        }
    }, [lastSaved])

    const formatTime = (date: Date) => {
        return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    }

    if (!isOnline) {
        return (
            <Badge variant="secondary" className="bg-orange-100 text-orange-800 border-orange-200">
                <CloudOff className="h-3 w-3 mr-1" />
                Offline - Saving locally
            </Badge>
        )
    }

    if (showSaved && lastSaved) {
        return (
            <Badge variant="secondary" className="bg-green-100 text-green-800 border-green-200">
                <Check className="h-3 w-3 mr-1" />
                Saved at {formatTime(lastSaved)}
            </Badge>
        )
    }

    return (
        <Badge variant="secondary" className="bg-gray-100 text-gray-600 border-gray-200">
            <Cloud className="h-3 w-3 mr-1" />
            Auto-save enabled
        </Badge>
    )
}
