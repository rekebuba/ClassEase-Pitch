import React, { useState, useEffect } from "react";
import StudentPanel from "../components/StdPanel";
import './styles/StudDashboard.css';
import './styles/Dashboard.css'; 

const StudentDashboard = () => {
  const [activePage, setActivePage] = useState("Home");
  return (
    <div className="dashboard-container">
      <StudentPanel />
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
