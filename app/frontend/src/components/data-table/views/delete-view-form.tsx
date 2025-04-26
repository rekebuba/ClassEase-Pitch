"use client"

import type React from "react"

import { useState } from "react"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { LoaderIcon } from "lucide-react"

interface DeleteViewFormProps {
  viewId: string
  setIsEditViewFormOpen: React.Dispatch<React.SetStateAction<boolean>>
  onDelete: (viewId: string) => void
}

export function DeleteViewForm({ viewId, setIsEditViewFormOpen, onDelete }: DeleteViewFormProps) {
  const [pending, setPending] = useState(false)

  const handleDelete = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setPending(true)

    // Simulate API call
    setTimeout(() => {
      onDelete(viewId)
      setIsEditViewFormOpen(false)
      toast.success("View deleted successfully.")
      setPending(false)
    }, 500)
  }

  return (
    <form onSubmit={handleDelete} className="p-2">
      <Button
        disabled={pending}
        variant="outline"
        size="sm"
        type="submit"
        className="w-full border-red-800/50 bg-destructive/5 text-red-600 hover:bg-destructive/10 hover:text-red-600 active:bg-destructive/10"
      >
        {pending ? <LoaderIcon aria-hidden="true" className="size-3.5 animate-spin" /> : "Delete"}
      </Button>
    </form>
  )
}
