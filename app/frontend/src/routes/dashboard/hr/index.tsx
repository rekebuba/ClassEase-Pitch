import { createFileRoute } from "@tanstack/react-router";
import { BriefcaseBusiness, CalendarDays, UserCheck, Users } from "lucide-react";

import { HRPageHeader, HRStatCard, MiniBar, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { employees, employmentTypes, pipeline, workforceByDepartment } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/")({
  component: HRDashboardPage,
});

function HRDashboardPage() {
  return (
    <div className="space-y-6">
      <HRPageHeader
        title="HR Management"
        description="Workforce overview for the currently selected school, using local HR mock data until API integration is ready."
      />

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <HRStatCard title="Total Employees" value="184" detail="112 teaching, 72 operations" icon={Users} />
        <HRStatCard title="Active Employees" value="176" detail="95.7% active workforce" icon={UserCheck} />
        <HRStatCard title="Employees on Leave" value="8" detail="5 sick, 3 annual leave" icon={CalendarDays} />
        <HRStatCard title="Open Positions" value="6" detail="24 pending applications" icon={BriefcaseBusiness} />
      </div>

      <div className="grid gap-4 lg:grid-cols-7">
        <div className="lg:col-span-3">
          <SectionCard title="Workforce Overview" description="Employee distribution by department">
            <div className="space-y-4">
              {workforceByDepartment.map(item => (
                <MiniBar key={item.department} label={item.department} value={item.employees} max={112} />
              ))}
            </div>
          </SectionCard>
        </div>
        <div className="lg:col-span-3">
          <SectionCard title="Employment Type" description="Contract mix across school employees">
            <div className="space-y-4">
              {employmentTypes.map(item => (
                <MiniBar key={item.type} label={item.type} value={item.count} max={138} className="bg-emerald-500" />
              ))}
            </div>
          </SectionCard>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <SectionCard title="Recent Employees" description="New and recently updated employee records">
          <div className="space-y-4">
            {employees.slice(0, 5).map(employee => (
              <div key={employee.id} className="flex items-center justify-between gap-3 rounded-md border p-3">
                <div>
                  <div className="font-medium">{employee.name}</div>
                  <div className="text-sm text-muted-foreground">
                    {employee.position}
                    {" · "}
                    {employee.department}
                  </div>
                </div>
                <StatusBadge value={employee.status} />
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Recruitment Pipeline" description="Current hiring funnel">
          <div className="grid gap-3 sm:grid-cols-3">
            {pipeline.map(stage => (
              <div key={stage.stage} className="rounded-md border p-3">
                <div className="text-2xl font-bold">{stage.count}</div>
                <div className="text-sm text-muted-foreground">{stage.stage}</div>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Upcoming HR Events">
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
          {[
            "Rahel Tadesse returns from sick leave on Aug 23",
            "Biruk Lemma interview scheduled for Aug 22",
            "Abebe Kebede birthday on Aug 28",
            "Teaching certificate expires Oct 10",
          ].map(event => <div key={event} className="rounded-md border p-3 text-sm">{event}</div>)}
        </div>
      </SectionCard>
    </div>
  );
}
