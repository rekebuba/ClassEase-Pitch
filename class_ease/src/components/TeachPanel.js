import {
    FaUserGraduate,
    FaClipboardList,
    FaBookOpen,
    FaCog,
    FaSignOutAlt,
    FaUserCircle
} from "react-icons/fa";
import { useNavigate } from "react-router-dom";


const TeacherPanel = () => {
    const navigate = useNavigate();

    const manageStudents = e => {
        navigate("/teacher/students");
    };

    return (
        <aside className="sidebar">
            <div className="profile-section">
                <FaUserCircle className="profile-icon" />
                <h3>Teacher Panel</h3>
                <p>Mr. Anderson</p>
                <p>Mathematics Teacher</p>
            </div>
            <nav className="menu">
                <ul>
                    <li>
                        <FaUserGraduate onClick={manageStudents} /> My Students
                    </li>
                    <li>
                        <FaClipboardList /> Manage Scores
                    </li>
                    <li>
                        <FaBookOpen /> Assignments
                    </li>
                    <li>
                        <FaCog /> Settings
                    </li>
                    <li>
                        <FaSignOutAlt /> Logout
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

export default TeacherPanel;
