import { createFileRoute } from "@tanstack/react-router";
import { Mail, MapPin, Phone, UserRound } from "lucide-react";

import { ActionFooter } from "@/components/setting/settings-actions";
import {
  DangerZone,
  FieldHelp,
  LoadingPreview,
  SettingInput,
  SettingsPage,
  SettingsSection,
  StaticAlerts,
} from "@/components/setting/settings-section";

export const Route = createFileRoute("/settings/general/")({
  component: GeneralSettingsPage,
});

function GeneralSettingsPage() {
  return (
    <SettingsPage title="General" description="Manage the core school profile shown across student records, reports, invoices, and parent communication.">
      <StaticAlerts />

      <SettingsSection title="School Identity" description="These details appear on dashboards, documents, and official school records." action={<FieldHelp>Keep the school code short; it is often used in exports and references.</FieldHelp>}>
        <div className="grid gap-4 md:grid-cols-2">
          <SettingInput label="School name" value="Evergreen Heights Academy" helper="Public-facing name used throughout the system." counter="26 / 80" />
          <SettingInput label="Registration number" value="EDU-KE-1938-4471" helper="Government or district registration identifier." />
          <SettingInput label="School code" value="EHA" helper="Short code used on reports and internal records." error="Preview validation: code should remain unique." />
          <SettingInput label="Motto" value="Knowledge, Character, Service" counter="28 / 120" />
          <div className="md:col-span-2">
            <SettingInput label="Description" value="A co-educational day school focused on academic excellence, inclusive leadership, and modern digital learning." counter="112 / 240" />
          </div>
        </div>
      </SettingsSection>

      <SettingsSection title="Contact Information" description="Primary communication channels for guardians, staff, and official documents.">
        <div className="grid gap-4 md:grid-cols-3">
          <SettingInput label="Email" type="email" value="admin@evergreenheights.ac.ke" helper="Used as the default reply-to address." />
          <SettingInput label="Phone" value="+254 700 482 915" />
          <SettingInput label="Alternate phone" value="+254 711 204 880" disabled helper="Disabled example for locked district-managed fields." />
          <SettingInput label="Website" value="https://evergreenheights.ac.ke" />
        </div>
      </SettingsSection>

      <SettingsSection title="Address" description="Location data used on official printouts and regional reporting.">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <SettingInput label="Country" value="Kenya" />
          <SettingInput label="Region" value="Nairobi County" />
          <SettingInput label="City" value="Nairobi" />
          <SettingInput label="Postal code" value="00100" />
          <div className="lg:col-span-4">
            <SettingInput label="Full address" value="Mamlaka Road, Upper Hill, Nairobi" helper="Shown on report cards, transcripts, invoices, and exported letters." />
          </div>
        </div>
      </SettingsSection>

      <SettingsSection title="Principal Information" description="Named contact used on approvals, certificates, and formal correspondence.">
        <div className="grid gap-4 md:grid-cols-3">
          <SettingInput label="Principal name" value="Dr. Miriam Otieno" />
          <SettingInput label="Principal email" type="email" value="principal@evergreenheights.ac.ke" />
          <SettingInput label="Principal phone" value="+254 722 315 640" />
        </div>
        <div className="mt-4 grid gap-3 md:grid-cols-3">
          {[{ icon: UserRound, label: "Profile owner", value: "Principal office" }, { icon: Mail, label: "Signature email", value: "principal@evergreenheights.ac.ke" }, { icon: Phone, label: "Escalation line", value: "+254 722 315 640" }, { icon: MapPin, label: "Campus", value: "Main campus" }].map(item => (
            <div key={item.label} className="flex items-center gap-3 rounded-2xl border bg-muted/20 p-4">
              <item.icon className="size-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">{item.label}</p>
                <p className="text-sm font-medium">{item.value}</p>
              </div>
            </div>
          ))}
        </div>
      </SettingsSection>

      <SettingsSection title="Interface States" description="Static examples for loading and helper states that can be reused when backend integration starts.">
        <LoadingPreview />
      </SettingsSection>

      <SettingsSection title="Danger Zone" description="Destructive workspace actions require explicit backend confirmation.">
        <DangerZone />
      </SettingsSection>

      <ActionFooter />
    </SettingsPage>
  );
}
