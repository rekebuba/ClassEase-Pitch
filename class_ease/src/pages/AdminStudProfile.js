import React, { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import ExamAssessmentReports from "./AdminExamAssessmentReports";
import api from '../services/api';
import { SubjectList } from './StudSubjectList'

const StudentProfile = ({ isProfileOpen, toggleAssessment, closeProfile, studentProfileSummary, assessmentSummary }) => {
    const [allSubjects, setAllSubjects] = useState([]);
    const [student, setStudent] = useState({});


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

    function calculateAge(birthday) {
        // birthday should be in the format 'YYYY-MM-DD'
        const birthDate = new Date(birthday);
        const today = new Date();

        return today.getFullYear() - birthDate.getFullYear();

    }

    useEffect(() => {
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
