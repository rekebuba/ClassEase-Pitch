import { Toaster } from "@/components/ui/toaster";
import { StudentHeader, StudentPanel } from "@/components/layout";


export default function StudentLayout({ children }) {
    return (
        <div className="min-h-screen flex overflow-hidden flex-col">
            <StudentHeader />
            <div className="flex flex-1 scroll-m-0">
                <StudentPanel />
                <main className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    {children}
                </main>
                <Toaster />
            </div>
        </div>
    );
}
