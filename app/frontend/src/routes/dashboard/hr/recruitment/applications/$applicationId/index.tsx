import { createFileRoute, notFound } from "@tanstack/react-router";

import { HRPageHeader, InfoGrid, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { applications } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/recruitment/applications/$applicationId/")({
  component: HRApplicationDetailPage,
  loader: ({ params }) => {
    const application = applications.find(item => item.id === params.applicationId);
    if (!application) {
      throw notFound();
    }
    return { application };
  },
});

function HRApplicationDetailPage() {
  const { application } = Route.useLoaderData();

  return (
    <div className="space-y-6">
      <HRPageHeader title={application.candidate} description={`${application.position} candidate profile and recruitment timeline.`} />
      <div className="grid gap-4 lg:grid-cols-2">
        <SectionCard title="Candidate Profile">
          <InfoGrid items={[
            { label: "Contact", value: application.contact },
            { label: "Location", value: application.location },
            { label: "Education", value: application.education },
            { label: "Experience", value: application.experience },
            { label: "Skills", value: application.skills.join(", ") },
          ]}
          />
        </SectionCard>
        <SectionCard title="Application">
          <InfoGrid items={[
            { label: "Position", value: application.position },
            { label: "Application date", value: application.applicationDate },
            { label: "Status", value: <StatusBadge value={application.status} /> },
            { label: "Recruiter", value: application.recruiter },
            { label: "Interview date", value: application.interviewDate ?? "Not scheduled" },
            { label: "Resume", value: "resume.pdf" },
          ]}
          />
        </SectionCard>
      </div>
      <SectionCard title="Recruitment Timeline">
        <div className="space-y-3">
          {["Application submitted", "Screening completed", "Candidate shortlisted", "Interview scheduled", "Interview completed", "Offer sent"].map((item, index) => (
            <div key={item} className="flex items-center gap-3 rounded-md border p-3 text-sm">
              <span className="flex h-6 w-6 items-center justify-center rounded-full bg-sky-100 text-xs font-medium text-sky-700">{index + 1}</span>
              {item}
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
