import { Toaster } from "@/components/ui/toaster";
import { TeacherHeader, TeacherPanel } from "@/components/layout";


export default function TeacherLayout({ children }) {
    return (
        <div className="min-h-screen flex overflow-hidden flex-col">
            <TeacherHeader />
            <div className="flex flex-1 scroll-m-0">
                <TeacherPanel />
                <main className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    {children}
                </main>
                <Toaster />
            </div>
        </div>
    );
}
