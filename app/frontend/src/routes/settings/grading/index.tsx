import { createFileRoute } from "@tanstack/react-router";
import { Award, BarChart3, FileText, Percent } from "lucide-react";

import { ActionFooter } from "@/components/setting/settings-actions";
import { SettingCard, SettingInput, SettingSelect, SettingsPage, SettingsSection, SettingSwitch } from "@/components/setting/settings-section";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

export const Route = createFileRoute("/settings/grading/")({
  component: GradingSettingsPage,
});

const gradeScale = [
  { grade: "A", range: "80 - 100", remark: "Excellent" },
  { grade: "B", range: "70 - 79", remark: "Very good" },
  { grade: "C", range: "60 - 69", remark: "Good" },
  { grade: "D", range: "50 - 59", remark: "Pass" },
  { grade: "E", range: "0 - 49", remark: "Below standard" },
];

function GradingSettingsPage() {
  return (
    <SettingsPage title="Grading" description="Configure grade boundaries, ranking visibility, GPA display, report defaults, and promotion criteria.">
      <SettingsSection title="Grade Boundaries" description="Static score boundaries used for previews, transcripts, and report card display.">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <SettingInput label="Passing Grade" value="D" />
          <SettingInput label="Highest Grade" value="A" />
          <SettingInput label="Lowest Grade" value="E" />
          <SettingSelect label="Decimal Precision" value="1 decimal place" options={["Whole number", "1 decimal place", "2 decimal places"]} />
        </div>
      </SettingsSection>

      <SettingsSection title="Grade Scale" description="Visible grading rubric for academic reports and teacher mark entry screens.">
        <div className="overflow-hidden rounded-2xl border">
          {gradeScale.map((item, index) => (
            <div key={item.grade} className="grid grid-cols-[80px_1fr_1fr] items-center gap-4 px-4 py-3 text-sm odd:bg-muted/30">
              <Badge className="w-fit">{item.grade}</Badge>
              <span className="font-medium">{item.range}</span>
              <span className="text-muted-foreground">{item.remark}</span>
              {index < gradeScale.length - 1 ? null : null}
            </div>
          ))}
        </div>
      </SettingsSection>

      <SettingsSection title="Ranking and Calculation" description="These static switches model gradebook behavior without connecting to any backend service.">
        <div className="grid gap-4 md:grid-cols-2">
          <SettingSwitch label="Auto Ranking" description="Automatically calculate class and stream position after marks are finalized." checked />
          <SettingSwitch label="Show Rank" description="Display student position on report cards and guardian portals." checked />
          <SettingSwitch label="Show GPA" description="Show GPA beside percentage scores where applicable." />
          <SettingSwitch label="Weighting Enabled" description="Use component weights for exams, assignments, projects, and participation." checked />
        </div>
      </SettingsSection>

      <SettingsSection title="Assessment Defaults" description="Default weighting and behavior for new assessment components.">
        <div className="grid gap-4 lg:grid-cols-3">
          <SettingCard icon={Percent} title="Default weights" description="Common distribution for a term with continuous assessment and final exam.">
            <div className="space-y-3">
              <SettingInput label="CAT / assignments" value="40%" />
              <SettingInput label="Final exam" value="60%" />
            </div>
          </SettingCard>
          <SettingCard icon={FileText} title="Report Card Options" description="Controls what appears in generated student report cards.">
            <div className="space-y-3">
              <SettingSwitch label="Teacher comments" description="Allow subject and class teacher comments." checked />
              <SettingSwitch label="Attendance summary" description="Show attendance rate and absence count." checked />
            </div>
          </SettingCard>
          <SettingCard icon={Award} title="Transcript Options" description="Long-term academic record display preferences.">
            <div className="space-y-3">
              <SettingSwitch label="Show cumulative average" description="Display aggregate performance across academic years." checked />
              <SettingSwitch label="Include behavior notes" description="Attach conduct summaries where approved." />
            </div>
          </SettingCard>
        </div>
      </SettingsSection>

      <SettingsSection title="Promotion Criteria" description="Rules used to flag students for progression review at year-end.">
        <div className="grid gap-4 md:grid-cols-3">
          <SettingInput label="Minimum average" value="50%" />
          <SettingInput label="Maximum failed subjects" value="2" />
          <SettingInput label="Required attendance" value="85%" />
        </div>
        <Separator className="my-5" />
        <div className="grid gap-4 md:grid-cols-2">
          <SettingSwitch label="Require principal approval" description="Hold promoted records until administrator approval." checked />
          <SettingSwitch label="Notify guardians" description="Send promotion result notifications after publishing." checked disabled badge="Locked" />
        </div>
      </SettingsSection>

      <div className="rounded-2xl border bg-background p-5 shadow-sm">
        <div className="flex items-center gap-2 text-sm font-medium">
          <BarChart3 className="size-4" />
          {" "}
          Grade distribution preview
        </div>
        <div className="mt-4 grid h-36 grid-cols-5 items-end gap-3">
          {[82, 74, 66, 48, 22].map((height, index) => (
            <div key={height} className="rounded-t-xl bg-primary/80" style={{ height: `${height}%` }}>
              <span className="sr-only">
                Bar
                {" "}
                {index + 1}
              </span>

            </div>
          ))}
        </div>
      </div>

      <ActionFooter />
    </SettingsPage>
  );
}
