import { createFileRoute } from "@tanstack/react-router";
import { ChartNoAxesCombined, ClipboardList, Star, TrendingUp } from "lucide-react";

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HRPageHeader, HRStatCard, InfoGrid, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { performanceReviews } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/performance/")({
  component: HRPerformancePage,
});

function HRPerformancePage() {
  const selected = performanceReviews[0];

  return (
    <div className="space-y-6">
      <HRPageHeader title="Performance Management" description="Review completion, staff ratings, goals, and improvement planning." />
      <div className="grid gap-4 md:grid-cols-4">
        <HRStatCard title="Employees Reviewed" value="138" detail="75% completion" icon={ClipboardList} />
        <HRStatCard title="Pending Reviews" value="32" detail="Due before Sep 15" icon={TrendingUp} />
        <HRStatCard title="Average Rating" value="4.1" detail="Out of 5" icon={Star} />
        <HRStatCard title="Improvement Plans" value="5" detail="Active support plans" icon={ChartNoAxesCombined} />
      </div>
      <SectionCard title="Performance Reviews">
        <div className="overflow-hidden rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Employee</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Position</TableHead>
                <TableHead>Review Period</TableHead>
                <TableHead>Rating</TableHead>
                <TableHead>Reviewer</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {performanceReviews.map(review => (
                <TableRow key={review.id}>
                  <TableCell className="font-medium">{review.employee}</TableCell>
                  <TableCell>{review.department}</TableCell>
                  <TableCell>{review.position}</TableCell>
                  <TableCell>{review.period}</TableCell>
                  <TableCell>{review.rating}</TableCell>
                  <TableCell>{review.reviewer}</TableCell>
                  <TableCell><StatusBadge value={review.status} /></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </SectionCard>
      <SectionCard title="Performance Detail Preview">
        <InfoGrid items={[
          { label: "Employee", value: selected.employee },
          { label: "Overall rating", value: selected.rating },
          { label: "Goals", value: "Improve parent feedback loop and document weekly intervention outcomes." },
          { label: "Achievements", value: "Delivered strong assessment preparation and peer mentoring." },
          { label: "Areas for improvement", value: "Tighter reporting cadence for intervention groups." },
          { label: "Manager comments", value: selected.comments },
        ]}
        />
      </SectionCard>
    </div>
  );
}
