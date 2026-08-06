import { SettingsHeader } from "./settings-header";
import { SettingsSidebar } from "./settings-sidebar";

import type { ReactNode } from "react";

type SettingsLayoutProps = {
  children: ReactNode;
};

export function SettingsLayout({ children }: SettingsLayoutProps) {
  return (
    <main className="w-full bg-muted/20">
      <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-4 py-5 sm:px-6 lg:px-8">
        <SettingsHeader />
        <div className="grid gap-6 lg:grid-cols-[280px_minmax(0,1fr)]">
          <aside className="hidden lg:block">
            <div className="sticky top-20 rounded-2xl border bg-background p-2 shadow-sm">
              <SettingsSidebar />
            </div>
          </aside>
          <section className="min-w-0">{children}</section>
        </div>
      </div>
    </main>
  );
}
