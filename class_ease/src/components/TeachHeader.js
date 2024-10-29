import {
    FaHome,
    FaCog,
    FaCogs,
    FaFileAlt,
    FaUserGraduate,
} from "react-icons/fa";
import classEaseHeader from '../images/ClassEase-header.png';
import { useNavigate } from "react-router-dom";
import React from "react";

/**
 * TeacherHeader component renders the header section for the teacher's dashboard.
 * It includes navigation links to the dashboard, student management, and profile update pages.
 *
 * @component
 * @example
 * return (
 *   <TeacherHeader />
 * )
 *
 * @returns {JSX.Element} The rendered header component.
 *
 * @function
 * @name TeacherHeader
 *
 * @description
 * The TeacherHeader component provides navigation options for teachers to manage students,
 * access the dashboard, and update their profile. It uses the `useNavigate` hook from
 * `react-router-dom` to handle navigation.
 */
const TeacherHeader = () => {
    const navigate = useNavigate();

    /**
     * Navigates to the home page.
     *
     * @param {Event} e - The event object.
     */
    const goToHome = e => {
        navigate("/");
    }

    /**
     * @function manageStudents
     * @description Navigates to the student management page.
     */
    const manageStudents = e => {
        navigate("/teacher/students");
    };

    /**
     * @function goToDashboard
     * @description Navigates to the teacher's dashboard.
     */
    const goToDashboard = e => {
        navigate("/teacher/dashboard")
    }

    /**
     * @function updateProfile
     * @description Navigates to the profile update page.
     */
    const updateProfile = e => {
        navigate("/teacher/update/profile")
    }

    return (
        <header className="dashboard-header">
            <div className="header-logo" onClick={goToHome}>
                <img src={classEaseHeader} alt="ClassEase School" />
            </div>
            <div className="dashboard-nav">
                <div className="nav-item">
                    <span className="nav-link" onClick={goToDashboard}>
                        <FaHome /> Home
                    </span>
                </div>
                <div className="nav-item dropdown">
                    <span className="nav-link">
                        <FaFileAlt /> Assessments & Exams
                    </span>
                    <div className="dropdown-content">
                        <div className="dropdown-item" onClick={manageStudents}><FaUserGraduate /> My Students</div>
                    </div>
                </div>
                <div className="nav-item dropdown">
                    <span className="nav-link">
                        <FaCog /> Settings
                    </span>
                    <div className="dropdown-content">
                        <div className="dropdown-item" onClick={updateProfile}><FaCogs /> Update Profile</div>
                    </div>
                </div>
            </div>
        </header>
    )
}

export default TeacherHeader;
