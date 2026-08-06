import { createFileRoute } from "@tanstack/react-router";
import { Image, Mail, Printer, Stamp } from "lucide-react";

import { ActionFooter } from "@/components/setting/settings-actions";
import { ColorSwatch, SettingCard, SettingInput, SettingsPage, SettingsSection, SettingSwitch, UploadCard } from "@/components/setting/settings-section";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/settings/branding/")({
  component: BrandingSettingsPage,
});

function BrandingSettingsPage() {
  return (
    <SettingsPage title="Branding" description="Control the visual identity used in the app, emails, report cards, transcripts, certificates, and printed letters.">
      <SettingsSection title="School Assets" description="Upload placeholders show the expected formats. Upload implementation is intentionally disabled.">
        <div className="grid gap-4 md:grid-cols-3">
          <UploadCard title="School logo" description="PNG or SVG, transparent background preferred." value="Current: evergreen-logo.svg" />
          <UploadCard title="Cover image" description="Wide campus image for portals and printable headers." value="Recommended: 1600 x 600 px" aspect="aspect-video" />
          <UploadCard title="Favicon" description="Square icon used in browser tabs and compact app surfaces." value="Current: favicon-32.png" />
        </div>
      </SettingsSection>

      <SettingsSection title="Brand Colors" description="These colors drive theme accents, document headers, badges, and selected controls.">
        <div className="grid gap-4 md:grid-cols-3">
          <ColorSwatch label="Primary color" value="#2563EB" className="bg-blue-600" />
          <ColorSwatch label="Secondary color" value="#0F766E" className="bg-teal-700" />
          <ColorSwatch label="Accent color" value="#F59E0B" className="bg-amber-500" />
        </div>
      </SettingsSection>

      <SettingsSection title="Theme Preview" description="A compact preview of how the selected identity appears in product surfaces and documents.">
        <div className="overflow-hidden rounded-2xl border bg-background">
          <div className="bg-blue-600 p-6 text-white">
            <div className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="flex size-12 items-center justify-center rounded-2xl bg-white/15 text-lg font-semibold">EH</div>
                <div>
                  <p className="font-semibold">Evergreen Heights Academy</p>
                  <p className="text-sm text-blue-100">Knowledge, Character, Service</p>
                </div>
              </div>
              <Badge className="bg-amber-500 text-amber-950 hover:bg-amber-500">Official</Badge>
            </div>
          </div>
          <div className="grid gap-4 p-5 md:grid-cols-3">
            <div className="rounded-xl border p-4">
              <p className="text-sm font-medium">Portal header</p>
              <p className="mt-1 text-xs text-muted-foreground">Primary navigation with school mark.</p>
            </div>
            <div className="rounded-xl border p-4">
              <p className="text-sm font-medium">Report card</p>
              <p className="mt-1 text-xs text-muted-foreground">Colored section labels and footer.</p>
            </div>
            <div className="rounded-xl border p-4">
              <p className="text-sm font-medium">Email template</p>
              <p className="mt-1 text-xs text-muted-foreground">Branded heading and action button.</p>
            </div>
          </div>
        </div>
      </SettingsSection>

      <SettingsSection title="Print and Communication Branding" description="Static configuration for formal documents, printed reports, and outbound email templates.">
        <div className="grid gap-4 lg:grid-cols-2">
          <SettingCard icon={Stamp} title="School Stamp Upload" description="Placeholder for a transparent stamp image used on formal certificates." badge="PNG recommended">
            <UploadCard title="Stamp image" description="Transparent PNG, 600 x 600 px." value="No upload action attached" />
          </SettingCard>
          <SettingCard icon={Image} title="Letterhead Preview" description="Preview the configured logo, seal, address, and principal signature placement.">
            <div className="rounded-xl border bg-white p-5 text-slate-950 shadow-sm">
              <div className="flex items-start justify-between border-b pb-4">
                <div>
                  <p className="font-semibold">Evergreen Heights Academy</p>
                  <p className="text-xs text-slate-500">Mamlaka Road, Upper Hill, Nairobi</p>
                </div>
                <div className="size-12 rounded-xl bg-blue-600 text-center text-sm font-bold leading-[3rem] text-white">EH</div>
              </div>
              <div className="space-y-2 py-5">
                <div className="h-2 w-2/3 rounded bg-slate-200" />
                <div className="h-2 w-full rounded bg-slate-100" />
                <div className="h-2 w-5/6 rounded bg-slate-100" />
              </div>
              <div className="border-t pt-3 text-xs text-slate-500">Principal signature and school stamp area</div>
            </div>
          </SettingCard>
          <SettingCard icon={Mail} title="Email Branding" description="Controls visible identity on guardian, teacher, and student emails.">
            <div className="grid gap-3 sm:grid-cols-2">
              <SettingInput label="Sender name" value="Evergreen Heights Academy" />
              <SettingInput label="Reply-to" value="admin@evergreenheights.ac.ke" />
            </div>
            <div className="mt-3"><SettingSwitch label="Include logo in email header" description="Adds the school logo to notification templates." checked /></div>
          </SettingCard>
          <SettingCard icon={Printer} title="Print Branding" description="Apply brand assets to report cards, transcripts, invoices, and certificates.">
            <div className="space-y-3">
              <SettingSwitch label="Show watermark" description="Use a low-opacity school mark on official PDFs." checked />
              <SettingSwitch label="Use color printing" description="Prefer branded color headings on generated printouts." checked />
              <Button variant="outline" disabled>Preview print packet</Button>
            </div>
          </SettingCard>
        </div>
      </SettingsSection>

      <ActionFooter />
    </SettingsPage>
  );
}
