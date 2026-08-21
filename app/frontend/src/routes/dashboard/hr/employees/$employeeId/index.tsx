import { createFileRoute, notFound } from "@tanstack/react-router";
import { Download, FilePlus, MoreHorizontal, Pencil, Plane } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { EmployeeIdentity, HRPageHeader, InfoGrid, MiniBar, MockActionDialog, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { attendanceRecords, documents, employees, leaveRequests, performanceReviews } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/employees/$employeeId/")({
  component: HREmployeeProfilePage,
  loader: ({ params }) => {
    const employee = employees.find(item => item.id === params.employeeId);
    if (!employee) {
      throw notFound();
    }
    return { employee };
  },
});

function HREmployeeProfilePage() {
  const { employee } = Route.useLoaderData();
  const employeeDocuments = documents.filter(document => document.employee === employee.name);
  const employeeLeave = leaveRequests.filter(leave => leave.employee === employee.name);
  const attendance = attendanceRecords.find(record => record.employee === employee.name);
  const review = performanceReviews.find(item => item.employee === employee.name);

  return (
    <div className="space-y-6">
      <HRPageHeader
        title="Employee Profile"
        description="Complete HR record, employment lifecycle, and staff activity."
        actions={(
          <>
            <Button variant="outline" size="sm"><Pencil className="mr-2 h-4 w-4" />Edit Employee</Button>
            <Button variant="outline" size="sm"><Download className="mr-2 h-4 w-4" />Download Profile</Button>
            <Button variant="outline" size="sm"><FilePlus className="mr-2 h-4 w-4" />Add Document</Button>
            <Button variant="outline" size="sm"><Plane className="mr-2 h-4 w-4" />Record Leave</Button>
            <Button variant="ghost" size="icon"><MoreHorizontal className="h-4 w-4" /></Button>
          </>
        )}
      />

      <Card>
        <CardContent className="flex flex-col gap-4 pt-6 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-4">
            <Avatar className="h-20 w-20 rounded-xl">
              <AvatarFallback className="rounded-xl bg-sky-100 text-2xl text-sky-700">{employee.initials}</AvatarFallback>
            </Avatar>
            <div>
              <h2 className="text-2xl font-bold">{employee.name}</h2>
              <p className="text-muted-foreground">
                {employee.employeeId}
                {" · "}
                {employee.position}
                {" · "}
                {employee.department}
              </p>
              <div className="mt-2 flex flex-wrap gap-2">
                <StatusBadge value={employee.status} />
                <StatusBadge value={employee.type} />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="flex h-auto flex-wrap justify-start">
          {["overview", "employment", "documents", "leave", "attendance", "performance", "activity"].map(tab => (
            <TabsTrigger key={tab} value={tab} className="capitalize">{tab}</TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value="overview" className="grid gap-4 lg:grid-cols-2">
          <SectionCard title="Personal & Contact Information">
            <InfoGrid items={[
              { label: "Full name", value: employee.name },
              { label: "Phone", value: employee.phone },
              { label: "Email", value: employee.email },
              { label: "Location", value: employee.location },
              { label: "Emergency contact", value: employee.emergencyContact },
            ]}
            />
          </SectionCard>
          <SectionCard title="Organization Information">
            <InfoGrid items={[
              { label: "Department", value: employee.department },
              { label: "Position", value: employee.position },
              { label: "Reporting manager", value: employee.manager },
              { label: "Work location", value: employee.location },
            ]}
            />
          </SectionCard>
        </TabsContent>

        <TabsContent value="employment">
          <SectionCard title="Employment Record">
            <InfoGrid items={[
              { label: "Position", value: employee.position },
              { label: "Department", value: employee.department },
              { label: "Employment type", value: employee.type },
              { label: "Employment status", value: <StatusBadge value={employee.status} /> },
              { label: "Date hired", value: employee.joinDate },
              { label: "Probation status", value: employee.probation },
              { label: "Contract start", value: employee.joinDate },
              { label: "Contract end", value: employee.contractEnd ?? "Permanent" },
              { label: "Reporting manager", value: employee.manager },
              { label: "Work location", value: employee.location },
            ]}
            />
          </SectionCard>
        </TabsContent>

        <TabsContent value="documents">
          <SectionCard title="Employee Documents">
            <div className="space-y-3">
              {employeeDocuments.length ? employeeDocuments.map(document => (
                <div key={document.id} className="flex items-center justify-between rounded-md border p-3">
                  <div>
                    <div className="font-medium">{document.name}</div>
                    <div className="text-sm text-muted-foreground">{document.category} · expires {document.expirationDate ?? "N/A"}</div>
                  </div>
                  <StatusBadge value={document.status} />
                </div>
              )) : <p className="text-sm text-muted-foreground">No mock documents for this employee.</p>}
            </div>
          </SectionCard>
        </TabsContent>

        <TabsContent value="leave">
          <SectionCard title="Leave Balance & History">
            <div className="grid gap-4 md:grid-cols-3">
              <MiniBar label="Annual" value={12} max={20} />
              <MiniBar label="Sick" value={7} max={10} className="bg-emerald-500" />
              <MiniBar label="Study" value={3} max={5} className="bg-amber-500" />
            </div>
            <div className="mt-4 space-y-3">
              {employeeLeave.map(leave => (
                <div key={leave.id} className="flex items-center justify-between rounded-md border p-3">
                  <span>{leave.type} · {leave.startDate} to {leave.endDate}</span>
                  <StatusBadge value={leave.status} />
                </div>
              ))}
            </div>
          </SectionCard>
        </TabsContent>

        <TabsContent value="attendance">
          <SectionCard title="Monthly Attendance Summary">
            {attendance
              ? (
                  <div className="grid gap-4 md:grid-cols-4">
                    <MiniBar label="Present" value={attendance.present} max={20} />
                    <MiniBar label="Late" value={attendance.late} max={5} className="bg-amber-500" />
                    <MiniBar label="Absent" value={attendance.absent} max={5} className="bg-red-500" />
                    <MiniBar label="Leave" value={attendance.leave} max={5} className="bg-emerald-500" />
                  </div>
                )
              : <p className="text-sm text-muted-foreground">No monthly attendance record available.</p>}
          </SectionCard>
        </TabsContent>

        <TabsContent value="performance">
          <SectionCard title="Performance">
            {review
              ? <InfoGrid items={[{ label: "Current rating", value: review.rating }, { label: "Review period", value: review.period }, { label: "Reviewer", value: review.reviewer }, { label: "Manager comments", value: review.comments }]} />
              : <p className="text-sm text-muted-foreground">No mock review available.</p>}
          </SectionCard>
        </TabsContent>

        <TabsContent value="activity">
          <SectionCard title="Activity Timeline">
            <div className="space-y-3">
              {["Employee joined school", "Employment contract uploaded", "Position changed", "Leave approved", "Performance review completed"].map(event => (
                <div key={event} className="rounded-md border p-3 text-sm">{event}</div>
              ))}
            </div>
          </SectionCard>
        </TabsContent>
      </Tabs>
    </div>
  );
}
