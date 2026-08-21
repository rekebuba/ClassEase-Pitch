import { createFileRoute } from "@tanstack/react-router";
import { Download, UserPlus } from "lucide-react";

import { Button } from "@/components/ui/button";
import { FilterBar, EmployeeTable, HRPageHeader, MockActionDialog, SimplePagination, SortButton, useEmployeeFilters } from "@/features/hr/components/common";
import { departments, employees, positions } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/employees/")({
  component: HREmployeesPage,
});

function HREmployeesPage() {
  const table = useEmployeeFilters(employees);

  return (
    <div className="space-y-6">
      <HRPageHeader
        title="Employees"
        description="Search, filter, and review employees for the selected school."
        actions={(
          <>
            <Button variant="outline" size="sm"><Download className="mr-2 h-4 w-4" />Export</Button>
            <MockActionDialog label="Add Employee" title="Add employee" description="Frontend-only mock employee form.">
              <input className="h-9 rounded-md border bg-transparent px-3 text-sm" placeholder="Full name" />
              <input className="h-9 rounded-md border bg-transparent px-3 text-sm" placeholder="Position" />
              <input className="h-9 rounded-md border bg-transparent px-3 text-sm" placeholder="Department" />
            </MockActionDialog>
          </>
        )}
      />

      <div className="rounded-lg border bg-card p-4">
        <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <FilterBar
            search={table.search}
            onSearch={table.setSearch}
            filters={[
              { label: "Department", value: table.department, options: departments.map(item => item.name), onChange: table.setDepartment },
              { label: "Position", value: table.position, options: positions.map(item => item.title), onChange: table.setPosition },
              { label: "Employment Type", value: table.type, options: ["Full-time", "Part-time", "Contract", "Temporary"], onChange: table.setType },
              { label: "Status", value: table.status, options: ["Active", "On Leave", "Probation", "Inactive"], onChange: table.setStatus },
            ]}
          />
          <SortButton label="Sort" onClick={() => table.setSortKey(table.sortKey === "name" ? "joinDate" : "name")} />
        </div>
        <EmployeeTable rows={table.paged} />
        <div className="mt-4">
          <SimplePagination page={table.page} pageCount={table.pageCount} onPageChange={table.setPage} />
        </div>
      </div>
    </div>
  );
}
