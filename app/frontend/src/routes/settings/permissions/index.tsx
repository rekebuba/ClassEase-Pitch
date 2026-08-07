import { createFileRoute } from "@tanstack/react-router";
import { Fingerprint, KeyRound, LockKeyhole, MonitorCheck, Shield, UserCog, UsersRound } from "lucide-react";

import { ActionFooter } from "@/components/setting/settings-actions";
import { SettingCard, SettingInput, SettingSelect, SettingsPage, SettingsSection, SettingSwitch } from "@/components/setting/settings-section";
import { Badge } from "@/components/ui/badge";

export const Route = createFileRoute("/settings/permissions/")({
  component: PermissionsSettingsPage,
});

function PermissionsSettingsPage() {
  return (
    <SettingsPage title="Permissions" description="Informational access-control settings for roles, security posture, sessions, password policy, and audit visibility.">
      <div className="grid gap-4 lg:grid-cols-2">
        <SettingCard icon={UsersRound} title="Roles" description="Role groups available for staff, teachers, students, guardians, and administrators." badge="8 roles">
          <div className="flex flex-wrap gap-2">{["Owner", "Principal", "Registrar", "Teacher", "Accountant", "Librarian", "Guardian", "Student"].map(role => <Badge key={role} variant="secondary">{role}</Badge>)}</div>
        </SettingCard>
        <SettingCard icon={KeyRound} title="Permissions" description="Fine-grained module access is summarized here for later backend binding." badge="Read only">
          <div className="grid gap-2 sm:grid-cols-2">
            <SettingSwitch label="Academic records" description="Read and edit student academic records." checked />
            <SettingSwitch label="Finance records" description="Restrict fee and invoice access." checked />
          </div>
        </SettingCard>
        <SettingCard icon={Shield} title="Security" description="Core account protection rules for sensitive school operations." badge="Strong">
          <SettingSwitch label="Require secure sessions" description="Block access from unknown devices after risk review." checked />
        </SettingCard>
        <SettingCard icon={MonitorCheck} title="Session Settings" description="Session duration and device policy used by authenticated users.">
          <div className="grid gap-3 sm:grid-cols-2">
            <SettingSelect label="Session timeout" value="8 hours" options={["2 hours", "4 hours", "8 hours", "12 hours"]} />
            <SettingInput label="Maximum devices" value="3" />
          </div>
        </SettingCard>
        <SettingCard icon={LockKeyhole} title="Password Policy" description="Password complexity expectations shown to school administrators.">
          <div className="space-y-3">
            <SettingInput label="Minimum length" value="12" />
            <SettingSwitch label="Require symbols" description="Passwords must include at least one symbol." checked />
            <SettingSwitch label="Expire passwords" description="Prompt staff to rotate passwords every 180 days." />
          </div>
        </SettingCard>
        <SettingCard icon={Fingerprint} title="MFA" description="Multi-factor authentication availability for privileged staff." badge="Recommended">
          <div className="space-y-3">
            <SettingSwitch label="Require MFA for administrators" description="Protect owner, principal, and registrar accounts." checked />
            <SettingSwitch label="Allow authenticator apps" description="Use TOTP-compatible apps for verification." checked />
          </div>
        </SettingCard>
        <SettingCard icon={UserCog} title="Login Restrictions" description="Static policy controls for location, time, and device access.">
          <div className="space-y-3">
            <SettingSwitch label="Restrict staff login hours" description="Allow administrative access only during school-approved windows." />
            <SettingSwitch label="Flag foreign logins" description="Add risk flags for unusual login countries." checked />
          </div>
        </SettingCard>
        <SettingCard icon={Shield} title="Audit Access" description="Defines who can view security and configuration activity.">
          <div className="space-y-3">
            <SettingSwitch label="Owner can view all logs" description="Owners see full audit details." checked disabled badge="Locked" />
            <SettingSwitch label="Principal can export logs" description="Allow principal-level audit exports." checked />
          </div>
        </SettingCard>
      </div>

      <SettingsSection title="Permission Matrix Preview" description="Compact static matrix for common modules and role access levels.">
        <div className="overflow-x-auto rounded-2xl border">
          <table className="w-full min-w-160 text-sm">
            <thead className="bg-muted/60 text-muted-foreground"><tr>{["Module", "Owner", "Principal", "Teacher", "Guardian"].map(head => <th key={head} className="px-4 py-3 text-left font-medium">{head}</th>)}</tr></thead>
            <tbody>{[["Students", "Full", "Full", "Limited", "Own child"], ["Grades", "Full", "Approve", "Edit assigned", "View"], ["Finance", "Full", "View", "None", "Own invoices"], ["Settings", "Full", "Limited", "None", "None"]].map(row => <tr key={row[0]} className="border-t">{row.map(cell => <td key={cell} className="px-4 py-3">{cell}</td>)}</tr>)}</tbody>
          </table>
        </div>
      </SettingsSection>

      <ActionFooter disabled saveLabel="Save policy" />
    </SettingsPage>
  );
}
