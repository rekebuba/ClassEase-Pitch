import React, { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import Api from '../../services/api';
import Alert from '../../services/Alert';


const AdminAssignTeacher = ({ isEditOpen, toggleEditProfile, teacherData }) => {
    const [teachers, setTeachers] = useState({ name: '', subjects: [] });
    const [classGrade, setClassGrade] = useState('');
    const [selectedSection, setSelectedSection] = useState([]);
    const [subjects, setSubjects] = useState([]);
    const [currentYear] = useState(new Date().getFullYear());
    const [selectedYear, setSelectedYear] = useState("2024/25");
    const [alert, setAlert] = useState({ type: "", message: "", show: false });


    useEffect(() => {
        if (!teacherData || Object.keys(teacherData).length === 0) return;
        const data = {
            name: teacherData.name || '',
            subjects: teacherData.subjects || [],
        };

        setTeachers(data);
    }, [teacherData]);

    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    const handleAssign = async (e) => {
        e.preventDefault();

        try {
            await Api.put('/admin/assign-teacher', {
                teacher_id: teacherData.id,
                grade: classGrade,
                section: selectedSection,
                subjects_taught: subjects,
                mark_list_year: selectedYear,
            });
            showAlert("success", "Teacher assigned successfully");
        } catch (error) {
            const errorMessage = error.response?.data?.error ?? "An unexpected error occurred.";
            showAlert("warning", errorMessage);
        }
    };
    const handleYearChange = e => setSelectedYear(e.target.value);

    const handleSectionChange = (e) => {
        const { value, checked } = e.target;
        if (checked) {
            setSelectedSection([...selectedSection, value]);
        } else {
            setSelectedSection(selectedSection.filter((section) => section !== value))
        }
    }

    return (
        <div className={`popup-overlay ${isEditOpen ? "open" : "close"}`}>
            <div className='popup-overlay-container'>
                <div className="close-popup">
                    <h2 style={{ margin: 0 }}>Assign Teacher to Classes</h2>
                    <button onClick={toggleEditProfile}><FaTimes size={24} /></button>
                </div>
                <form onSubmit={handleAssign}>
                    <div className="teacher-form-group">
                        <label htmlFor="teacher">Teacher</label>
                        <select
                            id="teacher"
                            name="teacher"
                            value={teachers.name}
                            onChange={(e) => setTeachers({ ...teachers, name: e.target.value })}
                            required
                        >
                            <option
                                key="default"
                                value={teachers.name}>
                                {teachers.name}
                            </option>
                        </select>
                    </div>
                    <div className="teacher-form-group">
                        <label htmlFor="classGrade">Select Class Grade</label>
                        <select
                            id="classGrade"
                            name="classGrade"
                            value={classGrade}
                            onChange={(e) => setClassGrade(e.target.value)}
                            required
                        >
                            <option value="">Select Grade</option>
                            {Array.from({ length: 12 }, (_, i) => i + 1).map(grade => (
                                <option key={grade} value={grade}>
                                    Grade {grade}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="form-group subjects">
                        <label htmlFor="section">Section:</label>
                        <div className="checkbox-group">
                            {['A', 'B', 'C'].map((section) => (
                                <div className="subject-container" key={section}>
                                    <label>
                                        <input
                                            type="checkbox"
                                            value={section}
                                            checked={selectedSection.includes(section)}
                                            onChange={handleSectionChange}
                                        />
                                        {section}
                                    </label>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="teacher-form-group">
                        <label htmlFor="year">Year:</label>
                        <select id="year" value={selectedYear} onChange={handleYearChange}>
                            {/* Dynamic Year Options */}
                            {Array.from({ length: 3 }, (_, i) => currentYear - i).map(year => (
                                <option key={year} value={year}>
                                    {year}/{(year + 1) % 100}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="teacher-form-group">
                        <label htmlFor="subjects">Select Subjects</label>
                        <select
                            id="subjects"
                            name="subjects"
                            value={subjects}
                            onChange={(e) => setSubjects(Array.from(e.target.selectedOptions, option => option.value))}
                            required
                            multiple
                        >
                            {(teachers.subjects && teachers.subjects.length > 0) ? (
                                teachers.subjects.map((subject, index) => (
                                    <option key={index} value={subject}>
                                        {subject}
                                    </option>
                                ))
                            ) : (
                                <option disabled>No subjects available</option>
                            )}
                        </select>
                    </div>
                    <button type="submit" className="teacher-assign-btn">
                        Assign Teacher
                    </button>
                </form>
                <Alert
                    type={alert.type}
                    message={alert.message}
                    show={alert.show}
                    onClose={closeAlert}
                />
            </div>
        </div>

    );
};

export default AdminAssignTeacher;
