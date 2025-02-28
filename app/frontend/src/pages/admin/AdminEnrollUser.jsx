import { AdminLayout } from "@/components/layout";
import { StudentRegistrationForm } from "@/pages/student";
import { TeacherRegistrationForm } from "@/features/teacher";

/**
 * AdminEnrollStud component renders the admin dashboard container with the appropriate registration form
 * based on the provided role.
 *
 * @param {Object} props - The component props.
 * @param {string} props.role - The role of the user to be enrolled, either 'teacher' or 'student'.
 *
 * Components:
 * - AdminPanel: Renders the admin panel.
 * - AdminHeader: Renders the admin header.
 * - TeacherRegistrationForm: Renders the registration form for teachers.
 * - StudentRegistrationForm: Renders the registration form for students.
 *
 * @returns {JSX.Element} The rendered component.
 */
const AdminEnrollUser = ({ role }) => {

    return (
        <AdminLayout>
            <div className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                {role === 'teacher' ? <TeacherRegistrationForm /> : <StudentRegistrationForm role='admin' />
                }
            </div>
        </AdminLayout>
    );
};


export default AdminEnrollUser;
