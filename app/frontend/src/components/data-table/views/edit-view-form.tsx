"use client"

import type React from "react"

import { useEffect, useRef, useState } from "react"
import { ChevronLeftIcon } from "@radix-ui/react-icons"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"

import { DeleteViewForm } from "./delete-view-form"
import { LoaderIcon } from "lucide-react"
import { renameViewData, StudentsViews } from "@/lib/types"
import { renameView } from "@/api/adminApi"

interface EditViewFormProps {
  view: StudentsViews
  setIsEditViewFormOpen: React.Dispatch<React.SetStateAction<boolean>>
  refetchViews: () => void
  onDelete: (viewId: string) => void
}

export function EditViewForm({ view, setIsEditViewFormOpen, refetchViews, onDelete }: EditViewFormProps) {
  const nameInputRef = useRef<HTMLInputElement>(null)
  const [name, setName] = useState(view.name)
  const [pending, setPending] = useState(false)

  useEffect(() => {
    nameInputRef.current?.focus()
  }, [])

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (name.trim() === "") {
      toast.error("Name cannot be empty.")
      return
    }

    setPending(true)

    // Simulate API call
    setTimeout(async () => {
      const updatedView: renameViewData = { viewId: view.viewId, name: name }
      const result = await renameView(updatedView);
      setIsEditViewFormOpen(false)

      toast.error(result.message, {
        style: { color: "green" },
      });
      refetchViews()

      setPending(false)
    }, 500)
  }

  return (
    <div>
      <div className="flex items-center gap-1 px-1 py-1.5">
        <Button variant="ghost" size="icon" className="size-6" onClick={() => setIsEditViewFormOpen(false)}>
          <span className="sr-only">Close edit view form</span>
          <ChevronLeftIcon aria-hidden="true" className="size-4" />
        </Button>
        <span className="text-sm">Edit view</span>
      </div>

      <Separator />

      <form onSubmit={handleSubmit} className="flex flex-col gap-2 p-2">
        <Input
          ref={nameInputRef}
          type="text"
          name="name"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          autoComplete="off"
        />
        <Button disabled={pending} size="sm" type="submit">
          {pending ? <LoaderIcon aria-hidden="true" className="size-3.5 animate-spin" /> : "Save"}
        </Button>
      </form>

      <Separator />

      <DeleteViewForm viewId={view.viewId} setIsEditViewFormOpen={setIsEditViewFormOpen} onDelete={onDelete} />
    </div>
  )
}
