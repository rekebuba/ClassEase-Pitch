import { Layout } from "@/components";
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
        <Layout role="teacher">
            <TeacherStudentList />
        </Layout>
    );
};

export default TeacherManageStudent;
