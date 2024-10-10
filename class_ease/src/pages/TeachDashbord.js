import React, { useState, useEffect } from "react";
import {
  FaUserGraduate,
  FaClipboardList,
  FaBookOpen,
  FaCog,
  FaSignOutAlt
} from "react-icons/fa";
import "./styles/TeacherDashboard.css";

const TeacherDashboard = () => {
  return (
    <div className="teacher-dashboard-container">
      <aside className="teacher-sidebar">
        <div className="teacher-profile-section">
          <h3>Teacher Panel</h3>
          <p>Mr. Anderson</p>
          <p>Mathematics Teacher</p>
        </div>
        <nav className="teacher-menu">
          <ul>
            <li>
              <FaUserGraduate /> My Students
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
      <div className="content">
        <main className="teacher-content">
          <header className="teacher-header">
            <h2>Welcome Mr. Anderson</h2>
          </header>
          <section className="teacher-stats">
            <div className="teacher-stat-card">
              <h3>Total Students</h3>
              <p>30</p>
            </div>
            <div className="teacher-stat-card">
              <h3>Pending Assignments</h3>
              <p>5 To Grade</p>
            </div>
          </section>
          <section className="teacher-students">
            <h3>My Students</h3>
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Grade</th>
                  <th>Score</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1234</td>
                  <td>John Doe</td>
                  <td>Grade 10</td>
                  <td>
                    <input
                      type="number"
                      className="score-input"
                      defaultValue="85"
                    />
                  </td>
                  <td>
                    <button className="update-btn">Update</button>
                  </td>
                </tr>
                <tr>
                  <td>5678</td>
                  <td>Jane Smith</td>
                  <td>Grade 10</td>
                  <td>
                    <input
                      type="number"
                      className="score-input"
                      defaultValue="90"
                    />
                  </td>
                  <td>
                    <button className="update-btn">Update</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </section>
          <section className="teacher-assignments">
            <h3>Manage Assignments</h3>
            <div className="assignment-form">
              <input
                type="text"
                placeholder="Assignment Title"
                className="assignment-input"
              />
              <textarea
                placeholder="Assignment Description"
                className="assignment-textarea"
              />
              <button className="create-assignment-btn">
                Create Assignment
              </button>
            </div>
            <div className="assignments-list">
              <h4>Pending Assignments</h4>
              <ul>
                <li>
                  <strong>Algebra Homework</strong> - Due: Oct 15
                  <button className="grade-btn">Grade</button>
                </li>
                <li>
                  <strong>Geometry Quiz</strong> - Due: Oct 17
                  <button className="grade-btn">Grade</button>
                </li>
              </ul>
            </div>
          </section>
        </main>
      </div>
    </div>
  );
};

export default TeacherDashboard;
