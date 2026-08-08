import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, BriefcaseBusiness, CheckCircle2, FileText, Search, UserRound } from "lucide-react";
import { useMemo, useState } from "react";

import { ApplicationStatusBadge } from "@/components/guest/application-status-badge";
import { useGuest } from "@/components/guest/guest-context";
import { ProfileForm } from "@/components/guest/profile-form";
import { ProfileProgress } from "@/components/guest/profile-progress";
import { SchoolCard } from "@/components/guest/school-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { guestSchools } from "@/lib/guest-data";

export const Route = createFileRoute("/guest/")({
  component: GuestDashboard,
});

function GuestDashboard() {
  const { profile, applications, isProfileComplete, saveProfile, loadDemoProfile } = useGuest();
  const [query, setQuery] = useState("");
  const [loadingPreview, setLoadingPreview] = useState(false);
  const displayName = profile.firstName || "there";

  const filteredSchools = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return guestSchools.filter(school => school.applicationsOpen).slice(0, 3);
    }

    return guestSchools.filter((school) => {
      const positionText = school.positions.map(position => position.title).join(" ");
      return `${school.name} ${school.location} ${school.category} ${positionText}`.toLowerCase().includes(normalized);
    });
  }, [query]);

  function onSearchChange(value: string) {
    setQuery(value);
    setLoadingPreview(true);
    window.setTimeout(() => setLoadingPreview(false), 250);
  }

  if (!isProfileComplete) {
    return (
      <div className="mx-auto max-w-5xl space-y-6">
        <section className="rounded-xl border bg-background p-6 sm:p-8">
          <div className="max-w-2xl space-y-3">
            <Badge variant="secondary">First-time setup</Badge>
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
              Complete your profile once. Apply anywhere.
            </h1>
            <p className="text-muted-foreground">
              Create a reusable application profile with the information schools commonly ask for. You can save it now and return later.
            </p>
          </div>
        </section>
        <ProfileForm profile={profile} onSave={saveProfile} onUseSample={loadDemoProfile} />
      </div>
    );
  }

  const pendingCount = applications.filter(application => application.status === "Pending").length;
  const reviewCount = applications.filter(application => application.status === "Under Review").length;

  return (
    <div className="space-y-6">
      <section className="rounded-xl border bg-background p-6 sm:p-8">
        <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
          <div className="space-y-5">
            <div className="space-y-2">
              <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
                Welcome back,
                {" "}
                {displayName}
              </h1>
              <p className="max-w-2xl text-muted-foreground">
                Find a school that's looking for you. Browse schools and open positions, then apply with your saved profile.
              </p>
            </div>
            <div className="relative max-w-2xl">
              <Search className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
              <Input
                value={query}
                onChange={event => onSearchChange(event.target.value)}
                placeholder="Search schools or positions..."
                className="pl-9"
              />
            </div>
          </div>
          <Card className="rounded-lg">
            <CardContent className="space-y-4">
              <ProfileProgress profile={profile} />
              <Button variant="outline" className="w-full" asChild>
                <Link to="/guest/profile">
                  View Profile
                  <UserRound className="size-4" />
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1fr_340px]">
        <section className="space-y-4">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h2 className="text-xl font-semibold">Open Opportunities</h2>
              <p className="text-sm text-muted-foreground">Schools currently accepting applications.</p>
            </div>
            <Button variant="outline" asChild>
              <Link to="/guest/schools">
                Explore Schools
                <ArrowRight className="size-4" />
              </Link>
            </Button>
          </div>
          {loadingPreview
            ? (
                <div className="grid gap-4">
                  <Skeleton className="h-60 rounded-lg" />
                  <Skeleton className="h-60 rounded-lg" />
                </div>
              )
            : (
                <div className="grid gap-4">
                  {filteredSchools.map(school => <SchoolCard key={school.slug} school={school} />)}
                </div>
              )}
        </section>

        <aside className="space-y-4">
          <Card className="rounded-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle2 className="size-5 text-emerald-600" />
                Profile
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-sm text-muted-foreground">Your reusable application profile is complete.</p>
              <Button variant="outline" className="w-full" asChild>
                <Link to="/guest/profile">View Profile</Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="rounded-lg">
            <CardHeader>
              <CardTitle>My Applications</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {applications.length > 0
                ? (
                    <>
                      <div className="grid grid-cols-3 gap-3 text-center">
                        <ApplicationMetric label="Applications" value={applications.length} />
                        <ApplicationMetric label="Pending" value={pendingCount} />
                        <ApplicationMetric label="Review" value={reviewCount} />
                      </div>
                      <div className="space-y-2">
                        {applications.slice(0, 2).map(application => (
                          <div key={application.id} className="rounded-lg border p-3">
                            <p className="font-medium">{application.positionTitle}</p>
                            <p className="text-sm text-muted-foreground">{application.schoolName}</p>
                            <ApplicationStatusBadge status={application.status} className="mt-2" />
                          </div>
                        ))}
                      </div>
                      <Button className="w-full" asChild>
                        <Link to="/guest/applications">
                          View Applications
                          <FileText className="size-4" />
                        </Link>
                      </Button>
                    </>
                  )
                : (
                    <Empty className="border p-6">
                      <EmptyHeader>
                        <EmptyMedia variant="icon">
                          <BriefcaseBusiness />
                        </EmptyMedia>
                        <EmptyTitle>No applications yet</EmptyTitle>
                        <EmptyDescription>Explore schools that are currently accepting applications.</EmptyDescription>
                      </EmptyHeader>
                      <EmptyContent>
                        <Button asChild>
                          <Link to="/guest/schools">Explore Schools</Link>
                        </Button>
                      </EmptyContent>
                    </Empty>
                  )}
            </CardContent>
          </Card>
        </aside>
      </div>
    </div>
  );
}

function ApplicationMetric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg bg-muted p-3">
      <p className="text-2xl font-semibold">{value}</p>
      <p className="text-xs text-muted-foreground">{label}</p>
    </div>
  );
}
