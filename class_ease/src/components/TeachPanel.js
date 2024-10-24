import {
    FaSignOutAlt,
    FaUserCircle
} from "react-icons/fa";


const TeacherPanel = () => {
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
                        <FaSignOutAlt /> Logout
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

export default TeacherPanel;
