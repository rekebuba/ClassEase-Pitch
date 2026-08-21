import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, BriefcaseBusiness, CheckCircle2, Circle, FileText, GraduationCap, School, UserRound } from "lucide-react";

import { ApplicationStatusBadge } from "@/components/guest/application-status-badge";
import { useGuest } from "@/components/guest/guest-context";
import { SchoolCard } from "@/components/guest/school-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { getOpenPositions, guestSchools, isEnrollmentAcceptingApplications, isPositionAcceptingApplications } from "@/lib/guest-data";

import type { ReactNode } from "react";

export const Route = createFileRoute("/guest/")({
  component: GuestDashboard,
});

function GuestDashboard() {
  const { profile, applications, isEmploymentProfileComplete, missingProfileFields } = useGuest();
  const displayName = profile.firstName || "there";
  const featuredSchools = guestSchools
    .filter(school =>
      school.enrollmentOpportunities.some(isEnrollmentAcceptingApplications)
      || school.positions.some(isPositionAcceptingApplications))
    .slice(0, 3);
  const openPositionCount = getOpenPositions().filter(({ position }) => isPositionAcceptingApplications(position)).length;
  const openEnrollmentCount = guestSchools.flatMap(school => school.enrollmentOpportunities).filter(isEnrollmentAcceptingApplications).length;
  const pendingCount = applications.filter(application => application.status === "Pending").length;
  const reviewCount = applications.filter(application => application.status === "Under Review").length;

  return (
    <div className="space-y-6">
      <section className="rounded-xl border bg-background p-6 sm:p-8">
        <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
          <div className="space-y-5">
            <div className="space-y-2">
              <Badge variant="secondary">Guest / Pre-Membership</Badge>
              <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
                Welcome back,
                {" "}
                {displayName}
              </h1>
              <p className="max-w-2xl text-muted-foreground">
                Find a school that's right for you. Explore schools, enroll a student, or find an open position.
              </p>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <ActionCard
                icon={<GraduationCap className="size-5" />}
                title="Enroll a Student"
                description="Find schools accepting new students for the upcoming academic year."
                buttonLabel="Find Schools"
                to="/guest/schools"
              />
              <ActionCard
                icon={<BriefcaseBusiness className="size-5" />}
                title="Find a Position"
                description="Explore schools currently hiring teachers, administrators, and staff."
                buttonLabel="View Positions"
                to="/guest/jobs"
              />
            </div>
          </div>
          <Card className="rounded-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <School className="size-5 text-sky-600" />
                Currently accepting
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-3 text-center">
              <Metric label="Enrollment" value={openEnrollmentCount} />
              <Metric label="Positions" value={openPositionCount} />
            </CardContent>
          </Card>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1fr_340px]">
        <section className="space-y-4">
          <div className="flex items-center justify-between gap-3">
            <div>
              <h2 className="text-xl font-semibold">Discover Schools</h2>
              <p className="text-sm text-muted-foreground">Schools showing public enrollment or employment opportunities.</p>
            </div>
            <Button variant="outline" asChild>
              <Link to="/guest/schools">
                Explore Schools
                <ArrowRight className="size-4" />
              </Link>
            </Button>
          </div>
          <div className="grid gap-4">
            {featuredSchools.map(school => <SchoolCard key={school.slug} school={school} />)}
          </div>
        </section>

        <aside className="space-y-4">
          <Card className="rounded-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {isEmploymentProfileComplete
                  ? <CheckCircle2 className="size-5 text-emerald-600" />
                  : <UserRound className="size-5 text-sky-600" />}
                Employment Profile
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {isEmploymentProfileComplete
                ? (
                    <p className="text-sm text-muted-foreground">
                      Your employment profile is complete and can be reused when applying for positions.
                    </p>
                  )
                : (
                    <div className="space-y-3">
                      <p className="text-sm text-muted-foreground">
                        Complete this only when you're ready to apply for a position.
                      </p>
                      <div className="rounded-lg border bg-muted/40 p-3">
                        <p className="text-sm font-medium">
                          {missingProfileFields.length}
                          {" "}
                          item
                          {missingProfileFields.length === 1 ? "" : "s"}
                          {" "}
                          remaining
                        </p>
                        <div className="mt-2 grid gap-1 text-sm text-muted-foreground">
                          {missingProfileFields.slice(0, 4).map(field => (
                            <span key={field.key} className="inline-flex items-center gap-2">
                              <Circle className="size-3" />
                              {field.label}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
              <Button variant="outline" className="w-full" asChild>
                <Link to="/guest/profile">
                  {isEmploymentProfileComplete ? "View Profile" : "Complete Profile"}
                </Link>
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
                        <Metric label="Applications" value={applications.length} />
                        <Metric label="Pending" value={pendingCount} />
                        <Metric label="Review" value={reviewCount} />
                      </div>
                      <div className="space-y-2">
                        {applications.slice(0, 2).map(application => (
                          <div key={application.id} className="rounded-lg border p-3">
                            <p className="font-medium">{application.opportunityTitle}</p>
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
                          <FileText />
                        </EmptyMedia>
                        <EmptyTitle>No applications yet</EmptyTitle>
                        <EmptyDescription>Choose a school, enrollment opportunity, or position to get started.</EmptyDescription>
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

function ActionCard({
  icon,
  title,
  description,
  buttonLabel,
  to,
}: {
  icon: ReactNode;
  title: string;
  description: string;
  buttonLabel: string;
  to: "/guest/schools" | "/guest/jobs";
}) {
  return (
    <Card className="rounded-lg">
      <CardContent className="space-y-4">
        <div className="flex size-10 items-center justify-center rounded-lg bg-sky-50 text-sky-700">
          {icon}
        </div>
        <div className="space-y-1">
          <h2 className="font-semibold">{title}</h2>
          <p className="text-sm leading-6 text-muted-foreground">{description}</p>
        </div>
        <Button asChild>
          <Link to={to}>
            {buttonLabel}
            <ArrowRight className="size-4" />
          </Link>
        </Button>
      </CardContent>
    </Card>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg bg-muted p-3">
      <p className="text-2xl font-semibold">{value}</p>
      <p className="text-xs text-muted-foreground">{label}</p>
    </div>
  );
}
