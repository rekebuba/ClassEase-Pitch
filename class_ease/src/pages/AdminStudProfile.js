import React, { useState } from 'react';
import { FaTimes } from 'react-icons/fa';
import ExamAssessmentReports from "./AdminExamAssessmentReports";


const StudentProfile = ({ isOpen, toggleProfile }) => {
    const [student] = useState({
        name: 'John Doe',
        age: 16,
        grade: 'Grade 10',
        section: 'Section A',
        performance: {
            overall: 'Excellent',
            subjects: [
                { name: 'Math', score: 95 },
                { name: 'English', score: 88 },
                { name: 'Science', score: 92 },
                { name: 'History', score: 85 },
            ],
            averageScore: 90,
            attendance: '95%',
        },
        pictureUrl: 'https://example.com/student-picture.jpg', // Replace with actual image URL
    });

    console.log(isOpen);

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
                            <h2>{student.name}</h2>
                            <p>Age: {student.age}</p>
                            <p>Grade: {student.grade}</p>
                            <p>Section: {student.section}</p>
                        </div>
                    </div>

                    <div className="profile-content">
                        <h3>Performance Overview</h3>
                        <p>Overall Performance: {student.performance.overall}</p>
                        <p>Average Score: {student.performance.averageScore}%</p>
                        <p>Attendance: {student.performance.attendance}</p>

                        <h4>Subject Scores</h4>
                        <ExamAssessmentReports />
                        <table className="subject-scores-table">
                            <thead>
                                <tr>
                                    <th>Subject</th>
                                    <th>Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                {student.performance.subjects.map((subject, index) => (
                                    <tr key={index}>
                                        <td>{subject.name}</td>
                                        <td>{subject.score}%</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
        </div>
    );
};


export default StudentProfile;
