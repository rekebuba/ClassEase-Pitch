import React, { useState, useEffect } from "react";
import TeacherPanel from "../components/TeachPanel";
import "./styles/TeacherDashboard.css";
import "./styles/Dashboard.css";

const TeacherDashboard = () => {
  const [activePage, setActivePage] = useState("Home");

  return (
    <div className="dashboard-container">
      <TeacherPanel />
      {/* <div className="content"> */}
        <main className="content">
          <header className="dashboard-header">
            {/* <h2>Welcome Back, John!</h2> */}
            <div className="dashboard-logo">ClassEase School</div>
            <div className="dashboard-nav">
              <div
                className={`nav-item ${activePage === "Home" ? "active" : ""}`}
                onClick={() => setActivePage("Home")}
              >
                Home
              </div>
              <div
                className={`nav-item ${activePage === "User Control" ? "active" : ""}`}
                onClick={() => setActivePage("User Control")}
              >
                User Control
              </div>
              <div
                className={`nav-item ${activePage === "Event Management" ? "active" : ""}`}
                onClick={() => setActivePage("Event Management")}
              >
                Event Management
              </div>
              <div
                className={`nav-item ${activePage === "Reports" ? "active" : ""}`}
                onClick={() => setActivePage("Reports")}
              >
                Reports
              </div>
              <div
                className={`nav-item ${activePage === "Contact" ? "active" : ""}`}
                onClick={() => setActivePage("Contact")}
              >
                Contact
              </div>
            </div>
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
      {/* </div> */}
    </div>
  );
};

export default TeacherDashboard;
