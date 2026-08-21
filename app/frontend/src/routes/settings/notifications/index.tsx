import { createFileRoute } from "@tanstack/react-router";
import { BellRing, Mail, Megaphone, MessageSquare, Smartphone } from "lucide-react";

import { ActionFooter } from "@/components/setting/settings-actions";
import { SettingCard, SettingInput, SettingSelect, SettingsPage, SettingsSection, SettingSwitch } from "@/components/setting/settings-section";
import { Badge } from "@/components/ui/badge";

export const Route = createFileRoute("/settings/notifications/")({
  component: NotificationsSettingsPage,
});

function NotificationsSettingsPage() {
  return (
    <SettingsPage title="Notifications" description="Design the communication preferences used for academic, attendance, exam, guardian, teacher, and student notifications.">
      <SettingsSection title="Channels" description="Static channel switches for future notification provider integration.">
        <div className="grid gap-4 md:grid-cols-3">
          <SettingCard icon={Mail} title="Email Notifications" description="Send official updates, reports, and account notices by email." badge="Primary"><SettingSwitch label="Enabled" description="Allow email delivery for enabled templates." checked /></SettingCard>
          <SettingCard icon={MessageSquare} title="SMS Notifications" description="Use SMS for urgent attendance, fee, and emergency alerts."><SettingSwitch label="Enabled" description="SMS provider integration can attach here later." checked /></SettingCard>
          <SettingCard icon={Smartphone} title="Push Notifications" description="Send app notifications to mobile and web users."><SettingSwitch label="Enabled" description="Deliver updates to signed-in app users." /></SettingCard>
        </div>
      </SettingsSection>

      <SettingsSection title="Audience Preferences" description="Control which groups receive different notification classes.">
        <div className="grid gap-4 md:grid-cols-2">
          <SettingSwitch label="Guardian Notifications" description="Send attendance, report card, disciplinary, and fee updates to guardians." checked />
          <SettingSwitch label="Teacher Notifications" description="Notify teachers about schedule changes, assigned classes, and approvals." checked />
          <SettingSwitch label="Student Notifications" description="Send timetable, exam, assignment, and announcement updates to students." checked />
          <SettingSwitch label="Report Card Notifications" description="Notify guardians and students when report cards are published." checked />
          <SettingSwitch label="Attendance Alerts" description="Send immediate absence and late-arrival alerts to guardians." checked badge="Urgent" />
          <SettingSwitch label="Exam Alerts" description="Remind students and guardians about upcoming exams and published marks." checked />
        </div>
      </SettingsSection>

      <SettingsSection title="Announcement Preferences" description="Templates and defaults for broad school announcements.">
        <div className="grid gap-4 lg:grid-cols-3">
          <SettingCard icon={Megaphone} title="Announcement routing" description="Default recipients for school-wide notices.">
            <div className="space-y-3">
              <SettingSwitch label="Send to guardians" description="Guardians receive high-priority announcements." checked />
              <SettingSwitch label="Send to staff" description="All active staff receive school announcements." checked />
              <SettingSwitch label="Send to students" description="Students receive age-appropriate notices." />
            </div>
          </SettingCard>
          <SettingCard icon={BellRing} title="Digest Frequency" description="Bundle lower-priority updates into a scheduled digest.">
            <div className="space-y-3">
              <SettingSelect label="Guardian digest" value="Daily at 6:00 PM" options={["Immediate", "Daily at 6:00 PM", "Weekly Monday", "Disabled"]} />
              <SettingSelect label="Teacher digest" value="Daily at 7:00 AM" options={["Immediate", "Daily at 7:00 AM", "Weekly Monday", "Disabled"]} />
            </div>
          </SettingCard>
          <SettingCard icon={Mail} title="Email Template Defaults" description="Reusable sender identity for notification templates.">
            <div className="space-y-3">
              <SettingInput label="Sender name" value="Evergreen Heights Academy" />
              <SettingInput label="Footer text" value="You are receiving this because you are connected to Evergreen Heights Academy." counter="86 / 160" />
            </div>
          </SettingCard>
        </div>
      </SettingsSection>

      <div className="rounded-2xl border bg-background p-5 shadow-sm">
        <p className="text-sm font-medium">Notification health preview</p>
        <div className="mt-4 flex flex-wrap gap-2">{["Email active", "SMS active", "Push draft", "Attendance urgent", "Daily digest"].map(item => <Badge key={item} variant="secondary">{item}</Badge>)}</div>
      </div>

      <ActionFooter />
    </SettingsPage>
  );
}
