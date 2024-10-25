import { FaSignOutAlt, FaUserCircle } from "react-icons/fa";


const AdminPanel = () => {
    return (
        <aside className="sidebar">
            <div className="profile-section">
                <FaUserCircle className="profile-icon" />
                <h3>Admin Panel</h3>
                <p>Mr. Anderson</p>
                <p>Principal</p>
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

export default AdminPanel;
