import { Info, Menu, ShieldCheck } from "lucide-react";
import { useState } from "react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

import { SettingsSidebar } from "./settings-sidebar";

export function SettingsHeader() {
  const [open, setOpen] = useState(false);

  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <div className="flex size-9 items-center justify-center rounded-2xl border bg-background shadow-sm">
              <ShieldCheck className="size-4" />
            </div>
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">School Settings</h1>
          </div>
          <p className="max-w-3xl text-sm leading-6 text-muted-foreground">
            Configure school identity, academic defaults, grading policy, permissions, communications, and operational audit visibility.
          </p>
        </div>

        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="outline" className="w-fit lg:hidden">
              <Menu className="size-4" />
              Settings menu
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[320px] p-0">
            <SheetHeader className="border-b px-5 py-4 text-left">
              <SheetTitle>School Settings</SheetTitle>
              <SheetDescription>Choose a settings area to edit.</SheetDescription>
            </SheetHeader>
            <div className="p-3">
              <SettingsSidebar onNavigate={() => setOpen(false)} />
            </div>
          </SheetContent>
        </Sheet>
      </div>

      <Alert className="rounded-2xl border-blue-200 bg-blue-50 text-blue-950 dark:border-blue-900/60 dark:bg-blue-950/20 dark:text-blue-100">
        <Info className="size-4" />
        <AlertTitle>Backend integration note</AlertTitle>
        <AlertDescription>
          This module is static UI only. Buttons, inputs, uploads, filters, and pagination are placeholders designed for later API integration.
        </AlertDescription>
      </Alert>
    </div>
  );
}
