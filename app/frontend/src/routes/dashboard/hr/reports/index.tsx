import { createFileRoute } from "@tanstack/react-router";
import { BarChart3, BriefcaseBusiness, CalendarDays, ClipboardCheck, Users } from "lucide-react";

import { HRPageHeader, HRStatCard, MiniBar, SectionCard } from "@/features/hr/components/common";
import { attendanceTrend, employmentTypes, pipeline, workforceByDepartment } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/reports/")({
  component: HRReportsPage,
});

function HRReportsPage() {
  return (
    <div className="space-y-6">
      <HRPageHeader title="HR Reports" description="Static workforce, recruitment, leave, attendance, and performance reporting views." />
      <div className="grid gap-4 md:grid-cols-5">
        <HRStatCard title="Workforce" value="184" detail="Total employees" icon={Users} />
        <HRStatCard title="Recruitment" value="24" detail="Applications" icon={BriefcaseBusiness} />
        <HRStatCard title="Leave" value="8" detail="On leave today" icon={CalendarDays} />
        <HRStatCard title="Attendance" value="96.4%" detail="Monthly rate" icon={BarChart3} />
        <HRStatCard title="Performance" value="75%" detail="Reviews complete" icon={ClipboardCheck} />
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <SectionCard title="Workforce Report">
          <div className="space-y-4">
            {workforceByDepartment.map(item => <MiniBar key={item.department} label={item.department} value={item.employees} max={112} />)}
          </div>
        </SectionCard>
        <SectionCard title="Employment Types">
          <div className="space-y-4">
            {employmentTypes.map(item => <MiniBar key={item.type} label={item.type} value={item.count} max={138} className="bg-emerald-500" />)}
          </div>
        </SectionCard>
        <SectionCard title="Recruitment Report">
          <div className="space-y-4">
            {pipeline.map(item => <MiniBar key={item.stage} label={item.stage} value={item.count} max={24} className="bg-amber-500" />)}
          </div>
        </SectionCard>
        <SectionCard title="Attendance Report">
          <div className="space-y-4">
            {attendanceTrend.map(item => <MiniBar key={item.day} label={item.day} value={item.rate} max={100} className="bg-slate-500" />)}
          </div>
        </SectionCard>
      </div>
    </div>
  );
}
