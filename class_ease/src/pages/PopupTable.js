import React, { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import api from '../services/api';
import Alert from './Alert';

const PopupTable = ({ isOpen, toggleAssessment, studentData }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [assessmentData, setAssessmentData] = useState([]);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });


    const handleScoreChange = (index, value) => {
        const updatedAssessments = [...assessmentData];
        updatedAssessments[index].score = value;
        setAssessmentData(updatedAssessments);
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
            const res = api.put('/teacher/students/mark_list', { student_data: studentData, assessments: assessmentData });
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

    useEffect(() => {
        if (assessmentData.length === 0 && studentData.assessment) {
            setAssessmentData(studentData.assessment);
        }
    }, [assessmentData, studentData.assessment])

    console.log("Student data: ", studentData);
    console.log("assessment Data: ", assessmentData);

    return (
        <div className={`popup-table-overlay ${isOpen ? "open" : "close"}`}>
            <div className="popup-table">
                <div className="popup-header-container">
                    <h3>{studentData.name} {studentData.father_name} Score</h3>
                    <button className="popup-fatimes" onClick={() => {
                        setIsEditing(false);
                        toggleAssessment();
                    }}
                    ><FaTimes size={15} /></button>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {(assessmentData && assessmentData.length > 0) &&
                            assessmentData.map((assessment, index) => (
                                <tr key={index}>
                                    <td>{assessment.assessment_type} ({assessment.percentage}%)</td>
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
                <button className="popup-table-edit-btn" onClick={handleEdit}>
                    Edit
                </button>
                <button className="popup-table-save-btn" onClick={handleSave}>
                    Save
                </button>
            </div>
            <Alert
                type={alert.type}
                message={alert.message}
                show={alert.show}
                onClose={closeAlert}
            />
        </div>
    );
};

export default PopupTable;
