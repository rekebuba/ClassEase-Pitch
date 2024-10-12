import {
  FaBook,
  FaCalendarAlt,
  FaUserCircle,
  FaCog,
  FaSignOutAlt
} from "react-icons/fa";

const StudentPanel = () => {
  return (
    <aside className="sidebar">
      <div className="profile-section">
        <FaUserCircle className="profile-icon" />
        <h3>John Doe</h3>
        <p>Grade 10 - Science Stream</p>
      </div>
      <nav className="menu">
        <ul>
          <li>
            <FaBook /> My Courses
          </li>
          <li>
            <FaCalendarAlt /> Schedule
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


export default StudentPanel;
