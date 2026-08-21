import { createFileRoute } from "@tanstack/react-router";
import { CalendarCheck, Clock, Plane, UserCheck } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HRPageHeader, HRStatCard, MockActionDialog, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { leaveRequests } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/leave/")({
  component: HRLeavePage,
});

function HRLeavePage() {
  const [requests, setRequests] = useState(leaveRequests);

  return (
    <div className="space-y-6">
      <HRPageHeader title="Leave Management" description="Leave requests, approvals, balances, and upcoming absences." actions={<MockActionDialog label="Leave Request" title="New leave request" description="Mock leave request form." />} />
      <div className="grid gap-4 md:grid-cols-4">
        <HRStatCard title="Pending Requests" value={String(requests.filter(item => item.status === "Pending").length)} detail="Need HR action" icon={Clock} />
        <HRStatCard title="Approved" value={String(requests.filter(item => item.status === "Approved").length)} detail="Current cycle" icon={CalendarCheck} />
        <HRStatCard title="On Leave Today" value="8" detail="Across all departments" icon={Plane} />
        <HRStatCard title="Upcoming Leave" value="12" detail="Next 30 days" icon={UserCheck} />
      </div>
      <SectionCard title="Leave Requests">
        <div className="overflow-hidden rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Employee</TableHead>
                <TableHead>Leave Type</TableHead>
                <TableHead>Start</TableHead>
                <TableHead>End</TableHead>
                <TableHead>Duration</TableHead>
                <TableHead>Reason</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {requests.map(request => (
                <TableRow key={request.id}>
                  <TableCell className="font-medium">{request.employee}</TableCell>
                  <TableCell>{request.type}</TableCell>
                  <TableCell>{request.startDate}</TableCell>
                  <TableCell>{request.endDate}</TableCell>
                  <TableCell>{request.duration}</TableCell>
                  <TableCell>{request.reason}</TableCell>
                  <TableCell><StatusBadge value={request.status} /></TableCell>
                  <TableCell>
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={request.status !== "Pending"}
                      onClick={() => setRequests(current => current.map(item => item.id === request.id ? { ...item, status: "Approved" } : item))}
                    >
                      Approve
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </SectionCard>
    </div>
  );
}
