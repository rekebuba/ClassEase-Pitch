import { CheckCircle2, Circle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { getProfileCompletion } from "@/lib/guest-data";

import type { GuestProfile } from "@/lib/guest-data";

export function ProfileProgress({ profile }: { profile: GuestProfile }) {
  const completion = getProfileCompletion(profile);
  const complete = completion === 100;

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <p className="text-sm font-medium">Profile completion</p>
          <p className="text-sm text-muted-foreground">
            {complete ? "You're ready to apply to schools." : "You're almost ready to apply to schools."}
          </p>
        </div>
        <Badge variant={complete ? "default" : "secondary"} className="gap-1">
          {complete ? <CheckCircle2 className="size-3" /> : <Circle className="size-3" />}
          {complete ? "Profile complete" : `${completion}% complete`}
        </Badge>
      </div>
      <Progress value={completion} />
    </div>
  );
}
