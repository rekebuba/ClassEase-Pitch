import { createFileRoute } from "@tanstack/react-router";
import { CheckCircle2, Clock3, Download, Search, ShieldAlert, SlidersHorizontal, XCircle } from "lucide-react";

import { ActionFooter } from "@/components/setting/settings-actions";
import { SettingCard, SettingsPage, SettingsSection } from "@/components/setting/settings-section";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Pagination, PaginationContent, PaginationEllipsis, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "@/components/ui/pagination";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/settings/audit-logs/")({
  component: AuditLogsSettingsPage,
});

const activities = [
  { user: "Miriam Otieno", action: "Updated grading policy", module: "Grading", date: "06 Aug 2026, 09:42", status: "Success" },
  { user: "Daniel Kariuki", action: "Viewed student profile", module: "Students", date: "06 Aug 2026, 09:18", status: "Success" },
  { user: "Aisha Ndlovu", action: "Attempted restricted export", module: "Finance", date: "06 Aug 2026, 08:55", status: "Blocked" },
  { user: "System", action: "Session expired", module: "Security", date: "05 Aug 2026, 18:02", status: "Warning" },
  { user: "Grace Wanjiku", action: "Changed notification template", module: "Notifications", date: "05 Aug 2026, 15:27", status: "Success" },
  { user: "Peter Mensah", action: "Failed login challenge", module: "Authentication", date: "05 Aug 2026, 07:31", status: "Failed" },
];

function statusBadge(status: string) {
  if (status === "Success") {
    return (
      <Badge className="bg-emerald-600 hover:bg-emerald-600">
        <CheckCircle2 className="mr-1 size-3" />
        Success
      </Badge>
    );
  }
  if (status === "Blocked") {
    return (
      <Badge className="bg-amber-500 text-amber-950 hover:bg-amber-500">
        <ShieldAlert className="mr-1 size-3" />
        Blocked
      </Badge>
    );
  }
  if (status === "Warning") {
    return (
      <Badge variant="secondary">
        <Clock3 className="mr-1 size-3" />
        Warning
      </Badge>
    );
  }
  return (
    <Badge variant="destructive">
      <XCircle className="mr-1 size-3" />
      Failed
    </Badge>
  );
}

function AuditLogsSettingsPage() {
  return (
    <SettingsPage title="Audit Logs" description="Monitor important school activity, security events, administrative changes, and access decisions.">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <SettingCard title="Events today" description="Tracked administrative and access events." badge="246">
          <p className="text-2xl font-semibold">246</p>
          <p className="text-xs text-emerald-600">+12% compared with yesterday</p>
        </SettingCard>
        <SettingCard title="Blocked actions" description="Denied access attempts and protected operations." badge="Review">
          <p className="text-2xl font-semibold">8</p>
          <p className="text-xs text-amber-600">3 require administrator review</p>
        </SettingCard>
        <SettingCard title="Failed logins" description="Unsuccessful authentication attempts." badge="Security">
          <p className="text-2xl font-semibold">14</p>
          <p className="text-xs text-muted-foreground">Across 6 accounts</p>
        </SettingCard>
        <SettingCard title="Retention" description="Audit history retained for compliance." badge="Policy">
          <p className="text-2xl font-semibold">365 days</p>
          <p className="text-xs text-muted-foreground">Export available after backend wiring</p>
        </SettingCard>
      </div>

      <SettingsSection title="Filters" description="Search and filter controls are static placeholders for future audit API integration.">
        <div className="grid gap-3 lg:grid-cols-[1.4fr_1fr_1fr_1fr_auto]">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
            <Input className="rounded-xl pl-9" placeholder="Search user, action, module, or IP address" defaultValue="" />
          </div>
          <Select defaultValue="All users">
            <SelectTrigger className="w-full rounded-xl"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="All users">All users</SelectItem>
              <SelectItem value="Staff">Staff</SelectItem>
              <SelectItem value="System">System</SelectItem>
              <SelectItem value="Guardians">Guardians</SelectItem>
            </SelectContent>
          </Select>
          <Select defaultValue="All actions">
            <SelectTrigger className="w-full rounded-xl"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="All actions">All actions</SelectItem>
              <SelectItem value="Create">Create</SelectItem>
              <SelectItem value="Update">Update</SelectItem>
              <SelectItem value="Export">Export</SelectItem>
              <SelectItem value="Login">Login</SelectItem>
            </SelectContent>
          </Select>
          <Select defaultValue="Last 7 days">
            <SelectTrigger className="w-full rounded-xl"><SelectValue /></SelectTrigger>
            <SelectContent>
              <SelectItem value="Last 24 hours">Last 24 hours</SelectItem>
              <SelectItem value="Last 7 days">Last 7 days</SelectItem>
              <SelectItem value="Last 30 days">Last 30 days</SelectItem>
              <SelectItem value="Custom range">Custom range</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" disabled>
            <SlidersHorizontal className="size-4" />
            Advanced
          </Button>
        </div>
      </SettingsSection>

      <SettingsSection
        title="Recent Activity"
        description="Representative audit trail with static pagination and status badges."
        action={(
          <Button variant="outline" disabled>
            <Download className="size-4" />
            Export CSV
          </Button>
        )}
      >
        <div className="overflow-hidden rounded-2xl border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>User</TableHead>
                <TableHead>Action</TableHead>
                <TableHead>Module</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {activities.map(activity => (
                <TableRow key={`${activity.user}-${activity.date}`} className="hover:bg-muted/40">
                  <TableCell className="font-medium">{activity.user}</TableCell>
                  <TableCell>{activity.action}</TableCell>
                  <TableCell><Badge variant="outline">{activity.module}</Badge></TableCell>
                  <TableCell className="text-muted-foreground">{activity.date}</TableCell>
                  <TableCell>{statusBadge(activity.status)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-muted-foreground">Showing 1-6 of 246 events</p>
          <Pagination className="mx-0 w-fit justify-start sm:justify-end">
            <PaginationContent>
              <PaginationItem><PaginationPrevious href="#" /></PaginationItem>
              <PaginationItem><PaginationLink href="#" isActive>1</PaginationLink></PaginationItem>
              <PaginationItem><PaginationLink href="#">2</PaginationLink></PaginationItem>
              <PaginationItem><PaginationLink href="#">3</PaginationLink></PaginationItem>
              <PaginationItem><PaginationEllipsis /></PaginationItem>
              <PaginationItem><PaginationNext href="#" /></PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      </SettingsSection>

      <div className="rounded-2xl border bg-background p-5 shadow-sm">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-medium">Empty state preview</p>
            <p className="mt-1 text-sm text-muted-foreground">When filters return no audit entries, show a clear empty result and a reset filters action.</p>
          </div>
          <Button variant="outline" disabled>Reset filters</Button>
        </div>
      </div>

      <ActionFooter disabled saveLabel="Save audit policy" />
    </SettingsPage>
  );
}
