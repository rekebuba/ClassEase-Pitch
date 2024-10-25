import React, { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
// import ExamAssessmentReports from "./AdminExamAssessmentReports";

const assignTeacherData = (data) => {
    if (!data || Object.keys(data).length === 0) return {};
    return {
        name: data.name || '',
        age: data.age || 0,
        experience: data.experience || '',
        classes: data.record || [],
        pictureUrl: 'https://example.com/teacher-picture.jpg',
        email: data.email || '',
        phone: data.phone || '',
        qualifications: data.qualifications || [],
        subjects: data.subjects || [],
    };
};

const TeachProfile = ({ isDetailOpen, toggleDetailProfile, teacherData }) => {
    const [teacher, setTeacher] = useState({
        name: '',
        age: null,
        email: '',
        phone: '',
        experience: '',
        subjects: [],
        classes: [],
        pictureUrl: 'https://example.com/teacher-picture.jpg',
        qualifications: [],
    });

    useEffect(() => {
        if (teacherData) {
            const transformedData = assignTeacherData(teacherData);
            setTeacher(transformedData);
        }
    }, [teacherData]);
    console.log(teacher)
    console.log(teacherData.record)

    return (
        <div className={`teacher-profile-view ${isDetailOpen ? "open" : "close"}`}>
            <div className="profile-header-container">
                <h2>Teacher Data</h2>
                <button className="profile-fatimes" onClick={toggleDetailProfile}><FaTimes size={24} /></button>
            </div>
            <div className="profile-header">
                <div className="teacher-picture">
                    <img src={teacher.pictureUrl} alt="Teacher" />
                </div>
                <div className="teacher-info">
                    <h2>{teacher.name}</h2>
                    <p>Age: {teacher.age}</p>
                    <p>Experience: {teacher.experience}</p>
                    <p>Email: {teacher.email}</p>
                    <p>Phone: {teacher.phone}</p>
                </div>
            </div>

            <div className="profile-content">
                <h3>Subjects Taught</h3>
                <ul>
                    {teacher.subjects && teacher.subjects.map((subject, index) => (
                        <li key={index}>{subject}</li>
                    ))}
                </ul>

                <h3>Classes Handled</h3>
                <ul>
                    {teacher.classes && teacher.classes.length > 0 ? (
                        teacher.classes.map((cls, index) => (
                            <li key={index}>Grade: {cls.grade}, Section: {cls.section}, Subject: {cls.subject}</li>
                        ))
                    ) : (
                        <li key='N/A'>N/A</li>
                    )}
                </ul>
                <h3>Qualifications</h3>
                <ul>
                    {teacher.qualifications && teacher.qualifications.map((qualification, index) => (
                        <li key={index}>{qualification}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default TeachProfile;
