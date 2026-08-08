import { Link } from "@tanstack/react-router";
import { CalendarDays, ExternalLink } from "lucide-react";

import { ApplicationStatusBadge } from "@/components/guest/application-status-badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { formatGuestDate } from "@/lib/guest-data";

import type { GuestApplication } from "@/lib/guest-data";

export function ApplicationCard({ application }: { application: GuestApplication }) {
  return (
    <Card className="rounded-lg">
      <CardContent className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0 space-y-2">
          <div>
            <h3 className="font-semibold">{application.positionTitle}</h3>
            <p className="text-sm text-muted-foreground">{application.schoolName}</p>
          </div>
          <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
            <span className="inline-flex items-center gap-1">
              <CalendarDays className="size-4" />
              Submitted
              {" "}
              {formatGuestDate(application.submittedAt)}
            </span>
            <ApplicationStatusBadge status={application.status} />
          </div>
        </div>
        <Button variant="outline" size="sm" asChild>
          <Link to="/guest/applications/$applicationId" params={{ applicationId: application.id }}>
            View
            <ExternalLink className="size-4" />
          </Link>
        </Button>
      </CardContent>
    </Card>
  );
}
