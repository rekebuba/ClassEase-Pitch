import { Link } from "@tanstack/react-router";
import { ArrowRight, CalendarDays, MapPin } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { formatGuestDate } from "@/lib/guest-data";

import type { GuestSchool } from "@/lib/guest-data";

export function SchoolCard({ school }: { school: GuestSchool }) {
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
              <Badge variant={school.applicationsOpen ? "default" : "secondary"}>
                {school.applicationsOpen ? "Applications open" : "Closed"}
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
          <p className="text-sm font-medium">Open positions</p>
          <div className="flex flex-wrap gap-2">
            {school.positions.map(position => (
              <Badge key={position.id} variant="outline">
                {position.title}
              </Badge>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-3 border-t pt-4 sm:flex-row sm:items-center sm:justify-between">
          <span className="inline-flex items-center gap-1 text-sm text-muted-foreground">
            <CalendarDays className="size-4" />
            Applications close
            {" "}
            {formatGuestDate(school.deadline)}
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
