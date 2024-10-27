import React, { useState } from 'react';
import { FaTimes } from 'react-icons/fa';
import api from '../../services/api';
import Alert from '../../services/Alert';

const TeacherPopupUpdateStudentScore = ({ isOpen, toggleAssessment, studentData }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [updateAssessmentData, setUpdateAssessmentData] = useState([]);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });


    const handleScoreChange = (index, value) => {
        const updatedAssessments = [...studentData.assessment];
        updatedAssessments[index].score = value;
        setUpdateAssessmentData(updatedAssessments);
    };

    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleSave = () => {
        setIsEditing(false);
        try {
            const res = api.put('/teacher/students/mark_list', { student_data: studentData, assessments: updateAssessmentData });
            if (res.status === 201) {
                showAlert("success", res.status['message']);
            }

        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                showAlert("warning", error.response.data['error']);
            }
            console.error(error);
        }
    };

    const calculateTotal = (studentData) => {
        if (studentData.assessment === undefined || studentData.assessment.length === 0) return 'N/A';
        const totalScore = studentData.assessment.reduce((acc, assessment) => acc + (assessment.score || 0), 0);
        return totalScore;
    };

    return (
        <div className={`popup-overlay ${isOpen ? "open" : "close"}`}>
            <div className='popup-overlay-container score'>
                <div className="popup-table">
                    <div className="close-popup">
                        <h3>{studentData.name} {studentData.father_name} Score</h3>
                        <button onClick={() => {
                            setIsEditing(false);
                            toggleAssessment();
                        }}
                        ><FaTimes size={15} /></button>
                    </div>
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th style={{ textAlign: "center" }}>Type</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {(studentData.assessment && studentData.assessment.length > 0) &&
                                studentData.assessment.map((assessment, index) => (
                                    <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f1f1f1' }}>
                                        <td style={{ textAlign: "center" }}>{assessment.assessment_type} ({assessment.percentage}%)</td>
                                        <td>
                                            {isEditing ? (
                                                <input
                                                    type="number"
                                                    min={0}
                                                    max={assessment.percentage}
                                                    value={assessment.score || 0}
                                                    onChange={(e) => {
                                                        let value = parseFloat(e.target.value);
                                                        if (value > assessment.percentage) value = assessment.percentage;
                                                        handleScoreChange(index, value);
                                                    }}
                                                />
                                            ) : (
                                                assessment.score !== null ? assessment.score : ''
                                            )}
                                        </td>
                                    </tr>
                                ))}
                        </tbody>
                    </table>
                    <div className='total-score'>
                        <h3><strong>Total Score: {calculateTotal(studentData)} / 100</strong></h3>
                    </div>
                    <div className='popup-table-btn'>
                        <button className="popup-table-edit-btn" onClick={handleEdit}>
                            Edit
                        </button>
                        <button className="popup-table-save-btn" onClick={handleSave}>
                            Save
                        </button>
                    </div>
                </div>
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

export default TeacherPopupUpdateStudentScore;
