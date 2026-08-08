import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { CalendarDays, MapPin, UsersRound } from "lucide-react";

import { PositionCard } from "@/components/guest/position-card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { findSchool, formatGuestDate } from "@/lib/guest-data";

export const Route = createFileRoute("/guest/schools/$schoolSlug/")({
  component: SchoolDetailsPage,
});

function SchoolDetailsPage() {
  const { schoolSlug } = Route.useParams();
  const school = findSchool(schoolSlug);

  if (!school) {
    throw notFound();
  }

  return (
    <div className="space-y-6">
      <section className="rounded-xl border bg-background p-6 sm:p-8">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div className="flex items-start gap-4">
            <Avatar className="size-16 rounded-xl">
              <AvatarFallback className="rounded-xl bg-sky-100 text-lg font-semibold text-sky-700">
                {school.logo}
              </AvatarFallback>
            </Avatar>
            <div className="space-y-3">
              <div>
                <div className="mb-2 flex flex-wrap items-center gap-2">
                  <Badge variant="secondary">{school.category}</Badge>
                  <Badge variant={school.applicationsOpen ? "default" : "secondary"}>
                    {school.applicationsOpen ? "Applications open" : "Applications closed"}
                  </Badge>
                </div>
                <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">{school.name}</h1>
                <p className="mt-2 flex items-center gap-1 text-muted-foreground">
                  <MapPin className="size-4" />
                  {school.location}
                </p>
              </div>
              <p className="max-w-3xl leading-7 text-muted-foreground">{school.description}</p>
            </div>
          </div>
          <Button asChild>
            <Link
              to="/guest/schools/$schoolSlug/positions/$positionId"
              params={{ schoolSlug: school.slug, positionId: school.positions[0]?.id ?? "" }}
            >
              View First Position
            </Link>
          </Button>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
        <section className="space-y-6">
          <Card className="rounded-lg">
            <CardHeader>
              <CardTitle>About</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="leading-7 text-muted-foreground">{school.about}</p>
            </CardContent>
          </Card>

          <section className="space-y-4">
            <div>
              <h2 className="text-xl font-semibold">Open Positions</h2>
              <p className="text-sm text-muted-foreground">Choose a position to review requirements before applying.</p>
            </div>
            <div className="grid gap-4">
              {school.positions.map(position => (
                <PositionCard key={position.id} schoolSlug={school.slug} position={position} />
              ))}
            </div>
          </section>
        </section>

        <aside>
          <Card className="rounded-lg">
            <CardHeader>
              <CardTitle>School information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-sm">
              <InfoRow icon={<UsersRound className="size-4" />} label="School size" value={school.students} />
              <Separator />
              <InfoRow label="Curriculum" value={school.curriculum} />
              <Separator />
              <InfoRow icon={<CalendarDays className="size-4" />} label="Application deadline" value={formatGuestDate(school.deadline)} />
            </CardContent>
          </Card>
        </aside>
      </div>
    </div>
  );
}

function InfoRow({ icon, label, value }: { icon?: React.ReactNode; label: string; value: string }) {
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
