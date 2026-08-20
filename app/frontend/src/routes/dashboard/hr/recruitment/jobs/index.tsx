import { createFileRoute } from "@tanstack/react-router";

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HRPageHeader, MockActionDialog, SectionCard, StatusBadge, TableActions } from "@/features/hr/components/common";
import { jobPostings } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/recruitment/jobs/")({
  component: HRJobsPage,
});

function HRJobsPage() {
  return (
    <div className="space-y-6">
      <HRPageHeader title="Job Postings" description="Published, draft, closed, and archived school vacancies." actions={<MockActionDialog label="Create Job Posting" title="Create job posting" description="Mock recruitment posting form." />} />
      <SectionCard title="Posting List">
        <div className="overflow-hidden rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Position</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Employment Type</TableHead>
                <TableHead>Openings</TableHead>
                <TableHead>Applications</TableHead>
                <TableHead>Posted</TableHead>
                <TableHead>Deadline</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="w-12">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {jobPostings.map(job => (
                <TableRow key={job.id}>
                  <TableCell className="font-medium">{job.position}</TableCell>
                  <TableCell>{job.department}</TableCell>
                  <TableCell><StatusBadge value={job.type} /></TableCell>
                  <TableCell>{job.openings}</TableCell>
                  <TableCell>{job.applications}</TableCell>
                  <TableCell>{job.postedDate}</TableCell>
                  <TableCell>{job.deadline}</TableCell>
                  <TableCell><StatusBadge value={job.status} /></TableCell>
                  <TableCell><TableActions viewTo="/dashboard/hr/recruitment/jobs/$jobId" params={{ jobId: job.id }} /></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </SectionCard>
    </div>
  );
}
