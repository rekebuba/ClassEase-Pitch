import { TeacherLayout } from "@/components/layout";
import { TeacherStudentList } from "@/features/teacher";
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
        <TeacherLayout>
            <TeacherStudentList />
        </TeacherLayout>
    );
};

export default TeacherManageStudent;
