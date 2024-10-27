import React, { useState } from 'react';
import { FaTimes } from 'react-icons/fa';
import api from '../../services/api';
import Alert from '../../services/Alert';

/**
 * TeacherPopupUpdateStudentScore component allows teachers to update student scores.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {boolean} props.isOpen - Determines if the popup is open.
 * @param {Function} props.toggleAssessment - Function to toggle the assessment popup.
 * @param {Object} props.studentData - Data of the student including assessments.
 * @param {Array} props.studentData.assessment - Array of assessment objects.
 * @param {string} props.studentData.name - Name of the student.
 * @param {string} props.studentData.father_name - Father's name of the student.
 *
 * @example
 * const studentData = {
 *   name: "John",
 *   father_name: "Doe",
 *   assessment: [
 *     { assessment_type: "Quiz", percentage: 20, score: 18 },
 *     { assessment_type: "Exam", percentage: 80, score: 70 }
 *   ]
 * };
 * <TeacherPopupUpdateStudentScore
 *   isOpen={true}
 *   toggleAssessment={toggleFunction}
 *   studentData={studentData}
 * />
 *
 * @returns {JSX.Element} The TeacherPopupUpdateStudentScore component.
 */
const TeacherPopupUpdateStudentScore = ({ isOpen, toggleAssessment, studentData }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [updateAssessmentData, setUpdateAssessmentData] = useState([]);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });

    /**
     * @function handleScoreChange
     * @description Updates the score of an assessment.
     * @param {number} index - Index of the assessment in the array.
     * @param {number} value - New score value.
     * @returns {void}
     */
    const handleScoreChange = (index, value) => {
        const updatedAssessments = [...studentData.assessment];
        updatedAssessments[index].score = value;
        setUpdateAssessmentData(updatedAssessments);
    };

    /**
     * @function showAlert
     * @description Sets the alert message.
     * @param {string} type - Type of the alert.
     * @param {string} message - Message to display in the alert.
     * @returns {void}
     */
    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    /**
     * @function closeAlert
     * @description Closes the alert message.
     * @returns {void}
     */
    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    /**
     * @function handleEdit
     * @description Sets the editing mode to true.
     * @returns {void}
     */
    const handleEdit = () => {
        setIsEditing(true);
    };

    /**
     * @function handleSave
     * @description Saves the updated assessment data.
     * @returns {void}
     */
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

    /**
     * @function calculateTotal
     * @description Calculates the total score of the student.
     * @param {Object} studentData - Data of the student including assessments.
     * @param {Array} studentData.assessment - Array of assessment objects.
     * @returns {string} The total score of the student.
     * @returns {string} 'N/A' if no assessments are available.
     * @returns {string} The total score of the student.
     * @returns {number} 0 if no score is available.
     */
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
