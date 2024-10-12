import React, { useState } from 'react';
import { FaTimes } from 'react-icons/fa';
// import ExamAssessmentReports from "./AdminExamAssessmentReports";


const TeachProfile = ({ isOpen, toggleProfile }) => {
    const [teacher] = useState({
        name: 'Jane Smith',
        age: 35,
        experience: '10 years',
        subjects: ['Math', 'Physics'],
        classes: ['Grade 10 - Section A', 'Grade 12 - Section B'],
        performance: {
            overall: 'Outstanding',
            studentFeedback: '4.8/5',
            passRate: '98%',
            attendance: '98%',
        },
        pictureUrl: 'https://example.com/teacher-picture.jpg', // Replace with actual image URL
        contact: {
            email: 'jane.smith@school.com',
            phone: '123-456-7890',
        },
        qualifications: ['B.Sc. in Physics', 'M.Sc. in Mathematics Education'],
        certifications: ['Certified Teacher', 'Advanced Classroom Management'],
    });

    return (
        <div className={`teacher-profile-view ${isOpen ? "open" : "close"}`}>
            <div className="profile-header-container">
                <h2>Teacher Data</h2>
                <button className="profile-fatimes" onClick={toggleProfile}><FaTimes size={24} /></button>
            </div>
            <div className="profile-header">
                <div className="teacher-picture">
                    <img src={teacher.pictureUrl} alt="Teacher" />
                </div>
                <div className="teacher-info">
                    <h2>{teacher.name}</h2>
                    <p>Age: {teacher.age}</p>
                    <p>Experience: {teacher.experience}</p>
                    <p>Email: {teacher.contact.email}</p>
                    <p>Phone: {teacher.contact.phone}</p>
                </div>
            </div>

            <div className="profile-content">
                <h3>Subjects Taught</h3>
                <ul>
                    {teacher.subjects.map((subject, index) => (
                        <li key={index}>{subject}</li>
                    ))}
                </ul>

                <h3>Classes Handled</h3>
                <ul>
                    {teacher.classes.map((cls, index) => (
                        <li key={index}>{cls}</li>
                    ))}
                </ul>

                <h3>Performance Overview</h3>
                <p>Overall Performance: {teacher.performance.overall}</p>
                <p>Student Feedback: {teacher.performance.studentFeedback}</p>
                <p>Pass Rate: {teacher.performance.passRate}</p>
                <p>Attendance: {teacher.performance.attendance}</p>

                <h3>Qualifications</h3>
                <ul>
                    {teacher.qualifications.map((qualification, index) => (
                        <li key={index}>{qualification}</li>
                    ))}
                </ul>

                <h3>Certifications</h3>
                <ul>
                    {teacher.certifications.map((certification, index) => (
                        <li key={index}>{certification}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default TeachProfile;
