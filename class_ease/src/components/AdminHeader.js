import {
    FaHome,
    FaUserGraduate,
    FaChalkboardTeacher,
    FaCog,
    FaCogs,
    FaChartBar,
    FaUsers,
    FaUserTie,
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
    FaUserTag,
    FaKey,
    FaDatabase,
    FaCalendarCheck,
    FaPlusCircle,
    FaEdit,
    FaRegCalendarAlt
} from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import React from "react";

const AdminHeader = () => {
    const navigate = useNavigate();

    const manageStudents = e => {
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

    const studentPerformance = e => {
        navigate("/admin/students/performance")
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

    const assignTeacher = e => {
        navigate("/admin/assign/teachers");
    }

    const dataExportImport = e => {
        navigate("/admin/settings/importexport")
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
                        <div className="dropdown-item" onClick={assignTeacher}><FaChalkboard /> Assign Teachers</div>
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
                        <div className="dropdown-item" onClick={studentPerformance}><FaChartPie /> Student Performance Report</div>
                        <div className="dropdown-item"><FaFileInvoice /> Attendance Reports</div>
                        <div className="dropdown-item"><FaFileContract /> Exam Reports</div>
                    </div>
                </div>
                <div className="nav-item dropdown">
                    <span className="nav-link">
                        <FaCog /> Settings
                    </span>
                    <div className="dropdown-content">
                        <div className="dropdown-item"><FaCogs /> System Settings</div>
                        <div className="dropdown-item"><FaUserTag /> User Roles</div>
                        <div className="dropdown-item"><FaKey /> Access Control</div>
                        <div className="dropdown-item"><FaDatabase /> Backup & Restore</div>
                    </div>
                </div>
            </div>
        </header>
    )
}

export default AdminHeader;
