import {
    FaHome,
    FaCog,
    FaCogs,
    FaFileAlt,
    FaUserGraduate,
} from "react-icons/fa";

import { useNavigate } from "react-router-dom";
import React from "react";

const TeacherHeader = () => {
    const navigate = useNavigate();

    const manageStudents = e => {
        navigate("/teacher/students");
    };

    const goToDashboard = e => {
        navigate("/teacher/dashboard")
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
                        <div className="dropdown-item"><FaCogs /> Update Profile</div>
                    </div>
                </div>
            </div>
        </header>
    )
}

export default TeacherHeader;
