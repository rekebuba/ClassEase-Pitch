import { createFileRoute, Outlet } from "@tanstack/react-router";

import { getYearsOptions } from "@/client/@tanstack/react-query.gen";
import AppHeader from "@/components/layout/header/app-header";
import AppSidebar from "@/components/layout/sidebar/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { requireMembership } from "@/lib/auth/route-guards";
import { can, Permission } from "@/lib/permissions";
import { queryClient } from "@/lib/query-client";

export const Route = createFileRoute("/dashboard")({
  component: RouteComponent,
  beforeLoad: requireMembership,
  loader: async () => {
    if (can(Permission["years:read"])) {
      queryClient.prefetchQuery(getYearsOptions());
    }
  },
});

function RouteComponent() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="flex min-h-screen flex-col w-full overflow-x-hidden">
        <AppHeader />
        <div className="p-4">
          <Outlet />
        </div>
      </div>
    </SidebarProvider>
  );
}
