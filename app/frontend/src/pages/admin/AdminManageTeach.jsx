import { useState } from "react";
import { AdminHeader, AdminPanel } from "@/components/layout";
import { AdminTeacherProfile, AdminTeacherList, AdminAssignTeacher } from "@/features/admin";
import "../../styles/AdminManageStudents.css";
import { Toaster } from '@/components/ui/sonner';

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
 * @property {Object} teacherSummary - State to store the summary data of a selected teacher.
 */
const AdminManageTeacher = () => {

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
    };

    /**
     * @method
     * @name toggleEditProfile
     * @description Closes the edit profile.
     */
    const toggleEditProfile = () => {
        setIsEditOpen(false);
    };

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
    };

    return (
        <div className="min-h-screen flex overflow-hidden flex-col">
            <AdminHeader />
            <div className="flex flex-1 scroll-m-0">
                <AdminPanel />
                <main className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    <AdminTeacherList toggleDropdown={toggleDropdown} teacherSummary={summary} />
                    <AdminTeacherProfile isDetailOpen={isDetailOpen} toggleDetailProfile={toggleDetailProfile} teacherData={teacherSummary} />
                    <AdminAssignTeacher isEditOpen={isEditOpen} toggleEditProfile={toggleEditProfile} teacherData={teacherSummary} />
                    <Toaster />
                </main>
            </div>
        </div>
    );
};

export default AdminManageTeacher;
