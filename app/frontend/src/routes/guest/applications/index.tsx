import { createFileRoute, Link } from "@tanstack/react-router";
import { BriefcaseBusiness, Search } from "lucide-react";
import { useMemo, useState } from "react";

import { ApplicationCard } from "@/components/guest/application-card";
import { useGuest } from "@/components/guest/guest-context";
import { Button } from "@/components/ui/button";
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const Route = createFileRoute("/guest/applications/")({
  component: ApplicationsPage,
});

function ApplicationsPage() {
  const { applications } = useGuest();
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState("all");

  const filteredApplications = useMemo(() => {
    const normalized = query.trim().toLowerCase();

    return applications.filter((application) => {
      const matchesQuery = !normalized
        || `${application.positionTitle} ${application.schoolName}`.toLowerCase().includes(normalized);
      const matchesStatus = status === "all" || application.status === status;

      return matchesQuery && matchesStatus;
    });
  }, [applications, query, status]);

  return (
    <div className="space-y-6">
      <section className="rounded-xl border bg-background p-6 sm:p-8">
        <div className="space-y-2">
          <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">My Applications</h1>
          <p className="text-muted-foreground">Track applications submitted with your reusable profile.</p>
        </div>
      </section>

      {applications.length > 0 && (
        <section className="grid gap-3 rounded-lg border bg-background p-4 md:grid-cols-[1fr_220px]">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
            <Input
              value={query}
              onChange={event => setQuery(event.target.value)}
              placeholder="Search applications..."
              className="pl-9"
            />
          </div>
          <Select value={status} onValueChange={setStatus}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All statuses</SelectItem>
              <SelectItem value="Pending">Pending</SelectItem>
              <SelectItem value="Under Review">Under Review</SelectItem>
              <SelectItem value="Accepted">Accepted</SelectItem>
              <SelectItem value="Rejected">Rejected</SelectItem>
              <SelectItem value="Withdrawn">Withdrawn</SelectItem>
            </SelectContent>
          </Select>
        </section>
      )}

      {applications.length === 0
        ? (
            <Empty className="border bg-background">
              <EmptyHeader>
                <EmptyMedia variant="icon">
                  <BriefcaseBusiness />
                </EmptyMedia>
                <EmptyTitle>You haven't applied to any schools yet.</EmptyTitle>
                <EmptyDescription>Explore schools that are currently accepting applications.</EmptyDescription>
              </EmptyHeader>
              <EmptyContent>
                <Button asChild>
                  <Link to="/guest/schools">Explore Schools</Link>
                </Button>
              </EmptyContent>
            </Empty>
          )
        : filteredApplications.length > 0
          ? (
              <div className="grid gap-4">
                {filteredApplications.map(application => (
                  <ApplicationCard key={application.id} application={application} />
                ))}
              </div>
            )
          : (
              <Empty className="border bg-background">
                <EmptyHeader>
                  <EmptyMedia variant="icon">
                    <Search />
                  </EmptyMedia>
                  <EmptyTitle>No matching applications</EmptyTitle>
                  <EmptyDescription>Try a different search or status filter.</EmptyDescription>
                </EmptyHeader>
              </Empty>
            )}
    </div>
  );
}
