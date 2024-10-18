import React, { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import ExamAssessmentReports from "./AdminExamAssessmentReports";

const assignStudentData = (data) => {
    if (data === undefined || Object.keys(data).length === 0) return {};
    return {
        name: `${data.name} ${data.father_name} ${data.grand_father_name}`,
        grade: data.grade,
        section: data.section,
        performance: data.performance || []
    };
}

const StudentProfile = ({ isOpen, toggleProfile, studentData }) => {
    const [student, setStudent] = useState({
        name: '',
        grade: '',
        section: '',
        performance: [],
        pictureUrl: 'https://example.com/student-picture.jpg'
    });

    useEffect(() => {
        const transformedData = assignStudentData(studentData)
        setStudent(transformedData);
    }, [studentData]);

    const calculateTotalScores = (semesters) => {
        const totalScores = {};
        for (let semester in semesters) {
            const scores = semesters[semester];
            if (Array.isArray(scores)) {
                const totalScore = scores.reduce((sum, assessment) => sum + (assessment.score || 0), 0);
                totalScores[semester] = totalScore;
            } else {
                totalScores[semester] = 0;  // In case no scores are available
            }
        }
        return totalScores;
    };


    return (
        <div className={`student-profile-view ${isOpen ? "open" : "close"}`}>
            <div className='manage-student-container'>
                <div className="profile-header-container">
                    <h2>Student Summary</h2>
                    <button className="profile-fatimes" onClick={toggleProfile}><FaTimes size={24} /></button>
                </div>
                <div className="profile-header">
                    <div className="student-picture">
                        <img src={student.pictureUrl} alt="Student" />
                    </div>
                    <div className="student-info">
                        <h2>{student.name} {student.father_name} {student.grand_father_name}</h2>
                        <p>Age: {student.date_of_birth}</p>
                        <p>Grade: {student.grade}</p>
                        <p>Section: {student.section}</p>
                    </div>
                </div>

                <div className="profile-content">
                    <h3>Performance Overview</h3>
                    {/* <p>Overall Performance: {student.performance.overall}</p> */}
                    {/* <p>Average Score: {student.performance.averageScore}%</p> */}

                    <ExamAssessmentReports />
                    <h4>Semester 1</h4>
                    <table className="subject-scores-table">
                        <thead>
                            <tr>
                                <th>Subject</th>
                                <th>Semester 1</th>
                                <th>Semester 2</th>
                                <th>Average By Semester</th>
                            </tr>
                        </thead>
                        <tbody>
                            {((student === undefined || Object.keys(student).length === 0) ? [] : student.performance).map((subject, index) => {
                                const totalScores = calculateTotalScores(subject.semesters);
                                return (
                                    <tr key={index}>
                                        <td>{subject.subject}</td>
                                        <td>{totalScores['semester1'] || 0}%</td>
                                        <td>{totalScores['semester2'] || 0}%</td>
                                        <td>{totalScores['semester1'] + totalScores['semester2'] || 0}%</td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};


export default StudentProfile;
