import { createFileRoute, notFound } from "@tanstack/react-router";

import { EmployeeTable, HRPageHeader, InfoGrid, MiniBar, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { departments, employees, positions } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/departments/$departmentId/")({
  component: HRDepartmentDetailPage,
  loader: ({ params }) => {
    const department = departments.find(item => item.id === params.departmentId);
    if (!department) {
      throw notFound();
    }
    return { department };
  },
});

function HRDepartmentDetailPage() {
  const { department } = Route.useLoaderData();
  const departmentEmployees = employees.filter(employee => employee.department === department.name);
  const departmentPositions = positions.filter(position => position.department === department.name);

  return (
    <div className="space-y-6">
      <HRPageHeader title={department.name} description="Department overview, staffing, vacancies, and recent HR activity." />
      <div className="grid gap-4 lg:grid-cols-2">
        <SectionCard title="Department Overview">
          <InfoGrid items={[
            { label: "Code", value: department.code },
            { label: "Manager", value: department.manager },
            { label: "Employees", value: department.employees },
            { label: "Open positions", value: department.openPositions },
            { label: "Budget", value: department.budget },
            { label: "Status", value: <StatusBadge value={department.status} /> },
          ]}
          />
        </SectionCard>
        <SectionCard title="Vacancy Pressure">
          <MiniBar label="Open positions" value={department.openPositions} max={6} className="bg-amber-500" />
          <div className="mt-4 space-y-3">
            {departmentPositions.map(position => (
              <div key={position.id} className="flex items-center justify-between rounded-md border p-3">
                <span>{position.title}</span>
                <StatusBadge value={position.status} />
              </div>
            ))}
          </div>
        </SectionCard>
      </div>
      <SectionCard title="Employees">
        <EmployeeTable rows={departmentEmployees} />
      </SectionCard>
      <SectionCard title="Recent Activity">
        <div className="space-y-3">
          {department.activity.map(item => <div key={item} className="rounded-md border p-3 text-sm">{item}</div>)}
        </div>
      </SectionCard>
    </div>
  );
}
