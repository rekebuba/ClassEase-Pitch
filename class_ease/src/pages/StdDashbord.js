import React, { useState, useEffect } from "react";
import { FaBook, FaCalendarAlt, FaUserCircle, FaCog, FaSignOutAlt } from 'react-icons/fa';
import './styles/StudentDashboard.css';


const StudentDashboard = () => {
  return (
    <div className="dashboard-container">
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
      <main className="content">
        <header className="dashboard-header">
          <h2>Welcome Back, John!</h2>
        </header>
        <section className="stats">
          <div className="stat-card">
            <h3>Current GPA</h3>
            <p>3.8</p>
          </div>
          <div className="stat-card">
            <h3>Upcoming Exams</h3>
            <p>3 Next Week</p>
          </div>
          <div className="stat-card">
            <h3>Assignments Due</h3>
            <p>5 This Week</p>
          </div>
        </section>
        <section className="course-list">
          <h3>My Courses</h3>
          <ul>
            <li>Mathematics</li>
            <li>Physics</li>
            <li>Chemistry</li>
            <li>Biology</li>
          </ul>
        </section>
      </main>
    </div>
  );
};
export default StudentDashboard;
