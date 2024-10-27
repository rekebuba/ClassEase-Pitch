import React, { useState } from "react";
import "../../styles/AdminManageStudents.css";
import AdminPanel from "../../components/AdminPanel";
import AdminHeader from "../../components/AdminHeader";
import StudentProfile from "./AdminStudProfile";
import AdminStudentsList from "./AdminStudList";
import PopupScore from "../student/StudPopupScore";



const AdminManageStudents = () => {

  const [isAssesOpen, setIsAssesOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [studentProfileSummary, setStudentProfileSummary] = useState({});
  const [studentAssessmentSummary, setStudentAssessmentSummary] = useState({});

  const toggleProfile = () => {
    setIsProfileOpen(!isProfileOpen);
  };

  const closeProfile = () => {
    setIsProfileOpen(false);
  }

  const toggleAssessment = () => {
    setIsAssesOpen(!isAssesOpen);
  }

  const closeAssessment = () => {
    setIsAssesOpen(false);
  }

  const profileSummary = (data) => {
    setStudentProfileSummary(data);
  }

  const assessmentSummary = (data) => {
    setStudentAssessmentSummary(data);
  }

  return (
    <div className="admin-manage-container">
      <AdminPanel />
      <main className="content">
        <AdminHeader />
        <AdminStudentsList
          toggleProfile={toggleProfile}
          profileSummary={profileSummary}
        />
        <StudentProfile
          isProfileOpen={isProfileOpen}
          toggleAssessment={toggleAssessment}
          closeProfile={closeProfile}
          studentProfileSummary={studentProfileSummary}
          assessmentSummary={assessmentSummary}
        />
        <PopupScore
          isAssesOpen={isAssesOpen}
          closeAssessment={closeAssessment}
          assessmentSummary={studentAssessmentSummary}
        />
      </main>
    </div>
  );
};

export default AdminManageStudents;
