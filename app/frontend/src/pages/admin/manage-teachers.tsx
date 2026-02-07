import { useState } from "react";

import {
  AdminAssignTeacher,
  AdminTeacherList,
} from "@/features/admin";

/**
 * AdminManageTeacher component manages the state and rendering of the admin panel for managing teachers.
 *
 * @component
 * @example
 * return (
 *   <AdminManageTeacher />
 * )
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @description
 * This component handles the state for opening and closing detail and edit profiles of teachers.
 * It also manages the summary data of a selected teacher.
 *
 * @function
 * @name AdminManageTeacher
 *
 * @property {boolean} isDetailOpen - State to track if the detail profile is open.
 * @property {boolean} isEditOpen - State to track if the edit profile is open.
 * @property {object} teacherSummary - State to store the summary data of a selected teacher.
 */
function AdminManageTeacher() {
  const [isDetailOpen, setIsDetailOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [teacherSummary, setTeacherSummary] = useState({});

  /**
   * @method
   * @name toggleDropdown
   * @description Toggles the dropdown state for detail or edit profiles based on the role.
   * @param {string} role - The role to toggle ('detail' or 'edit').
   */
  const toggleDropdown = (role) => {
    if (role === "detail") {
      setIsDetailOpen(!isDetailOpen);
    }
    if (role === "edit") {
      setIsEditOpen(!isEditOpen);
    }
  };

  /**
   * @method
   * @name toggleEditProfile
   * @description Closes the edit profile.
   */
  const toggleEditProfile = () => {
    setIsEditOpen(false);
  };

  const summary = (data) => {
    setTeacherSummary(data);
  };

  return (
    <>
      <AdminTeacherList
        toggleDropdown={toggleDropdown}
        teacherSummary={summary}
      />
      <AdminAssignTeacher
        isEditOpen={isEditOpen}
        toggleEditProfile={toggleEditProfile}
        teacherData={teacherSummary}
      />
    </>
  );
}

export default AdminManageTeacher;
