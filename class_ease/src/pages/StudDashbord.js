import React, { useState, useEffect } from "react";
import StudentPanel from "../components/StdPanel";
import './styles/StudDashboard.css';
import './styles/Dashboard.css';
import StudentSubjectList from "./StudSubjectList";
import PopupScore from "./StudPopupScore";

const StudentDashboard = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [studentSummary, setStudentSummary] = useState({});

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const toggleAssessment = () => {
    setIsOpen(false);
  }

  const summary = (data) => {
    setStudentSummary(data);
  }

  return (
    <div className="admin-manage-container">
      <StudentPanel />
      <main className="content">
        <header className="dashboard-header">
          <div className="dashboard-logo">ClassEase School</div>
        </header>
        <StudentSubjectList toggleDropdown={toggleDropdown} studentSummary={summary} />
        <PopupScore isOpen={isOpen} toggleAssessment={toggleAssessment} studentData={studentSummary} />
      </main>
    </div>
  );
};
export default StudentDashboard;
