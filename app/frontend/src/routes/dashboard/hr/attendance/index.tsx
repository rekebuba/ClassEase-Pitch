import { createFileRoute } from "@tanstack/react-router";
import { Clock, LogIn, TimerOff, UserCheck, Users } from "lucide-react";

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HRPageHeader, HRStatCard, MiniBar, SectionCard } from "@/features/hr/components/common";
import { attendanceRecords, attendanceTrend } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/attendance/")({
  component: HRAttendancePage,
});

function HRAttendancePage() {
  return (
    <div className="space-y-6">
      <HRPageHeader title="HR Attendance" description="Staff attendance overview, late arrivals, absence, and leave counts." />
      <div className="grid gap-4 md:grid-cols-5">
        <HRStatCard title="Attendance Rate" value="96.4%" detail="This month" icon={UserCheck} />
        <HRStatCard title="Present Today" value="168" detail="Across all departments" icon={Users} />
        <HRStatCard title="Absent Today" value="3" detail="Unplanned absences" icon={TimerOff} />
        <HRStatCard title="Late Today" value="5" detail="After 8:10 AM" icon={Clock} />
        <HRStatCard title="On Leave" value="8" detail="Approved leave" icon={LogIn} />
      </div>
      <SectionCard title="Attendance Trend">
        <div className="space-y-4">
          {attendanceTrend.map(item => <MiniBar key={item.day} label={item.day} value={item.rate} max={100} />)}
        </div>
      </SectionCard>
      <SectionCard title="Monthly Attendance Table">
        <div className="overflow-hidden rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Employee</TableHead>
                <TableHead>Present</TableHead>
                <TableHead>Late</TableHead>
                <TableHead>Absent</TableHead>
                <TableHead>Leave</TableHead>
                <TableHead>Attendance %</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {attendanceRecords.map(record => (
                <TableRow key={record.employee}>
                  <TableCell className="font-medium">{record.employee}</TableCell>
                  <TableCell>{record.present}</TableCell>
                  <TableCell>{record.late}</TableCell>
                  <TableCell>{record.absent}</TableCell>
                  <TableCell>{record.leave}</TableCell>
                  <TableCell>{record.rate}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </SectionCard>
    </div>
  );
}
