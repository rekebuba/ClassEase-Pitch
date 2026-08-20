import { createFileRoute, notFound } from "@tanstack/react-router";

import { HRPageHeader, InfoGrid, MiniBar, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { applications, jobPostings, pipeline } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/recruitment/jobs/$jobId/")({
  component: HRJobDetailPage,
  loader: ({ params }) => {
    const job = jobPostings.find(item => item.id === params.jobId);
    if (!job) {
      throw notFound();
    }
    return { job };
  },
});

function HRJobDetailPage() {
  const { job } = Route.useLoaderData();
  const candidates = applications.filter(application => application.position === job.position);

  return (
    <div className="space-y-6">
      <HRPageHeader title={job.position} description={job.description} />
      <div className="grid gap-4 lg:grid-cols-2">
        <SectionCard title="Position Information">
          <InfoGrid items={[
            { label: "Department", value: job.department },
            { label: "Employment type", value: job.type },
            { label: "Openings", value: job.openings },
            { label: "Application deadline", value: job.deadline },
            { label: "Status", value: <StatusBadge value={job.status} /> },
          ]}
          />
        </SectionCard>
        <SectionCard title="Application Statistics">
          <div className="space-y-4">
            {pipeline.map(stage => <MiniBar key={stage.stage} label={stage.stage} value={Math.min(stage.count, job.applications)} max={job.applications} />)}
          </div>
        </SectionCard>
      </div>
      <SectionCard title="Candidates">
        <div className="space-y-3">
          {candidates.map(candidate => (
            <div key={candidate.id} className="flex items-center justify-between rounded-md border p-3">
              <span>{candidate.candidate} · {candidate.experience}</span>
              <StatusBadge value={candidate.status} />
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
