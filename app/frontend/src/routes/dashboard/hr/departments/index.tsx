import { createFileRoute } from "@tanstack/react-router";
import { Building2 } from "lucide-react";

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HRPageHeader, HRStatCard, SectionCard, StatusBadge, TableActions } from "@/features/hr/components/common";
import { departments } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/departments/")({
  component: HRDepartmentsPage,
});

function HRDepartmentsPage() {
  return (
    <div className="space-y-6">
      <HRPageHeader title="Departments" description="Department ownership, staffing levels, vacancies, and HR activity." />
      <div className="grid gap-4 md:grid-cols-3">
        <HRStatCard title="Departments" value="8" detail="All within selected school" icon={Building2} />
        <HRStatCard title="Open Positions" value="6" detail="Mostly teaching and IT" icon={Building2} />
        <HRStatCard title="Largest Department" value="Teaching" detail="112 employees" icon={Building2} />
      </div>
      <SectionCard title="Department Directory">
        <div className="overflow-hidden rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Department</TableHead>
                <TableHead>Code</TableHead>
                <TableHead>Manager</TableHead>
                <TableHead>Employees</TableHead>
                <TableHead>Open Positions</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="w-12">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {departments.map(department => (
                <TableRow key={department.id}>
                  <TableCell className="font-medium">{department.name}</TableCell>
                  <TableCell className="font-mono text-xs">{department.code}</TableCell>
                  <TableCell>{department.manager}</TableCell>
                  <TableCell>{department.employees}</TableCell>
                  <TableCell>{department.openPositions}</TableCell>
                  <TableCell><StatusBadge value={department.status} /></TableCell>
                  <TableCell><TableActions viewTo="/dashboard/hr/departments/$departmentId" params={{ departmentId: department.id }} /></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </SectionCard>
    </div>
  );
}
