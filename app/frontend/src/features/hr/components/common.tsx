import { Link } from "@tanstack/react-router";
import { ArrowDownUp, MoreHorizontal, Search } from "lucide-react";
import { useMemo, useState } from "react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";

import type { Employee, EmployeeStatus, EmploymentType } from "@/features/hr/data/mock";
import type { LinkOptions } from "@tanstack/react-router";
import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";

type BadgeTone = "default" | "green" | "amber" | "red" | "blue" | "slate";

const toneClasses: Record<BadgeTone, string> = {
  default: "",
  green: "border-emerald-200 bg-emerald-50 text-emerald-700",
  amber: "border-amber-200 bg-amber-50 text-amber-700",
  red: "border-red-200 bg-red-50 text-red-700",
  blue: "border-sky-200 bg-sky-50 text-sky-700",
  slate: "border-slate-200 bg-slate-50 text-slate-700",
};

export function StatusBadge({ value }: { value: string }) {
  const tone: BadgeTone = value.includes("Active") || value.includes("Valid") || value.includes("Approved") || value.includes("Published") || value.includes("Completed") || value.includes("Hired")
    ? "green"
    : value.includes("Pending") || value.includes("Probation") || value.includes("Interview") || value.includes("Shortlisted") || value.includes("Expiring") || value.includes("Hiring")
      ? "amber"
      : value.includes("Rejected") || value.includes("Expired") || value.includes("Overdue") || value.includes("Inactive")
        ? "red"
        : value.includes("Screening") || value.includes("New") || value.includes("Offer") || value.includes("Assessment")
          ? "blue"
          : "slate";

  return (
    <Badge variant="outline" className={cn("whitespace-nowrap", toneClasses[tone])}>
      {value}
    </Badge>
  );
}

export function HRPageHeader({
  title,
  description,
  actions,
}: {
  title: string;
  description: string;
  actions?: ReactNode;
}) {
  return (
    <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
        <p className="max-w-3xl text-sm text-muted-foreground">{description}</p>
      </div>
      {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
    </div>
  );
}

export function HRStatCard({
  title,
  value,
  detail,
  icon: Icon,
}: {
  title: string;
  value: string;
  detail: string;
  icon: LucideIcon;
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground">{detail}</p>
      </CardContent>
    </Card>
  );
}

export function EmployeeIdentity({ employee, subtitle }: { employee: Pick<Employee, "name" | "initials" | "employeeId">; subtitle?: string }) {
  return (
    <div className="flex min-w-[14rem] items-center gap-3">
      <Avatar className="h-9 w-9 rounded-lg">
        <AvatarFallback className="rounded-lg bg-sky-100 text-sky-700">{employee.initials}</AvatarFallback>
      </Avatar>
      <div>
        <div className="font-medium">{employee.name}</div>
        <div className="text-xs text-muted-foreground">{subtitle ?? employee.employeeId}</div>
      </div>
    </div>
  );
}

export function MockActionDialog({ label, title, description, children }: { label: string; title: string; description: string; children?: ReactNode }) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button size="sm">{label}</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <div className="grid gap-3">
          {children ?? (
            <>
              <Input placeholder="Reference number" />
              <Input placeholder="Notes" />
            </>
          )}
        </div>
        <DialogFooter showCloseButton>
          <Button type="button">Save mock record</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export function TableActions({ viewTo, params }: { viewTo?: LinkOptions["to"]; params?: LinkOptions["params"] }) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <MoreHorizontal className="h-4 w-4" />
          <span className="sr-only">Open actions</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {viewTo && (
          <DropdownMenuItem asChild>
            <Link to={viewTo} params={params}>View details</Link>
          </DropdownMenuItem>
        )}
        <DropdownMenuItem>Edit record</DropdownMenuItem>
        <DropdownMenuItem>Download summary</DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export function FilterBar({
  search,
  onSearch,
  filters,
}: {
  search: string;
  onSearch: (value: string) => void;
  filters: Array<{ label: string; value: string; options: string[]; onChange: (value: string) => void }>;
}) {
  return (
    <div className="flex flex-col gap-3 md:flex-row md:items-center">
      <div className="relative md:max-w-sm md:flex-1">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input value={search} onChange={event => onSearch(event.target.value)} placeholder="Search records..." className="pl-9" />
      </div>
      <div className="flex flex-wrap gap-2">
        {filters.map(filter => (
          <Select key={filter.label} value={filter.value} onValueChange={filter.onChange}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder={filter.label} />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">{filter.label}</SelectItem>
              {filter.options.map(option => (
                <SelectItem key={option} value={option}>{option}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        ))}
      </div>
    </div>
  );
}

export function useEmployeeFilters(source: Employee[]) {
  const [search, setSearch] = useState("");
  const [department, setDepartment] = useState("all");
  const [position, setPosition] = useState("all");
  const [type, setType] = useState("all");
  const [status, setStatus] = useState("all");
  const [sortKey, setSortKey] = useState<"name" | "joinDate">("name");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase();
    return source
      .filter(employee => !term || [employee.name, employee.employeeId, employee.position, employee.department].some(value => value.toLowerCase().includes(term)))
      .filter(employee => department === "all" || employee.department === department)
      .filter(employee => position === "all" || employee.position === position)
      .filter(employee => type === "all" || employee.type === type)
      .filter(employee => status === "all" || employee.status === status)
      .sort((a, b) => sortKey === "name" ? a.name.localeCompare(b.name) : b.joinDate.localeCompare(a.joinDate));
  }, [department, position, search, sortKey, source, status, type]);

  const pageSize = 6;
  const pageCount = Math.max(1, Math.ceil(filtered.length / pageSize));
  const safePage = Math.min(page, pageCount);
  const paged = filtered.slice((safePage - 1) * pageSize, safePage * pageSize);

  return {
    search,
    setSearch: (value: string) => {
      setSearch(value);
      setPage(1);
    },
    department,
    setDepartment,
    position,
    setPosition,
    type,
    setType: (value: string) => setType(value as EmploymentType | "all"),
    status,
    setStatus: (value: string) => setStatus(value as EmployeeStatus | "all"),
    sortKey,
    setSortKey,
    page: safePage,
    setPage,
    pageCount,
    paged,
    total: filtered.length,
  };
}

export function EmployeeTable({ rows }: { rows: Employee[] }) {
  return (
    <div className="overflow-hidden rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Employee</TableHead>
            <TableHead>Employee ID</TableHead>
            <TableHead>Position</TableHead>
            <TableHead>Department</TableHead>
            <TableHead>Employment Type</TableHead>
            <TableHead>Join Date</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="w-12">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map(employee => (
            <TableRow key={employee.id}>
              <TableCell><EmployeeIdentity employee={employee} subtitle={employee.email} /></TableCell>
              <TableCell className="font-mono text-xs">{employee.employeeId}</TableCell>
              <TableCell>{employee.position}</TableCell>
              <TableCell>{employee.department}</TableCell>
              <TableCell><StatusBadge value={employee.type} /></TableCell>
              <TableCell>{employee.joinDate}</TableCell>
              <TableCell><StatusBadge value={employee.status} /></TableCell>
              <TableCell>
                <TableActions viewTo="/dashboard/hr/employees/$employeeId" params={{ employeeId: employee.id }} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

export function SimplePagination({ page, pageCount, onPageChange }: { page: number; pageCount: number; onPageChange: (page: number) => void }) {
  return (
    <div className="flex items-center justify-between gap-3 text-sm text-muted-foreground">
      <span>
        Page
        {" "}
        {page}
        {" "}
        of
        {" "}
        {pageCount}
      </span>
      <div className="flex gap-2">
        <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => onPageChange(page - 1)}>Previous</Button>
        <Button variant="outline" size="sm" disabled={page >= pageCount} onClick={() => onPageChange(page + 1)}>Next</Button>
      </div>
    </div>
  );
}

export function SortButton({ onClick, label }: { onClick: () => void; label: string }) {
  return (
    <Button variant="outline" size="sm" onClick={onClick}>
      <ArrowDownUp className="mr-2 h-4 w-4" />
      {label}
    </Button>
  );
}

export function MiniBar({ label, value, max, className }: { label: string; value: number; max: number; className?: string }) {
  const width = Math.max(8, Math.round((value / max) * 100));
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm">
        <span>{label}</span>
        <span className="font-medium">{value}</span>
      </div>
      <div className="h-2 rounded-full bg-muted">
        <div className={cn("h-2 rounded-full bg-sky-500", className)} style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}

export function InfoGrid({ items }: { items: Array<{ label: string; value?: ReactNode }> }) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {items.map(item => (
        <div key={item.label}>
          <p className="text-sm font-medium text-muted-foreground">{item.label}</p>
          <div className="mt-1 font-medium">{item.value ?? "N/A"}</div>
        </div>
      ))}
    </div>
  );
}

export function SectionCard({ title, description, children }: { title: string; description?: string; children: ReactNode }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}
