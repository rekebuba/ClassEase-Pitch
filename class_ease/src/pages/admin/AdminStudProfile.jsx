import React, { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import ExamAssessmentReports from "./AdminExamAssessmentReports";
import api from '../../services/api';
import { SubjectList } from '../student/StudSubjectList';

/**
 * StudentProfile component displays a detailed profile of a student including their personal information and performance overview.
 *
 * @component
 * @param {Object} props - The properties object.
 * @param {boolean} props.isProfileOpen - A flag indicating whether the profile popup is open or closed.
 * @param {function} props.toggleAssessment - A function to toggle the assessment view.
 * @param {function} props.closeProfile - A function to close the profile popup.
 * @param {Object} props.studentProfileSummary - An object containing the summary of the student's profile.
 * @param {string} props.studentProfileSummary.student_id - The ID of the student.
 * @param {string} props.studentProfileSummary.grade - The grade of the student.
 * @param {string} props.studentProfileSummary.pictureUrl - The URL of the student's picture.
 * @param {string} props.studentProfileSummary.name - The name of the student.
 * @param {string} props.studentProfileSummary.father_name - The father's name of the student.
 * @param {string} props.studentProfileSummary.grand_father_name - The grandfather's name of the student.
 * @param {string} props.studentProfileSummary.date_of_birth - The date of birth of the student in 'YYYY-MM-DD' format.
 * @param {string} props.studentProfileSummary.section - The section of the student.
 * @param {Object} props.assessmentSummary - An object containing the summary of the student's assessment.
 *
 * @returns {JSX.Element} The rendered StudentProfile component.
 */
const StudentProfile = ({ isProfileOpen, toggleAssessment, closeProfile, studentProfileSummary, assessmentSummary }) => {
    const [allSubjects, setAllSubjects] = useState([]);
    const [student, setStudent] = useState({});

    /**
     * @function calculateAge
     * @param {string} birthday - The date of birth of the student in 'YYYY-MM-DD' format.
     * @returns {number} The age of the student.
     * @description Calculates the age of the student based on their date of birth.
     */
    function calculateAge(birthday) {
        // birthday should be in the format 'YYYY-MM-DD'
        const birthDate = new Date(birthday);
        const today = new Date();

        return today.getFullYear() - birthDate.getFullYear();

    }

    useEffect(() => {
        /**
         * @function lodeStudentSubjectList
         * @description Loads the list of subjects for the student.
         * @async
         * @returns {Promise<void>} The response data.
         * @throws {error} The error that was caught
         */
        const lodeStudentSubjectList = async () => {
            try {
                if (studentProfileSummary !== undefined && Object.keys(studentProfileSummary).length > 0) {
                    const response = await api.get(`/student/score`, {
                        params: {
                            student_id: studentProfileSummary.student_id,
                            grade: studentProfileSummary.grade,
                            semester: 1
                        }
                    });
                    setAllSubjects(response.data['student_assessment']);
                    // setStudent(response.data['student']);
                }
            } catch (error) {
                if (error.response && error.response.data && error.response.data['error']) {
                    console.error(error.response.data['error']);
                }
            }
        };
        lodeStudentSubjectList();
        setStudent(studentProfileSummary);
    }, [isProfileOpen, studentProfileSummary]);

    return (
        <div className={`popup-overlay ${isProfileOpen ? "open" : "close"}`}>
            <div className='popup-overlay-container'>
                <div className="close-popup">
                    <h2 style={{ margin: 0 }}>Student Summary</h2>
                    <button onClick={closeProfile} style={{ background: 'none', border: 'none', cursor: 'pointer' }}><FaTimes size={24} /></button>
                </div>
                <div className="popup-profile-header">
                    <div className="popup-profile-picture">
                        <img src={student.pictureUrl} alt="Student" />
                    </div>
                    <div className="popup-profile-info">
                        <h2>{student.name} {student.father_name} {student.grand_father_name} </h2>
                        <p>Age: {calculateAge(student.date_of_birth)}</p>
                        <p>Grade: {student.grade}</p>
                        <p style={{ margin: 0 }}>Section: {student.section}</p>
                    </div>
                </div>

                <div className="popup-profile-content">
                    <h3>Performance Overview</h3>
                    <ExamAssessmentReports subjectSummary={allSubjects} />
                    <SubjectList
                        allSubjects={allSubjects}
                        student={student}
                        toggleAssessment={toggleAssessment}
                        assessmentSummary={assessmentSummary}
                    />
                </div>
            </div>
        </div>
    );
};


export default StudentProfile;
