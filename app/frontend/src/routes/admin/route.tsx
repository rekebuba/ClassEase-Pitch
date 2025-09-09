import {
  getAdminBasicInfoOptions,
  getYearsOptions,
} from "@/client/@tanstack/react-query.gen";
import AdminHeader from "@/components/layout/header/admin-header";
import AdminSidebar from "@/components/layout/sidebar/admin-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { queryClient } from "@/lib/query-client";
import { createFileRoute, Outlet } from "@tanstack/react-router";

export const Route = createFileRoute("/admin")({
  component: RouteComponent,
  loader: async () => {
    await queryClient.ensureQueryData(getAdminBasicInfoOptions());
    await queryClient.ensureQueryData(getYearsOptions());
  },
});

function RouteComponent() {
  return (
    <SidebarProvider>
      <AdminSidebar />
      <div className="flex min-h-screen flex-col w-full overflow-x-hidden">
        <AdminHeader />
        <div className="p-4">
          <Outlet />
        </div>
      </div>
    </SidebarProvider>
  );
}
