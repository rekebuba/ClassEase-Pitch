import { Link } from "@tanstack/react-router";
import { ArrowRight, CalendarDays } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { formatGuestDate } from "@/lib/guest-data";

import type { SchoolPosition } from "@/lib/guest-data";

export function PositionCard({ schoolSlug, position }: { schoolSlug: string; position: SchoolPosition }) {
  return (
    <Card className="rounded-lg">
      <CardContent className="space-y-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="font-semibold">{position.title}</h3>
              <Badge variant="secondary">{position.type}</Badge>
            </div>
            <p className="max-w-2xl text-sm text-muted-foreground">{position.summary}</p>
          </div>
          <Button asChild>
            <Link
              to="/guest/schools/$schoolSlug/positions/$positionId"
              params={{ schoolSlug, positionId: position.id }}
            >
              View Position
              <ArrowRight className="size-4" />
            </Link>
          </Button>
        </div>
        <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
          <Badge variant="outline">{position.category}</Badge>
          <span className="inline-flex items-center gap-1">
            <CalendarDays className="size-4" />
            Closes
            {" "}
            {formatGuestDate(position.deadline)}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
