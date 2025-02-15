import { AdminHeader, AdminPanel } from "@/components/layout";
import { StudentRegistrationForm } from "@/pages/student";
import { TeacherRegistrationForm } from "@/features/teacher";
import { Toaster } from '@/components/ui/sonner';

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
const AdminEnrollStud = ({ role }) => {

    return (
        <div className="admin-dashboard-container">
            <AdminPanel />
            <div className="content">
                <main className="dashboard-content">
                    <AdminHeader />
                    {role === 'teacher' ? <TeacherRegistrationForm /> : <StudentRegistrationForm role='admin' />
                    }
                    <Toaster />
                </main>
            </div>
        </div>
    );
};


export default AdminEnrollStud;
