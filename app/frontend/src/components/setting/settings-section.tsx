import { AlertTriangle, CheckCircle2, HelpCircle, Upload } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

type SettingsPageProps = {
  title: string;
  description: string;
  children: ReactNode;
};

export function SettingsPage({ title, description, children }: SettingsPageProps) {
  return (
    <div className="space-y-6">
      <div className="rounded-2xl border bg-background p-6 shadow-sm">
        <h2 className="text-xl font-semibold tracking-tight">{title}</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-muted-foreground">{description}</p>
      </div>
      {children}
    </div>
  );
}

type SettingsSectionProps = {
  title: string;
  description?: string;
  children: ReactNode;
  action?: ReactNode;
};

export function SettingsSection({ title, description, children, action }: SettingsSectionProps) {
  return (
    <section className="rounded-2xl border bg-background shadow-sm">
      <div className="flex flex-col gap-3 p-5 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h3 className="text-base font-semibold">{title}</h3>
          {description ? <p className="mt-1 max-w-2xl text-sm leading-6 text-muted-foreground">{description}</p> : null}
        </div>
        {action}
      </div>
      <Separator />
      <div className="p-5">{children}</div>
    </section>
  );
}

type FieldProps = {
  label: string;
  value?: string;
  placeholder?: string;
  helper?: string;
  error?: string;
  disabled?: boolean;
  counter?: string;
  type?: string;
};

export function SettingInput({ label, value, placeholder, helper, error, disabled, counter, type = "text" }: FieldProps) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-3">
        <Label>{label}</Label>
        {counter ? <span className="text-xs text-muted-foreground">{counter}</span> : null}
      </div>
      <Input type={type} defaultValue={value} placeholder={placeholder} disabled={disabled} aria-invalid={Boolean(error)} className="rounded-xl" />
      {helper ? <p className="text-xs leading-5 text-muted-foreground">{helper}</p> : null}
      {error ? <p className="text-xs leading-5 text-destructive">{error}</p> : null}
    </div>
  );
}

type SettingSelectProps = {
  label: string;
  value: string;
  options: string[];
  helper?: string;
  disabled?: boolean;
};

export function SettingSelect({ label, value, options, helper, disabled }: SettingSelectProps) {
  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <Select defaultValue={value} disabled={disabled}>
        <SelectTrigger className="w-full rounded-xl">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {options.map(option => <SelectItem key={option} value={option}>{option}</SelectItem>)}
        </SelectContent>
      </Select>
      {helper ? <p className="text-xs leading-5 text-muted-foreground">{helper}</p> : null}
    </div>
  );
}

type SettingSwitchProps = {
  label: string;
  description: string;
  checked?: boolean;
  disabled?: boolean;
  badge?: string;
};

export function SettingSwitch({ label, description, checked = false, disabled, badge }: SettingSwitchProps) {
  return (
    <div className="flex items-start justify-between gap-4 rounded-2xl border bg-muted/20 p-4">
      <div className="space-y-1">
        <div className="flex flex-wrap items-center gap-2">
          <p className="text-sm font-medium">{label}</p>
          {badge ? <Badge variant="secondary">{badge}</Badge> : null}
        </div>
        <p className="text-sm leading-6 text-muted-foreground">{description}</p>
      </div>
      <Switch defaultChecked={checked} disabled={disabled} className="mt-1" />
    </div>
  );
}

type SettingCardProps = {
  icon?: LucideIcon;
  title: string;
  description: string;
  children?: ReactNode;
  badge?: string;
};

export function SettingCard({ icon: Icon, title, description, children, badge }: SettingCardProps) {
  return (
    <Card className="rounded-2xl shadow-sm transition-colors hover:bg-muted/20">
      <CardContent className="space-y-4 px-5">
        <div className="flex items-start gap-3">
          {Icon ? <div className="flex size-9 shrink-0 items-center justify-center rounded-xl border bg-background"><Icon className="size-4" /></div> : null}
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h4 className="text-sm font-semibold">{title}</h4>
              {badge ? <Badge variant="outline">{badge}</Badge> : null}
            </div>
            <p className="mt-1 text-sm leading-6 text-muted-foreground">{description}</p>
          </div>
        </div>
        {children}
      </CardContent>
    </Card>
  );
}

type UploadCardProps = {
  title: string;
  description: string;
  value?: string;
  aspect?: string;
};

export function UploadCard({ title, description, value, aspect = "aspect-[4/3]" }: UploadCardProps) {
  return (
    <div className="rounded-2xl border bg-muted/20 p-4">
      <div className={cn("flex w-full flex-col items-center justify-center rounded-xl border border-dashed bg-background p-6 text-center", aspect)}>
        <Upload className="size-7 text-muted-foreground" />
        <p className="mt-3 text-sm font-medium">{title}</p>
        <p className="mt-1 max-w-xs text-xs leading-5 text-muted-foreground">{description}</p>
        <Button variant="outline" size="sm" className="mt-4" disabled>Upload disabled</Button>
      </div>
      {value ? <p className="mt-3 text-xs text-muted-foreground">{value}</p> : null}
    </div>
  );
}

type ColorSwatchProps = {
  label: string;
  value: string;
  className: string;
};

export function ColorSwatch({ label, value, className }: ColorSwatchProps) {
  return (
    <div className="rounded-2xl border bg-muted/20 p-4">
      <div className={cn("h-20 rounded-xl border shadow-inner", className)} />
      <div className="mt-3 flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-medium">{label}</p>
          <p className="text-xs text-muted-foreground">{value}</p>
        </div>
        <Input defaultValue={value} className="h-8 w-28 rounded-lg text-xs" />
      </div>
    </div>
  );
}

export function DangerZone() {
  return (
    <div className="rounded-2xl border border-destructive/30 bg-destructive/5 p-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="flex items-center gap-2 text-destructive">
            <AlertTriangle className="size-4" />
            <h4 className="font-semibold">Delete school workspace</h4>
          </div>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted-foreground">
            Permanently remove school profile, branding, settings, and connected records after backend confirmation. This preview keeps the action disabled.
          </p>
        </div>
        <Button variant="destructive" disabled>Delete school</Button>
      </div>
    </div>
  );
}

export function StaticAlerts() {
  return (
    <div className="grid gap-3 md:grid-cols-3">
      <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-950 dark:border-emerald-900/60 dark:bg-emerald-950/20 dark:text-emerald-100">
        <CheckCircle2 className="size-4" />
        <p className="mt-2 text-sm font-medium">Saved preview</p>
        <p className="mt-1 text-xs leading-5 opacity-80">Example success state for form submissions.</p>
      </div>
      <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-amber-950 dark:border-amber-900/60 dark:bg-amber-950/20 dark:text-amber-100">
        <AlertTriangle className="size-4" />
        <p className="mt-2 text-sm font-medium">Policy warning</p>
        <p className="mt-1 text-xs leading-5 opacity-80">Example warning state for risky configuration changes.</p>
      </div>
      <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-red-950 dark:border-red-900/60 dark:bg-red-950/20 dark:text-red-100">
        <AlertTriangle className="size-4" />
        <p className="mt-2 text-sm font-medium">Danger state</p>
        <p className="mt-1 text-xs leading-5 opacity-80">Example destructive action confirmation state.</p>
      </div>
    </div>
  );
}

export function LoadingPreview() {
  return (
    <div className="rounded-2xl border bg-muted/20 p-4">
      <div className="flex items-center gap-3">
        <Skeleton className="size-10 rounded-full" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-4 w-48" />
          <Skeleton className="h-3 w-72 max-w-full" />
        </div>
      </div>
    </div>
  );
}

export function FieldHelp({ children }: { children: ReactNode }) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Button variant="ghost" size="icon-sm" className="size-7">
            <HelpCircle className="size-4" />
            <span className="sr-only">Help</span>
          </Button>
        </TooltipTrigger>
        <TooltipContent sideOffset={6}>{children}</TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
