import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { StudentPanel } from "@/components/layout";
import { StudentPopupScore, StudentSubjectList } from "@/features/student";
import classEaseHeader from '../../assets/images/ClassEase-header.png';
import '../../styles/StudDashboard.css';
import '../../styles/Dashboard.css';


/**
 * StudentDashboard component renders the main dashboard for students.
 * It includes the student panel, subject list, and a popup for assessment scores.
 *
 * @component
 * @example
 * return (
 *   <StudentDashboard />
 * )
 *
 * @returns {JSX.Element} The rendered student dashboard component.
 *
 * @function
 * @name StudentDashboard
 * @description
 * - Manages the state for assessment popup visibility and student summary.
 * - Toggles the assessment popup visibility.
 * - Closes the assessment popup.
 * - Updates the student summary with provided data.
 */
const StudentDashboard = () => {
  const [isAssesOpen, setIsAssesOpen] = useState(false);
  const [studentSummary, setStudentSummary] = useState({});
  const navigate = useNavigate();


  /**
   * Navigates the user to the home page.
   */
  const goToHome = () => {
    navigate("/");
  };

  /**
   * @function toggleAssessment
   * @description Toggles the visibility of the assessment popup.
   * @returns {void}
   */
  const toggleAssessment = () => {
    setIsAssesOpen(!isAssesOpen);
  };

  /**
   * @function closeAssessment
   * @description Closes the assessment popup.
   * @returns {void}
   */
  const closeAssessment = () => {
    setIsAssesOpen(false);
  };

  /**
   * @function summary
   * @param {object} data - The summary of the student's assessments.
   * @description Updates the student summary with provided data.
   * @returns {void}
   */
  const summary = (data) => {
    setStudentSummary(data);
  };

  return (
    <div className="admin-manage-container">
      <StudentPanel />
      <main className="content">
        <header className="dashboard-header">
          <div className="header-logo" onClick={goToHome}>
            <img src={classEaseHeader} alt="ClassEase School" />
          </div>
        </header>
        <StudentSubjectList
          toggleAssessment={toggleAssessment}
          assessmentSummary={summary}
        />
        <StudentPopupScore
          isAssesOpen={isAssesOpen}
          closeAssessment={closeAssessment}
          assessmentSummary={studentSummary}
        />
      </main>
    </div>
  );
};
export default StudentDashboard;
