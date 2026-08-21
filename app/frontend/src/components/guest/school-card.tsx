import { Link } from "@tanstack/react-router";
import { ArrowRight, BriefcaseBusiness, CalendarDays, GraduationCap, MapPin } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { formatGuestDate, isEnrollmentAcceptingApplications, isPositionAcceptingApplications } from "@/lib/guest-data";

import type { GuestSchool } from "@/lib/guest-data";

export function SchoolCard({ school }: { school: GuestSchool }) {
  const openEnrollment = school.enrollmentOpportunities.filter(isEnrollmentAcceptingApplications);
  const openPositions = school.positions.filter(isPositionAcceptingApplications);
  const acceptingApplications = openEnrollment.length > 0 || openPositions.length > 0;
  const nextDeadline = [...openEnrollment.map(item => item.deadline), ...openPositions.map(item => item.deadline)].sort()[0];

  return (
    <Card className="rounded-lg">
      <CardContent className="space-y-5">
        <div className="flex items-start gap-4">
          <Avatar className="size-12 rounded-lg">
            <AvatarFallback className="rounded-lg bg-sky-100 font-semibold text-sky-700">
              {school.logo}
            </AvatarFallback>
          </Avatar>
          <div className="min-w-0 flex-1 space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="font-semibold">{school.name}</h3>
              <Badge variant={acceptingApplications ? "default" : "secondary"}>
                {acceptingApplications ? "Accepting applications" : "No public openings"}
              </Badge>
            </div>
            <p className="flex items-center gap-1 text-sm text-muted-foreground">
              <MapPin className="size-4" />
              {school.location}
            </p>
          </div>
        </div>

        <div className="space-y-2">
          <p className="text-sm font-medium">{school.category}</p>
          <p className="text-sm leading-6 text-muted-foreground">{school.description}</p>
        </div>

        <div className="space-y-2">
          <div className="grid gap-3 sm:grid-cols-2">
            <div className="rounded-lg border p-3">
              <p className="flex items-center gap-2 text-sm font-medium">
                <GraduationCap className="size-4 text-sky-600" />
                Student Enrollment
              </p>
              <p className="mt-2 text-sm text-muted-foreground">
                {openEnrollment.length > 0
                  ? openEnrollment.map(item => item.grade).join(", ")
                  : "Not currently accepting"}
              </p>
            </div>
            <div className="rounded-lg border p-3">
              <p className="flex items-center gap-2 text-sm font-medium">
                <BriefcaseBusiness className="size-4 text-sky-600" />
                Open Positions
              </p>
              <p className="mt-2 text-sm text-muted-foreground">
                {openPositions.length > 0
                  ? openPositions.slice(0, 2).map(position => position.title).join(", ")
                  : "Not currently hiring"}
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-3 border-t pt-4 sm:flex-row sm:items-center sm:justify-between">
          <span className="inline-flex items-center gap-1 text-sm text-muted-foreground">
            <CalendarDays className="size-4" />
            {nextDeadline ? `Next deadline ${formatGuestDate(nextDeadline)}` : "No active deadline"}
          </span>
          <Button variant="outline" asChild>
            <Link to="/guest/schools/$schoolSlug" params={{ schoolSlug: school.slug }}>
              View School
              <ArrowRight className="size-4" />
            </Link>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
