import { useState } from "react";
import "../../styles/AdminManageStudents.css";
import AdminPanel from "../../components/AdminPanel";
import AdminHeader from "../../components/AdminHeader";
import StudentProfile from "./AdminStudProfile";
import AdminStudentsList from "./AdminStudList";
import PopupScore from "../student/StudPopupScore";
import { Toaster } from '@/components/ui/sonner';


/**
 * AdminManageStudents component manages the state and behavior for the admin's student management interface.
 * 
 * @component
 * 
 * @example
 * return (
 *   <AdminManageStudents />
 * )
 * 
 * @returns {JSX.Element} The rendered component.
 * 
 * @description
 * This component handles the following functionalities:
 * - Toggling the visibility of the student profile and assessment popups.
 * - Managing the state for student profile and assessment summaries.
 * 
 * @state {boolean} isAssesOpen - State to track if the assessment popup is open.
 * @state {boolean} isProfileOpen - State to track if the profile popup is open.
 * @state {Object} studentProfileSummary - State to store the summary of the student's profile.
 * @state {Object} studentAssessmentSummary - State to store the summary of the student's assessment.
 * 
 * @component {AdminPanel} - Renders the admin panel.
 * @component {AdminHeader} - Renders the admin header.
 * @component {AdminStudentsList} - Renders the list of students with the ability to toggle profile popup and set profile summary.
 * @component {StudentProfile} - Renders the student profile popup with the ability to toggle assessment popup, close profile popup, and set assessment summary.
 * @component {PopupScore} - Renders the assessment popup with the ability to close it and set assessment summary.
 */
const AdminManageStudents = () => {

  const [isAssesOpen, setIsAssesOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [studentProfileSummary, setStudentProfileSummary] = useState({});
  const [studentAssessmentSummary, setStudentAssessmentSummary] = useState({});

  /**
   * @function toggleProfile - Toggles the visibility of the student profile popup.
   * @returns {void}
   */
  const toggleProfile = () => {
    setIsProfileOpen(!isProfileOpen);
  };

  /**
   * @function closeProfile - Closes the student profile popup.
   * @returns {void}
   */
  const closeProfile = () => {
    setIsProfileOpen(false);
  };

  /**
   * @function toggleAssessment - Toggles the visibility of the student assessment popup.
   * @return {void}
   */
  const toggleAssessment = () => {
    setIsAssesOpen(!isAssesOpen);
  };

  /**
   * @function closeAssessment - Closes the student assessment popup.
   * @return {void}
   */
  const closeAssessment = () => {
    setIsAssesOpen(false);
  };

  /**
   * @function profileSummary - Sets the student profile summary state.
   * @param {Object} data - The student profile summary data.
   * @returns {void}
   */
  const profileSummary = (data) => {
    setStudentProfileSummary(data);
  };

  /**
   * @function assessmentSummary - Sets the student assessment summary state.
   * @param {Object} data - The student assessment summary data.
   * @returns {void}
   */
  const assessmentSummary = (data) => {
    setStudentAssessmentSummary(data);
  };

  return (
    <div className="min-h-screen flex overflow-hidden flex-col">
      <AdminHeader />
      <div className="flex flex-1 scroll-m-0">
        <AdminPanel />
        <main className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
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
          <Toaster />
        </main>
      </div>
    </div>
  );
};

export default AdminManageStudents;
