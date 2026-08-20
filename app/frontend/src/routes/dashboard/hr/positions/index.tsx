import { createFileRoute } from "@tanstack/react-router";
import { ClipboardCheck } from "lucide-react";

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HRPageHeader, HRStatCard, MockActionDialog, SectionCard, StatusBadge, TableActions } from "@/features/hr/components/common";
import { positions } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/positions/")({
  component: HRPositionsPage,
});

function HRPositionsPage() {
  return (
    <div className="space-y-6">
      <HRPageHeader
        title="Positions"
        description="Position catalog, staffing coverage, openings, and recruitment status."
        actions={<MockActionDialog label="Add Position" title="Add position" description="Mock position form for frontend planning." />}
      />
      <div className="grid gap-4 md:grid-cols-3">
        <HRStatCard title="Position Types" value="12" detail="Academic and operations roles" icon={ClipboardCheck} />
        <HRStatCard title="Currently Hiring" value="4" detail="Teaching and IT roles" icon={ClipboardCheck} />
        <HRStatCard title="Filled Roles" value="64" detail="From listed sample positions" icon={ClipboardCheck} />
      </div>
      <SectionCard title="Position Catalog">
        <div className="overflow-hidden rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Position</TableHead>
                <TableHead>Code</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Level</TableHead>
                <TableHead>Employees</TableHead>
                <TableHead>Openings</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="w-12">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {positions.map(position => (
                <TableRow key={position.id}>
                  <TableCell className="font-medium">{position.title}</TableCell>
                  <TableCell className="font-mono text-xs">{position.code}</TableCell>
                  <TableCell>{position.department}</TableCell>
                  <TableCell><StatusBadge value={position.type} /></TableCell>
                  <TableCell>{position.level}</TableCell>
                  <TableCell>{position.employees}</TableCell>
                  <TableCell>{position.openings}</TableCell>
                  <TableCell><StatusBadge value={position.status} /></TableCell>
                  <TableCell><TableActions viewTo="/dashboard/hr/positions/$positionId" params={{ positionId: position.id }} /></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </SectionCard>
    </div>
  );
}
