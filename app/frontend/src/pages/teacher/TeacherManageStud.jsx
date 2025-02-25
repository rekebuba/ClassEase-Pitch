import { TeacherHeader, TeacherPanel } from "@/components/layout";
import { TeacherStudentList } from "@/features/teacher";
import { Toaster } from '@/components/ui/sonner';
import "../../styles/AdminManageStudents.css";


/**
 * TeacherManageStudents component
 * @component
 * @return {component} TeacherManageStudents
 * @example
 * return <TeacherManageStudents />
 */
const TeacherManageStudent = () => {
    return (
        <div className="min-h-screen flex overflow-hidden flex-col">
            <TeacherPanel />
            <div className="flex flex-1 scroll-m-0">
                <TeacherHeader />
                <main className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    <TeacherStudentList />
                    <Toaster />
                </main>
            </div>
        </div>
    );
};

export default TeacherManageStudent;
