import React from "react";
import TeacherPanel from "../../components/TeachPanel";
import "../../styles/TeacherDashboard.css";
import "../../styles/Dashboard.css";
import TeacherHeader from "../../components/TeachHeader";

/**
 * TeacherDashboard component
 * @component
 * @return {component} TeacherDashboard
 * @example
 * return <TeacherDashboard />
 */
const TeacherDashboard = () => {
  return (
    <div className="admin-manage-container">
      <TeacherPanel />
      <main className="content">
        <TeacherHeader />
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
      </main>
    </div>
  );
};

export default TeacherDashboard;
