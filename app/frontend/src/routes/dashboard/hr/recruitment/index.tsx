import { createFileRoute, Link } from "@tanstack/react-router";
import { BriefcaseBusiness, Users } from "lucide-react";

import { Button } from "@/components/ui/button";
import { HRPageHeader, HRStatCard, MiniBar, SectionCard } from "@/features/hr/components/common";
import { applications, jobPostings, pipeline } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/recruitment/")({
  component: HRRecruitmentPage,
});

function HRRecruitmentPage() {
  return (
    <div className="space-y-6">
      <HRPageHeader
        title="Recruitment"
        description="Open roles, candidate movement, and hiring activity."
        actions={(
          <>
            <Button asChild size="sm"><Link to="/dashboard/hr/recruitment/jobs">Job Postings</Link></Button>
            <Button asChild variant="outline" size="sm"><Link to="/dashboard/hr/recruitment/applications">Applications</Link></Button>
          </>
        )}
      />
      <div className="grid gap-4 md:grid-cols-3">
        <HRStatCard title="Open Postings" value={String(jobPostings.filter(job => job.status === "Published").length)} detail="Published school vacancies" icon={BriefcaseBusiness} />
        <HRStatCard title="Applications" value={String(applications.length)} detail="Sample candidate records" icon={Users} />
        <HRStatCard title="Pending Interviews" value="2" detail="Scheduled this week" icon={Users} />
      </div>
      <SectionCard title="Candidate Pipeline">
        <div className="space-y-4">
          {pipeline.map(stage => <MiniBar key={stage.stage} label={stage.stage} value={stage.count} max={24} />)}
        </div>
      </SectionCard>
    </div>
  );
}
