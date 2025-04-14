import { Toaster } from "@/components/ui/toaster";
import { AppSidebar } from "@/components/layout/app-sidebar";
import { Header } from "@/components/layout/Header"

import { SidebarProvider } from "@/components/ui/sidebar"

export default function Layout({ role, children }) {
    return (
        <SidebarProvider>
            <AppSidebar role={role} />
            <div className="flex min-h-screen flex-col w-full">
                <Header />
                <div className="p-5">
                    {children}
                </div>
            </div>
        </SidebarProvider>
    );
}
