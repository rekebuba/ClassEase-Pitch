import { AdminHeader, AdminPanel } from "@/components/layout";
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
    <div className="min-h-screen flex overflow-hidden flex-col">
      <AdminHeader />
      <div className="flex flex-1 scroll-m-0">
        <AdminPanel />
        <div className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
          <AdminStudentList />
        </div>
      </div>
    </div>
  );
};

export default AdminManageStudents;
