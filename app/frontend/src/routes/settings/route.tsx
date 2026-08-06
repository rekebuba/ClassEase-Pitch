import { createFileRoute, Outlet } from "@tanstack/react-router";

import AppHeader from "@/components/layout/header/app-header";
import AppSidebar from "@/components/layout/sidebar/app-sidebar";
import { SettingsLayout } from "@/components/setting/settings-layout";
import { SidebarProvider } from "@/components/ui/sidebar";
import { requireMembership } from "@/lib/auth/route-guards";

export const Route = createFileRoute("/settings")({
  component: RouteComponent,
  beforeLoad: requireMembership,
});

function RouteComponent() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="flex min-h-screen flex-col w-full overflow-x-hidden">
        <AppHeader />
        <SettingsLayout>
          <Outlet />
        </SettingsLayout>
      </div>
    </SidebarProvider>
  );
}
