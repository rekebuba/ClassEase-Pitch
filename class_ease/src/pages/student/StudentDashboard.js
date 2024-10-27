import React, { useState, useEffect } from "react";
import StudentPanel from "../../components/StdPanel";
import '../../styles/StudDashboard.css';
import '../../styles/Dashboard.css';
import StudentSubjectList from "./StudSubjectList";
import PopupScore from "./StudPopupScore";

const StudentDashboard = () => {
  const [isAssesOpen, setIsAssesOpen] = useState(false);
  const [studentSummary, setStudentSummary] = useState({});

  const toggleAssessment = () => {
    setIsAssesOpen(!isAssesOpen);
  };

  const closeAssessment = () => {
    setIsAssesOpen(false);
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
        <StudentSubjectList
          toggleAssessment={toggleAssessment}
          assessmentSummary={summary}
        />
        <PopupScore
          isAssesOpen={isAssesOpen}
          closeAssessment={closeAssessment}
          assessmentSummary={studentSummary}
        />
      </main>
    </div>
  );
};
export default StudentDashboard;
