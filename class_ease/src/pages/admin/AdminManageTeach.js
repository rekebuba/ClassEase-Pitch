import React, { useState } from "react";
import "../../styles/AdminManageStudents.css";
import AdminPanel from "../../components/AdminPanel";
import AdminHeader from "../../components/AdminHeader";
import AdminTeachProfile from "./AdminTeachProfile";
import AdminTeachList from "./AdminTeachList";
import AssignTeacher from "./AdminAssignTeacher";

/**
 * AdminManageStudents component manages the state and rendering of the admin panel for managing teachers.
 * 
 * @component
 * @example
 * return (
 *   <AdminManageStudents />
 * )
 * 
 * @returns {JSX.Element} The rendered component.
 * 
 * @description
 * This component handles the state for opening and closing detail and edit profiles of teachers.
 * It also manages the summary data of a selected teacher.
 * 
 * @function
 * @name AdminManageStudents
 * 
 * @property {boolean} isDetailOpen - State to track if the detail profile is open.
 * @property {boolean} isEditOpen - State to track if the edit profile is open.
 * @property {Object} teacherSummary - State to store the summary data of a selected teacher.
 */
const AdminManageStudents = () => {

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
        if (role === 'detail') {
            setIsDetailOpen(!isDetailOpen);
        }
        if (role === 'edit') {
            setIsEditOpen(!isEditOpen);
        }
    };

    /**
     * @method
     * @name toggleDetailProfile
     * @description Closes the detail profile.
     */
    const toggleDetailProfile = () => {
        setIsDetailOpen(false);
    }

    /**
     * @method
     * @name toggleEditProfile
     * @description Closes the edit profile.
     */
    const toggleEditProfile = () => {
        setIsEditOpen(false);
    }

    /**
     * @method
     * @name summary
     * @description Sets the summary data for a selected teacher.
     * @param {Object} data - The summary data of the teacher.
     * @returns {Object} The summary data of the teacher.
     * @example
     * summary({
     *  name: "John Doe",
     *  email: "
     * })
     * 
     */
    const summary = (data) => {
        setTeacherSummary(data);
    }

    return (
        <div className="admin-manage-container">
            <AdminPanel />
            <main className="content">
                <AdminHeader />
                <AdminTeachList toggleDropdown={toggleDropdown} teacherSummary={summary} />
                <AdminTeachProfile isDetailOpen={isDetailOpen} toggleDetailProfile={toggleDetailProfile} teacherData={teacherSummary} />
                <AssignTeacher isEditOpen={isEditOpen} toggleEditProfile={toggleEditProfile} teacherData={teacherSummary} />
            </main>
        </div>
    );
};

export default AdminManageStudents;