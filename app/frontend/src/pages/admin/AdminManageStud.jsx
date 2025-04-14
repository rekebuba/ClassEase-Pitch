import { Layout } from "@/components/layout";
import { AdminStudentList } from "@/features/admin";


/**
 * AdminManageStudents component manages the state and behavior for the admin's student management interface.
 * 
 * @description
 * This component handles the following functionalities:
 * - Toggling the visibility of the student profile and assessment popups.
 * - Managing the state for student profile and assessment summaries.
 * 
 * @component {AdminHeader} - Renders the admin header.
 * @component {AdminPanel} - Renders the admin panel.
 * @component {AdminStudentsList} - Renders the list of students with the ability to toggle profile popup and set profile summary.
 */
const AdminManageStudents = () => {

  return (
    <Layout role="admin">
      <AdminStudentList />
    </Layout>
  );
};

export default AdminManageStudents;
