import { CheckCircle2, CircleAlert } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { getProfileMissingFields } from "@/lib/guest-data";

import type { GuestProfile } from "@/lib/guest-data";

export function ProfileSummary({ profile }: { profile: GuestProfile }) {
  const missing = getProfileMissingFields(profile);

  return (
    <Card className="rounded-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          {missing.length === 0
            ? <CheckCircle2 className="size-5 text-emerald-600" />
            : <CircleAlert className="size-5 text-amber-600" />}
          Your profile
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {missing.length > 0 && (
          <div className="rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
            <p className="font-medium">
              {missing.length}
              {" "}
              item
              {missing.length === 1 ? "" : "s"}
              {" "}
              remaining
            </p>
            <div className="mt-2 flex flex-wrap gap-2">
              {missing.map(field => <Badge key={field.key} variant="outline" className="bg-white">{field.label}</Badge>)}
            </div>
          </div>
        )}
        <div className="grid gap-4 text-sm sm:grid-cols-2">
          <SummaryItem label="Applicant" value={`${profile.firstName} ${profile.lastName}`.trim() || "Not provided"} />
          <SummaryItem label="Email" value={profile.email || "Not provided"} />
          <SummaryItem label="Phone" value={profile.phone || "Not provided"} />
          <SummaryItem label="Location" value={profile.city || "Not provided"} />
        </div>
        <Separator />
        <div className="grid gap-4 text-sm sm:grid-cols-2">
          <SummaryItem label="Education" value={[profile.highestEducation, profile.fieldOfStudy].filter(Boolean).join(" in ") || "Not provided"} />
          <SummaryItem label="Institution" value={profile.institution || "Optional"} />
          <SummaryItem label="Experience" value={profile.yearsOfExperience ? `${profile.yearsOfExperience} years` : "Optional"} />
          <SummaryItem label="Skills" value={profile.skills || "Optional"} />
        </div>
      </CardContent>
    </Card>
  );
}

function SummaryItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase text-muted-foreground">{label}</p>
      <p className="mt-1 font-medium">{value}</p>
    </div>
  );
}
