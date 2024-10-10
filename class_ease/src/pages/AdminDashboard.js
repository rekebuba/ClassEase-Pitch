import React, { useState, useEffect } from "react";
import {
  FaUserGraduate,
  FaChalkboardTeacher,
  FaCog,
  FaChartBar,
  FaSignOutAlt
} from "react-icons/fa";
import "./styles/AdminDashboard.css";

const AdminDashboard = () => {
  return (
    <div className="admin-dashboard-container">
      <aside className="admin-sidebar">
        <div className="admin-profile-section">
          <h3>Admin Panel</h3>
        </div>
        <nav className="admin-menu">
          <ul>
            <li>
              <FaUserGraduate /> Manage Students
            </li>
            <li>
              <FaChalkboardTeacher /> Manage Teachers
            </li>
            <li>
              <FaChartBar /> Reports
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
      <div className="content">
        <main className="admin-content">
          <header className="admin-header">
            <h2>Welcome Admin</h2>
          </header>
          <section className="admin-stats">
            <div className="admin-stat-card">
              <h3>Total Students</h3>
              <p>350</p>
            </div>
            <div className="admin-stat-card">
              <h3>Total Teachers</h3>
              <p>45</p>
            </div>
            <div className="admin-stat-card">
              <h3>Active Classes</h3>
              <p>20</p>
            </div>
          </section>
          <section className="data-management">
            <div className="data-section">
              <h3>Student Data</h3>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>1234</td>
                    <td>John Doe</td>
                    <td>Grade 10</td>
                    <td>
                      <button className="view-btn">View</button>
                    </td>
                  </tr>
                  <tr>
                    <td>5678</td>
                    <td>Jane Smith</td>
                    <td>Grade 9</td>
                    <td>
                      <button className="view-btn">View</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="data-section">
              <h3>Teacher Data</h3>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Subject</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>9876</td>
                    <td>Mr. Anderson</td>
                    <td>Mathematics</td>
                    <td>
                      <button className="view-btn">View</button>
                    </td>
                  </tr>
                  <tr>
                    <td>5432</td>
                    <td>Ms. Thompson</td>
                    <td>English</td>
                    <td>
                      <button className="view-btn">View</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default AdminDashboard;
