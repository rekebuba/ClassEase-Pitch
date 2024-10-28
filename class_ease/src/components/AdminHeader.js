import {
    FaHome,
    FaUserGraduate,
    FaChalkboardTeacher,
    FaCog,
    FaCogs,
    FaChartBar,
    FaUsers,
    FaUserShield,
    FaBookOpen,
    FaBuilding,
    FaBook,
    FaChalkboard,
    FaUserPlus,
    FaCalendarAlt,
    FaFileAlt,
    FaBookReader,
    FaFileSignature,
    FaGraduationCap,
    FaPenAlt,
    FaChartPie,
    FaFileInvoice,
    FaFileContract,
    FaCalendarCheck,
    FaPlusCircle,
    FaEdit,
    FaRegCalendarAlt
} from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import React from "react";

/**
 * AdminHeader component renders the header section of the admin dashboard.
 * It includes navigation links for various administrative tasks such as 
 * managing students and teachers, creating events, and accessing reports.
 * 
 * @component
 * @example
 * return (
 *   <AdminHeader />
 * )
 * 
 * @returns {JSX.Element} The rendered header component for the admin dashboard.
 * 
 * @function
 * @name AdminHeader
 * 
 * @description
 * The AdminHeader component provides a set of navigation links organized into 
 * dropdown menus. Each link triggers a navigation action to a different part 
 * of the admin interface. The component uses the `useNavigate` hook from 
 * `react-router-dom` to handle navigation.
 * 
 * @property {function} manageStudents - Navigates to the student management page.
 * @property {function} manageTeachers - Navigates to the teacher management page.
 * @property {function} assessMarkList - Navigates to the mark list assessment page.
 * @property {function} createEvent - Navigates to the new event creation page.
 * @property {function} goToDashboard - Navigates to the admin dashboard.
 * @property {function} userAccessControl - Navigates to the user access control page.
 * @property {function} enrollStudent - Navigates to the student enrollment page.
 * @property {function} enrollTeacher - Navigates to the teacher registration page.
 * @property {function} updateProfile - Navigates to the profile update page.
 */
const AdminHeader = () => {
    const navigate = useNavigate();

    const manageStudents = () => {
        navigate("/admin/manage/students");
    }

    const manageTeachers = e => {
        navigate("/admin/manage/teachers");
    }

    const assessMarkList = e => {
        navigate("/admin/assessment/marklist");
    }

    const createEvent = e => {
        navigate("/admin/events/newevent")
    }

    const goToDashboard = e => {
        navigate("/admin/dashboard")
    }

    const userAccessControl = e => {
        navigate("/admin/users/accesscontrol")
    }

    const enrollStudent = e => {
        navigate("/admin/student/registration")
    }

    const enrollTeacher = e => {
        navigate("/admin/teacher/registration")
    }

    const updateProfile = e => {
        navigate("/admin/update/profile")
    }

    return (
        <header className="dashboard-header">
            <div className="dashboard-logo">ClassEase School</div>
            <div className="dashboard-nav">
                <div className="nav-item">
                    <span className="nav-link" onClick={goToDashboard}>
                        <FaHome /> Home
                    </span>
                </div>
                <div className="nav-item dropdown">
                    <span className="nav-link">
                        <FaUsers /> User Management
                    </span>
                    <div className="dropdown-content">
                        <div className="dropdown-item" onClick={manageStudents}><FaUserGraduate /> Manage Students</div>
                        <div className="dropdown-item" onClick={manageTeachers}><FaChalkboardTeacher /> Manage Teachers</div>
                        <div className="dropdown-item" onClick={enrollStudent}><FaUserPlus /> Enroll Students</div>
                        <div className="dropdown-item" onClick={enrollTeacher}><FaUserPlus /> Register Teacher</div>
                        <div className="dropdown-item" onClick={userAccessControl}><FaUserShield /> Roles & Permissions</div>
                    </div>
                </div>
                <div className="nav-item dropdown">
                    <span className="nav-link">
                        <FaBookOpen /> Classes & Subjects
                    </span>
                    <div className="dropdown-content">
                        <div className="dropdown-item"><FaBuilding /> Class Management</div>
                        <div className="dropdown-item"><FaBook /> Subject Management</div>
                        <div className="dropdown-item"><FaChalkboard /> Assign Teachers</div>
                        <div className="dropdown-item"><FaCalendarAlt /> Timetable Setup</div>
                    </div>
                </div>
                <div className="nav-item dropdown">
                    <span className="nav-link">
                        <FaFileAlt /> Assessments & Exams
                    </span>
                    <div className="dropdown-content">
                        <div className="dropdown-item" onClick={assessMarkList}><FaBookReader /> Create Mark List</div>
                        <div className="dropdown-item"><FaFileSignature /> Manage Tests & Quizzes</div>
                        <div className="dropdown-item"><FaPenAlt /> Manage Midterm Exams</div>
                        <div className="dropdown-item"><FaGraduationCap /> Manage Final Exams</div>
                    </div>
                </div>
                <div className="nav-item dropdown">
                    <span className="nav-link">
                        <FaCalendarCheck /> Events & Activities
                    </span>
                    <div className="dropdown-content">
                        <div className="dropdown-item" onClick={createEvent}><FaPlusCircle /> Create New Event</div>
                        <div className="dropdown-item"><FaEdit /> Manage Events</div>
                        <div className="dropdown-item"><FaRegCalendarAlt /> Event Calendar</div>
                    </div>
                </div>
                <div className="nav-item dropdown">
                    <span className="nav-link">
                        <FaChartBar /> Report
                    </span>
                    <div className="dropdown-content">
                        <div className="dropdown-item"><FaChartPie /> Student Performance Report</div>
                        <div className="dropdown-item"><FaFileInvoice /> Attendance Reports</div>
                        <div className="dropdown-item"><FaFileContract /> Exam Reports</div>
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

export default AdminHeader;
