import { createFileRoute, Link } from "@tanstack/react-router";
import { CheckCircle2 } from "lucide-react";

import { useGuest } from "@/components/guest/guest-context";
import { ProfileForm } from "@/components/guest/profile-form";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export const Route = createFileRoute("/guest/profile/")({
  component: GuestProfilePage,
});

function GuestProfilePage() {
  const { profile, isEmploymentProfileComplete, saveProfile, loadDemoProfile } = useGuest();

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Profile</h1>
          <p className="text-muted-foreground">Manage employment information reused when you apply for school positions.</p>
        </div>
        {isEmploymentProfileComplete && (
          <Button asChild>
            <Link to="/guest/schools">Explore Schools</Link>
          </Button>
        )}
      </div>
      {isEmploymentProfileComplete && (
        <Card className="rounded-lg border-emerald-200 bg-emerald-50">
          <CardContent className="flex items-start gap-3 text-emerald-800">
            <CheckCircle2 className="mt-0.5 size-5" />
            <div>
              <p className="font-medium">Employment profile complete</p>
              <p className="text-sm">You're ready to apply for open positions.</p>
            </div>
          </CardContent>
        </Card>
      )}
      <ProfileForm profile={profile} onSave={saveProfile} onUseSample={!isEmploymentProfileComplete ? loadDemoProfile : undefined} />
    </div>
  );
}
