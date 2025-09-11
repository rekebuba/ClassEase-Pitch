import { TeacherTable } from "@/features/admin/tables";
import { useEffect, useState } from "react";
import { toast } from "sonner";
// import Pagination from "../../library/pagination";

/**
 * AdminTeachList Component
 *
 * @component
 * @param {Object} props - The component props.
 * @param {Function} props.toggleDropdown - Function to toggle the dropdown menu.
 * @param {Function} props.teacherSummary - Function to display the teacher summary.
 *
 * @description
 * This component renders a list of teachers with search and pagination functionality.
 * It allows the admin to manage teachers by viewing details or editing their information.
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @example
 * <AdminTeachList toggleDropdown={toggleDropdown} teacherSummary={teacherSummary} />
 */
const AdminTeachList = () => {
  const [allTeacher, setAllStudents] = useState({ teachers: [], meta: {} }); // Store all teachers

  useEffect(() => {
    const handleSearch = async () => {
      try {
        const response = await adminApi.getTeachers();

        const data = {
          teachers: response.data["teachers"],
          meta: response.data["meta"],
        };

        setAllStudents(data); // Store all teachers
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data["error"]
        ) {
          toast.error(error.response.data["error"], {
            description:
              "Please try again later, if the problem persists, contact the administrator.",
            style: { color: "red" },
          });
        } else {
          toast.error("An unexpected error occurred.", {
            description:
              "Please try again later, if the problem persists, contact the administrator.",
            style: { color: "red" },
          });
        }
      }
    };

    handleSearch(); // Fetch the list of Teachers when the component loads
  }, []);

  return (
    <section>
      <TeacherTable data={allTeacher.teachers} />
    </section>
  );
};

export default AdminTeachList;
