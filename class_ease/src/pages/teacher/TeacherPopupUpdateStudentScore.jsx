import { useState, useEffect, useCallback } from 'react';
import { FaTimes } from 'react-icons/fa';
import api from '../../services/api';
import Alert from '../../services/Alert';
import { InputOTP, InputOTPGroup, InputOTPSlot } from '@/components/ui/input-otp';

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
const TeacherPopupUpdateStudentScore = ({ isOpen, toggleAssessment, studentData, onSave }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [updateAssessmentData, setUpdateAssessmentData] = useState([]);
    const [individualAssessment, setIndividualAssessment] = useState({});

    const fetchIndividualAssessment = useCallback(async () => {
        try {
            const res = await api.get('/teacher/student/assessment', {
                params: {
                    student_id: studentData.student_id,
                    grade_id: studentData.grade_id,
                    subject_id: studentData.subject_id,
                    section_id: studentData.section_id,
                    semester: studentData.semester,
                    year: studentData.year,
                },
            });
            if (res.status === 200) {
                const updatedData = { ...studentData, ...res.data };
                setIndividualAssessment(updatedData);
            }
        } catch (error) {
            if (error.response?.data?.error) {
                showAlert("error", error.response.data.error);
            }
        }
    }, [studentData]);

    useEffect(() => {
        if (studentData === undefined) {
            return;
        }
        fetchIndividualAssessment();
    }, [studentData, fetchIndividualAssessment]);

    /**
     * @function handleScoreChange
     * @description Updates the score of an assessment.
     * @param {number} index - Index of the assessment in the array.
     * @param {number} value - New score value.
     * @returns {void}
     */
    const handleScoreChange = (index, value) => {
        const updatedAssessments = [...updateAssessmentData];
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
        const updatedAssessments = individualAssessment.assessment.map((assessment) => ({
            ...assessment,
        }));
        setUpdateAssessmentData(updatedAssessments);
    };

    /**
     * @function handleSave
     * @description Saves the updated assessment data.
     * @returns {void}
     */
    const handleSave = async () => {
        setIsEditing(false);
        try {
            const res = await api.put('/teacher/students/mark_list', { student_data: studentData, assessments: updateAssessmentData });
            if (res.status === 201) {
                showAlert("success", res.data['message']);
            }

        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                showAlert("warning", error.response.data['error']);
            }
            console.error(error);
        }
        // Fetch updated data and pass it to onSave
        await fetchIndividualAssessment();
        onSave(true); // to get teh updated student data
    };

    const calculateTotalScore = (assessments) => {
        return assessments.reduce((total, item) => total + item.score, 0);
    };

    return (
        <div className={`popup-overlay ${isOpen ? "open" : "close"}`}>
            <div className='popup-overlay-container score'>
                <div className="popup-table">
                    <div className="close-popup">
                        <h3>{studentData.name} {studentData.father_name} Score</h3>
                        <button onClick={() => {
                            setIsEditing(false);
                            setUpdateAssessmentData([]);
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
                            {(individualAssessment.assessment && individualAssessment.assessment.length > 0) &&
                                individualAssessment.assessment.map((assessment, index) => (
                                    <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f1f1f1' }}>
                                        <td style={{ textAlign: "center" }}>{assessment.assessment_type} ( {assessment.percentage}% )</td>
                                        <InputOTP
                                            maxLength={1}
                                            value={updateAssessmentData[index].score || 0}
                                            onChange={(value) => {
                                                let newScore = parseFloat(value);
                                                if (newScore > assessment.percentage) newScore = assessment.percentage;
                                                handleScoreChange(index, value);
                                            }}>
                                            <InputOTPGroup>
                                                <td>
                                                    {isEditing ? (
                                                        <InputOTPSlot key={index} index={index} />
                                                    ) : (
                                                        assessment.score !== null ? assessment.score : 'N/A'
                                                    )}
                                                </td>
                                            </InputOTPGroup>
                                        </InputOTP>
                                    </tr>
                                ))}
                        </tbody>
                    </table>
                    <div className='total-score'>
                        <h3><strong>Total Score: {individualAssessment.assessment ? calculateTotalScore(individualAssessment.assessment) : 'N/A'} / 100</strong></h3>
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
