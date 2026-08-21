import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";

import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HRPageHeader, SectionCard, StatusBadge, TableActions } from "@/features/hr/components/common";
import { applications } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/recruitment/applications/")({
  component: HRApplicationsPage,
});

function HRApplicationsPage() {
  const [search, setSearch] = useState("");
  const filtered = useMemo(() => {
    const term = search.toLowerCase();
    return applications.filter(application => [application.candidate, application.position, application.status].some(value => value.toLowerCase().includes(term)));
  }, [search]);

  return (
    <div className="space-y-6">
      <HRPageHeader title="Applications" description="Candidate records and pipeline status for active recruitment." />
      <SectionCard title="Candidate Pipeline">
        <Input value={search} onChange={event => setSearch(event.target.value)} placeholder="Search candidates..." className="mb-4 max-w-sm" />
        <div className="overflow-hidden rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Candidate</TableHead>
                <TableHead>Position</TableHead>
                <TableHead>Applied</TableHead>
                <TableHead>Experience</TableHead>
                <TableHead>Education</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Interview</TableHead>
                <TableHead>Recruiter</TableHead>
                <TableHead className="w-12">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map(application => (
                <TableRow key={application.id}>
                  <TableCell className="font-medium">{application.candidate}</TableCell>
                  <TableCell>{application.position}</TableCell>
                  <TableCell>{application.applicationDate}</TableCell>
                  <TableCell>{application.experience}</TableCell>
                  <TableCell>{application.education}</TableCell>
                  <TableCell><StatusBadge value={application.status} /></TableCell>
                  <TableCell>{application.interviewDate ?? "Not scheduled"}</TableCell>
                  <TableCell>{application.recruiter}</TableCell>
                  <TableCell><TableActions viewTo="/dashboard/hr/recruitment/applications/$applicationId" params={{ applicationId: application.id }} /></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </SectionCard>
    </div>
  );
}
