import { createFileRoute } from "@tanstack/react-router";
import { CalendarRange, Clock, Languages, UsersRound } from "lucide-react";

import { ActionFooter } from "@/components/setting/settings-actions";
import { SettingCard, SettingInput, SettingSelect, SettingsPage, SettingsSection, SettingSwitch } from "@/components/setting/settings-section";
import { Badge } from "@/components/ui/badge";

export const Route = createFileRoute("/settings/academic/")({
  component: AcademicSettingsPage,
});

function AcademicSettingsPage() {
  return (
    <SettingsPage title="Academic" description="Set calendar structure, attendance policy, class timing, and localization defaults used across academic operations.">
      <SettingsSection title="Academic Calendar" description="Static school-year configuration for term planning and report scheduling.">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <SettingInput label="Current Academic Year" value="2026" disabled helper="Display only until wired to the backend academic year service." />
          <SettingSelect label="Semester System" value="Trimester" options={["Semester", "Trimester", "Quarter", "Custom terms"]} />
          <SettingSelect label="Grading Periods" value="3 formal grading periods" options={["2 formal grading periods", "3 formal grading periods", "4 formal grading periods", "Monthly continuous assessment"]} />
          <SettingSelect label="Attendance Tracking" value="Daily and period-based" options={["Daily only", "Period-based only", "Daily and period-based", "Disabled"]} />
        </div>
      </SettingsSection>

      <SettingsSection title="Class Period Configuration" description="Define normal school hours and classroom scheduling constraints.">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <SettingInput label="School Start Time" type="time" value="07:45" />
          <SettingInput label="School End Time" type="time" value="16:10" />
          <SettingSelect label="Weekend Days" value="Saturday and Sunday" options={["Saturday and Sunday", "Friday and Saturday", "Sunday only", "Custom"]} />
          <SettingInput label="Maximum Class Size" type="number" value="42" helper="Warning threshold for new enrollment workflows." />
        </div>
      </SettingsSection>

      <SettingsSection title="Promotion Rules" description="Placeholder values for automatic eligibility and progression review.">
        <div className="grid gap-4 lg:grid-cols-3">
          <SettingCard icon={UsersRound} title="Promotion eligibility" description="Students must satisfy minimum score and attendance requirements." badge="Review required">
            <div className="grid gap-3 sm:grid-cols-2">
              <SettingInput label="Passing Score" value="50" />
              <SettingInput label="Attendance minimum" value="85%" />
            </div>
          </SettingCard>
          <SettingCard icon={CalendarRange} title="Term rollover" description="Academic rollover is currently represented as a disabled static action." badge="Static">
            <SettingSwitch label="Auto-create next term" description="Prepare next term shells during year rollover." checked disabled />
          </SettingCard>
          <SettingCard icon={Clock} title="Late enrollment" description="Controls how mid-term student joins are treated in attendance and assessment." badge="Policy">
            <SettingSelect label="Default rule" value="Pro-rate attendance" options={["Pro-rate attendance", "Require administrator review", "Mark as full-term", "Exclude until next term"]} />
          </SettingCard>
        </div>
      </SettingsSection>

      <SettingsSection title="Localization Defaults" description="Regional preferences used by finance, reports, attendance, and communication surfaces.">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <SettingSelect label="Default Language" value="English" options={["English", "Kiswahili", "French", "Arabic"]} />
          <SettingSelect label="Timezone" value="Africa/Nairobi" options={["Africa/Nairobi", "Africa/Kampala", "Africa/Dar_es_Salaam", "UTC"]} />
          <SettingSelect label="Currency" value="KES" options={["KES", "USD", "UGX", "TZS"]} />
          <SettingSelect label="Date Format" value="DD MMM YYYY" options={["DD MMM YYYY", "DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"]} />
        </div>
        <div className="mt-4 rounded-2xl border bg-muted/20 p-4">
          <div className="flex items-center gap-2 text-sm font-medium">
            <Languages className="size-4" />
            {" "}
            Preview
          </div>
          <p className="mt-2 text-sm text-muted-foreground">Thursday, 06 Aug 2026 at 07:45 EAT · KES 12,500.00</p>
        </div>
      </SettingsSection>

      <div className="rounded-2xl border bg-background p-5 shadow-sm">
        <div className="flex flex-wrap gap-2">
          {["Calendar locked", "Attendance enabled", "Trimester", "Promotion review", "Africa/Nairobi"].map(label => <Badge key={label} variant="secondary">{label}</Badge>)}
        </div>
      </div>

      <ActionFooter />
    </SettingsPage>
  );
}
