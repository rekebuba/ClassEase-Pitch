import { createFileRoute, notFound } from "@tanstack/react-router";

import { EmployeeTable, HRPageHeader, InfoGrid, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { employees, jobPostings, positions } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/positions/$positionId/")({
  component: HRPositionDetailPage,
  loader: ({ params }) => {
    const position = positions.find(item => item.id === params.positionId);
    if (!position) {
      throw notFound();
    }
    return { position };
  },
});

function HRPositionDetailPage() {
  const { position } = Route.useLoaderData();
  const currentEmployees = employees.filter(employee => employee.position === position.title);
  const relatedPostings = jobPostings.filter(job => job.position === position.title);

  return (
    <div className="space-y-6">
      <HRPageHeader title={position.title} description={position.description} />
      <div className="grid gap-4 lg:grid-cols-2">
        <SectionCard title="Position Information">
          <InfoGrid items={[
            { label: "Code", value: position.code },
            { label: "Department", value: position.department },
            { label: "Employment type", value: position.type },
            { label: "Level", value: position.level },
            { label: "Employees", value: position.employees },
            { label: "Openings", value: position.openings },
            { label: "Status", value: <StatusBadge value={position.status} /> },
          ]}
          />
        </SectionCard>
        <SectionCard title="Responsibilities & Requirements">
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <h3 className="font-medium">Responsibilities</h3>
              <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
                {position.responsibilities.map(item => <li key={item}>{item}</li>)}
              </ul>
            </div>
            <div>
              <h3 className="font-medium">Requirements</h3>
              <ul className="mt-2 space-y-2 text-sm text-muted-foreground">
                {position.requirements.map(item => <li key={item}>{item}</li>)}
              </ul>
            </div>
          </div>
        </SectionCard>
      </div>
      <SectionCard title="Current Employees">
        <EmployeeTable rows={currentEmployees} />
      </SectionCard>
      <SectionCard title="Related Job Postings">
        <div className="space-y-3">
          {relatedPostings.map(job => (
            <div key={job.id} className="flex items-center justify-between rounded-md border p-3">
              <span>{job.position} · {job.applications} applications</span>
              <StatusBadge value={job.status} />
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
