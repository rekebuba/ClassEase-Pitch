import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { ArrowLeft, CheckCircle2, CircleAlert, Send } from "lucide-react";
import { useState } from "react";

import { useGuest } from "@/components/guest/guest-context";
import { ProfileSummary } from "@/components/guest/profile-summary";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { findPosition, findSchool, formatGuestDate, isPositionAcceptingApplications } from "@/lib/guest-data";

export const Route = createFileRoute("/guest/schools/$schoolSlug/positions/$positionId/")({
  component: PositionDetailsPage,
});

function PositionDetailsPage() {
  const { schoolSlug, positionId } = Route.useParams();
  const school = findSchool(schoolSlug);
  const position = findPosition(schoolSlug, positionId);
  const { profile, isEmploymentProfileComplete, missingProfileFields, submitApplication, applications } = useGuest();
  const [reviewing, setReviewing] = useState(false);
  const [submittedApplicationId, setSubmittedApplicationId] = useState<string | null>(null);

  if (!school || !position) {
    throw notFound();
  }

  const existingApplication = applications.find(application =>
    application.kind === "Employment"
    && application.schoolSlug === school.slug
    && application.opportunityId === position.id);
  const acceptingApplications = isPositionAcceptingApplications(position);

  function submit() {
    const application = submitApplication(school!, position!);
    setSubmittedApplicationId(application.id);
    setReviewing(false);
  }

  if (submittedApplicationId || existingApplication) {
    const applicationId = submittedApplicationId ?? existingApplication!.id;
    return (
      <div className="mx-auto max-w-3xl">
        <Card className="rounded-lg border-emerald-200 bg-emerald-50">
          <CardContent className="space-y-6 p-8 text-center">
            <div className="mx-auto flex size-14 items-center justify-center rounded-full bg-emerald-100 text-emerald-700">
              <CheckCircle2 className="size-7" />
            </div>
            <div className="space-y-2">
              <h1 className="text-2xl font-semibold">Application submitted</h1>
              <p className="text-emerald-800">
                Your application for
                {" "}
                <span className="font-medium">{position.title}</span>
                {" "}
                at
                {" "}
                <span className="font-medium">{school.name}</span>
                {" "}
                has been submitted. The school will review your application.
              </p>
            </div>
            <div className="flex flex-col justify-center gap-3 sm:flex-row">
              <Button asChild>
                <Link to="/guest/applications/$applicationId" params={{ applicationId }}>
                  View Application
                </Link>
              </Button>
              <Button variant="outline" asChild>
                <Link to="/guest/jobs">Find More Positions</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (reviewing) {
    return (
      <div className="mx-auto max-w-4xl space-y-6">
        <Button variant="ghost" onClick={() => setReviewing(false)}>
          <ArrowLeft className="size-4" />
          Back to position
        </Button>
        <Card className="rounded-lg">
          <CardHeader>
            <CardTitle>Review Application</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid gap-4 text-sm md:grid-cols-2">
              <ReviewItem label="Position" value={position.title} />
              <ReviewItem label="School" value={school.name} />
              <ReviewItem label="Applicant" value={`${profile.firstName} ${profile.lastName}`} />
              <ReviewItem label="Email" value={profile.email} />
              <ReviewItem label="Phone" value={profile.phone} />
              <ReviewItem label="Education" value={profile.highestEducation} />
              <ReviewItem label="Field of study" value={profile.fieldOfStudy} />
              <ReviewItem label="Experience" value={profile.yearsOfExperience ? `${profile.yearsOfExperience} years` : "Not specified"} />
              <ReviewItem label="Skills" value={profile.skills || "Not specified"} />
            </div>
            <Separator />
            <p className="text-sm text-muted-foreground">
              This application uses your current employment profile. You can update it from your profile page before submitting.
            </p>
            <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
              <Button variant="outline" onClick={() => setReviewing(false)}>Back</Button>
              <Button onClick={submit}>
                Submit Application
                <Send className="size-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Button variant="ghost" asChild>
        <Link to="/guest/schools/$schoolSlug" params={{ schoolSlug: school.slug }}>
          <ArrowLeft className="size-4" />
          Back to school
        </Link>
      </Button>

      <section className="rounded-xl border bg-background p-6 sm:p-8">
        <div className="space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="secondary">{position.category}</Badge>
            <Badge variant="outline">{position.employmentType}</Badge>
            <Badge variant={acceptingApplications ? "default" : "secondary"}>
              {acceptingApplications ? "Applications open" : "Applications closed"}
            </Badge>
          </div>
          <div>
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{position.title}</h1>
            <p className="mt-2 text-muted-foreground">
              {school.name}
              {" "}
              ·
              {" "}
              {school.location}
            </p>
          </div>
          <p className="max-w-3xl leading-7 text-muted-foreground">{position.description}</p>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
        <section className="space-y-6">
          <DetailList title="Requirements" items={position.requirements} />
          <DetailList title="Responsibilities" items={position.responsibilities} />
          <DetailList title="Benefits" items={position.benefits} />
          <Card className="rounded-lg">
            <CardHeader>
              <CardTitle>Position details</CardTitle>
            </CardHeader>
            <CardContent className="grid gap-4 text-sm sm:grid-cols-2">
              <ReviewItem label="Location" value={position.location} />
              <ReviewItem label="Openings" value={`${position.openingsCount}`} />
              <ReviewItem label="Employment type" value={position.employmentType} />
              <ReviewItem label="Application deadline" value={formatGuestDate(position.deadline)} />
            </CardContent>
          </Card>
        </section>

        <aside className="space-y-4">
          {!acceptingApplications && (
            <Alert className="border-slate-200 bg-slate-50">
              <CircleAlert className="size-4 text-slate-700" />
              <AlertTitle>Applications are closed</AlertTitle>
              <AlertDescription>
                This position is not currently accepting applications.
              </AlertDescription>
            </Alert>
          )}
          {!isEmploymentProfileComplete && (
            <Alert className="border-amber-200 bg-amber-50">
              <CircleAlert className="size-4 text-amber-700" />
              <AlertTitle>Complete your employment profile</AlertTitle>
              <AlertDescription>
                <p>You'll only need to do this once. Your profile can be reused when applying to other positions.</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {missingProfileFields.map(field => <Badge key={field.key} variant="outline" className="bg-white">{field.label}</Badge>)}
                </div>
                <Button className="mt-3" asChild>
                  <Link to="/guest/profile">Complete Profile</Link>
                </Button>
              </AlertDescription>
            </Alert>
          )}
          <ProfileSummary profile={profile} />
          <Button className="w-full" size="lg" disabled={!isEmploymentProfileComplete || !acceptingApplications} onClick={() => setReviewing(true)}>
            {acceptingApplications ? "Apply Now" : "Applications are closed"}
          </Button>
        </aside>
      </div>
    </div>
  );
}

function DetailList({ title, items }: { title: string; items: string[] }) {
  return (
    <Card className="rounded-lg">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="grid gap-3 text-sm text-muted-foreground">
          {items.map(item => (
            <li key={item} className="flex gap-2">
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-emerald-600" />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

function ReviewItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border p-4">
      <p className="text-xs font-medium uppercase text-muted-foreground">{label}</p>
      <p className="mt-1 font-medium">{value}</p>
    </div>
  );
}
