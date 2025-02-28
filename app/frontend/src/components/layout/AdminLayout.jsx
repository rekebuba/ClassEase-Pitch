import { Toaster } from "@/components/ui/toaster";
import { AdminHeader, AdminPanel } from "@/components/layout";


export default function AdminLayout({ children }) {
    return (
        <div className="min-h-screen flex overflow-hidden flex-col">
            <AdminHeader />
            <div className="flex flex-1 scroll-m-0">
                <AdminPanel />
                <main className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    {children}
                </main>
                <Toaster />
            </div>
        </div>
    );
}
