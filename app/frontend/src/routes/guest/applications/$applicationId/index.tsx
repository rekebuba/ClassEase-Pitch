import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { ArrowLeft, CalendarDays, Mail, Phone, School } from "lucide-react";

import { ApplicationStatusBadge } from "@/components/guest/application-status-badge";
import { useGuest } from "@/components/guest/guest-context";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { formatGuestDate } from "@/lib/guest-data";

export const Route = createFileRoute("/guest/applications/$applicationId/")({
  component: ApplicationDetailsPage,
});

function ApplicationDetailsPage() {
  const { applicationId } = Route.useParams();
  const { applications } = useGuest();
  const application = applications.find(item => item.id === applicationId);

  if (!application) {
    throw notFound();
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6">
      <Button variant="ghost" asChild>
        <Link to="/guest/applications">
          <ArrowLeft className="size-4" />
          Back to applications
        </Link>
      </Button>

      <section className="rounded-xl border bg-background p-6 sm:p-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="space-y-2">
            <ApplicationStatusBadge status={application.status} />
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{application.positionTitle}</h1>
            <p className="text-muted-foreground">{application.schoolName}</p>
          </div>
          <Button variant="outline" asChild>
            <Link
              to="/guest/schools/$schoolSlug/positions/$positionId"
              params={{ schoolSlug: application.schoolSlug, positionId: application.positionId }}
            >
              View Position
            </Link>
          </Button>
        </div>
      </section>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="rounded-lg">
          <CardHeader>
            <CardTitle>Application</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm">
            <InfoItem icon={<School className="size-4" />} label="School" value={application.schoolName} />
            <Separator />
            <InfoItem icon={<CalendarDays className="size-4" />} label="Submitted" value={formatGuestDate(application.submittedAt)} />
            <Separator />
            <div>
              <p className="font-medium">Current status</p>
              <ApplicationStatusBadge status={application.status} className="mt-2" />
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-lg">
          <CardHeader>
            <CardTitle>Submitted profile snapshot</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm">
            <InfoItem label="Applicant" value={application.applicantName} />
            <Separator />
            <InfoItem icon={<Mail className="size-4" />} label="Email" value={application.email} />
            <Separator />
            <InfoItem icon={<Phone className="size-4" />} label="Phone" value={application.phone} />
            <Separator />
            <InfoItem label="Education" value={application.education} />
            <Separator />
            <InfoItem label="Experience" value={application.experience} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function InfoItem({ icon, label, value }: { icon?: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex gap-3">
      {icon && <span className="mt-0.5 text-muted-foreground">{icon}</span>}
      <div>
        <p className="font-medium">{label}</p>
        <p className="text-muted-foreground">{value}</p>
      </div>
    </div>
  );
}
