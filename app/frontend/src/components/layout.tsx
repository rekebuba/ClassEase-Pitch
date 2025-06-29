import { Toaster } from "@/components/ui/toaster";
import { AppSidebar } from "@/components/app-sidebar";
import { Header } from "@/components/Header"

import { SidebarProvider } from "@/components/ui/sidebar"
import { RoleProps } from "@/lib/types";

export default function Layout({ role, children }: { role: RoleProps; children: React.ReactNode }) {
    return (
        <SidebarProvider>
            <AppSidebar role={role} />
            <div className="flex min-h-screen flex-col w-full overflow-x-hidden">
                <Header />
                <div className="p-0">
                    {children}
                </div>
            </div>
        </SidebarProvider>
    );
}
